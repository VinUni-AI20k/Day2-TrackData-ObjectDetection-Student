"""Công cụ kiểm tra nhãn Ngày 2: đọc bản xuất CVAT, kiểm tra, đối chiếu và tính precision/recall.

Chạy từ thư mục gốc của repo, ví dụ:

    python src/day2_lab.py audit --coco exports/coco-v1.zip --yolo exports/yolo-v1.zip --out outputs/v1
    python src/day2_lab.py compare --mine exports/coco-v1.zip --reference reference/day2-reference.zip --out outputs/v1
    python src/day2_lab.py model-check --labels exports/coco-v1.zip

Bạn không cần sửa tệp này. Phần cần tự viết nằm trong ``src/cp1_box_math.py``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
CLASS_NAMES = ["car", "truck", "bus", "van"]
IMAGE_SIZE = (640, 640)
EDGE_TOLERANCE_PX = 1.0
# Ngưỡng ghép hộp dùng trong bài. 0.5 là ngưỡng AP50 quen thuộc của COCO/Ultralytics.
MATCH_IOU = 0.5
# Gợi ý xem lại: hộp đã ghép nhưng IoU thấp hơn mức này được đưa vào danh sách "cần xem lỏng/lệch".
# Đây là mốc ôn tập của lớp, không phải tiêu chuẩn chất lượng.
REVIEW_IOU = 0.75


# ---------------------------------------------------------------- hình học hộp

def yolo_to_xyxy(line: str, width: int, height: int) -> tuple[int, list[float]]:
    """``class xc yc w h`` (chuẩn hóa 0..1) -> (class_id, [x1, y1, x2, y2]) theo điểm ảnh."""
    parts = line.split()
    if len(parts) != 5:
        raise ValueError(f"Dòng YOLO cần đúng 5 số, nhận được: {line!r}")
    cls = int(parts[0])
    xc, yc, w, h = (float(v) for v in parts[1:])
    return cls, [(xc - w / 2) * width, (yc - h / 2) * height, (xc + w / 2) * width, (yc + h / 2) * height]


def coco_to_xyxy(bbox: list[float]) -> list[float]:
    """COCO ``[x, y, w, h]`` (góc trên-trái, điểm ảnh) -> ``[x1, y1, x2, y2]``."""
    x, y, w, h = (float(v) for v in bbox)
    return [x, y, x + w, y + h]


def iou(a: list[float], b: list[float]) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = area(a) + area(b) - inter
    return inter / union if union > 0 else 0.0


def area(box: list[float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


# ---------------------------------------------------------------- tệp và ZIP

def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_members(path: Path) -> dict[str, bytes]:
    """Đọc tệp văn bản nhỏ trong ZIP hoặc thư mục; bỏ qua ảnh. Chặn đường dẫn thoát ra ngoài."""
    members: dict[str, bytes] = {}
    if path.is_dir():
        for file in path.rglob("*"):
            if file.is_file() and file.suffix.lower() in {".txt", ".yaml", ".yml", ".json", ".xml"}:
                members[file.relative_to(path).as_posix()] = file.read_bytes()
        return members
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            name = PurePosixPath(info.filename)
            if info.is_dir() or name.is_absolute() or ".." in name.parts:
                continue
            if name.suffix.lower() in {".txt", ".yaml", ".yml", ".json", ".xml"}:
                if info.file_size > 50_000_000:
                    raise ValueError(f"Tệp quá lớn trong ZIP: {info.filename}")
                members[str(name)] = archive.read(info)
    return members


def _image_sizes() -> dict[str, tuple[int, int]]:
    sizes = {}
    manifest = DATA / "image-manifest.csv"
    with manifest.open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            sizes[row["image_id"]] = (int(row["width"]), int(row["height"]))
    return sizes


def _parse_names(text: str) -> list[str]:
    """Đọc ``names`` trong data.yaml của CVAT (dạng dict ``0: car`` hoặc list ``[car, ...]``)."""
    try:
        import yaml

        names = yaml.safe_load(text).get("names")
    except ImportError:  # pragma: no cover - dự phòng khi thiếu PyYAML
        names = {}
        inside = False
        for raw in text.splitlines():
            if raw.strip().startswith("names:"):
                inside = True
                continue
            if inside and ":" in raw and raw.startswith((" ", "\t")):
                key, value = raw.split(":", 1)
                names[int(key.strip())] = value.strip().strip("'\"")
            elif inside and raw.strip():
                break
    if isinstance(names, dict):
        return [str(names[k]) for k in sorted(names, key=int)]
    return [str(n) for n in names or []]


# ---------------------------------------------------------------- đọc bản xuất

def load_export(path: str | Path) -> dict:
    """Đọc bản xuất COCO 1.0 hoặc Ultralytics YOLO Detection của CVAT (ZIP hoặc thư mục).

    Trả về ``{"format", "names", "images": {image_id: [box, ...]}, "problems": [...]}``;
    mỗi ``box`` có ``label``, ``xyxy`` và, với COCO, ``occluded`` / ``truncated``.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Không thấy {path}")
    members = _read_members(path)
    coco = [n for n in members if n.endswith(".json") and "instances" in PurePosixPath(n).name]
    if coco:
        return _load_coco(members, coco)
    if any(PurePosixPath(n).name == "data.yaml" for n in members):
        return _load_yolo(members)
    raise ValueError(f"{path.name}: không nhận ra COCO (annotations/instances_*.json) hoặc YOLO (data.yaml)")


def _flag(value) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return None


def _load_coco(members: dict[str, bytes], files: list[str]) -> dict:
    result = {"format": "coco", "names": [], "images": {}, "problems": []}
    for name in sorted(files):
        doc = json.loads(members[name])
        categories = {c["id"]: c["name"] for c in doc.get("categories", [])}
        result["names"] = [categories[k] for k in sorted(categories)]
        images = {}
        for image in doc.get("images", []):
            stem = PurePosixPath(image["file_name"]).stem
            images[image["id"]] = stem
            result["images"].setdefault(stem, [])
        for ann in doc.get("annotations", []):
            stem = images.get(ann.get("image_id"))
            if stem is None:
                result["problems"].append(f"Annotation {ann.get('id')} trỏ tới image_id không tồn tại")
                continue
            attributes = ann.get("attributes") or {}
            if not isinstance(attributes, dict):
                attributes = {}
            result["images"][stem].append(
                {
                    "label": categories.get(ann.get("category_id"), f"id{ann.get('category_id')}"),
                    "xyxy": coco_to_xyxy(ann["bbox"]),
                    "occluded": _flag(attributes.get("occluded")),
                    "truncated": _flag(attributes.get("truncated")),
                    "source": f"{name}#{ann.get('id')}",
                }
            )
    return result


def _load_yolo(members: dict[str, bytes]) -> dict:
    yaml_name = next(n for n in members if PurePosixPath(n).name == "data.yaml")
    names = _parse_names(members[yaml_name].decode("utf-8"))
    sizes = _image_sizes()
    result = {"format": "yolo", "names": names, "images": {}, "problems": []}
    for name in sorted(members):
        parts = PurePosixPath(name).parts
        if "labels" not in parts or not name.endswith(".txt"):
            continue
        stem = PurePosixPath(name).stem
        width, height = sizes.get(stem, IMAGE_SIZE)
        boxes = result["images"].setdefault(stem, [])
        for number, line in enumerate(members[name].decode("utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                cls, xyxy = yolo_to_xyxy(line, width, height)
                values = [float(v) for v in line.split()[1:]]
            except ValueError as error:
                result["problems"].append(f"{name}:{number}: {error}")
                continue
            if any(v < 0 or v > 1 for v in values):
                result["problems"].append(f"{name}:{number}: tọa độ chuẩn hóa nằm ngoài 0..1")
            label = names[cls] if 0 <= cls < len(names) else f"id{cls}"
            boxes.append({"label": label, "xyxy": xyxy, "source": f"{name}:{number}"})
    return result


# ---------------------------------------------------------------- CP3: kiểm tra bản xuất

def _touches_edge(box: list[float], width: int, height: int) -> bool:
    tol = EDGE_TOLERANCE_PX
    return box[0] <= tol or box[1] <= tol or box[2] >= width - tol or box[3] >= height - tol


def audit(coco_path: str | Path, yolo_path: str | Path) -> dict:
    """Kiểm tra hai bản xuất của cùng một lần gán nhãn. ``errors`` phải rỗng trước khi nộp."""
    coco, yolo = load_export(coco_path), load_export(yolo_path)
    errors: list[str] = []
    warnings: list[str] = []
    if coco["format"] != "coco":
        errors.append("--coco không phải bản xuất COCO 1.0")
    if yolo["format"] != "yolo":
        errors.append("--yolo không phải bản xuất Ultralytics YOLO Detection")
    errors += coco["problems"] + yolo["problems"]
    if yolo["names"] != CLASS_NAMES:
        errors.append(f"Thứ tự lớp YOLO là {yolo['names']}, cần {CLASS_NAMES}")
    if sorted(coco["names"]) != sorted(CLASS_NAMES):
        errors.append(f"Tên lớp COCO là {coco['names']}, cần đúng {CLASS_NAMES}")

    sizes = _image_sizes()
    per_image = []
    for stem in sorted(sizes):
        c_boxes = coco["images"].get(stem)
        y_boxes = yolo["images"].get(stem)
        if c_boxes is None:
            errors.append(f"{stem}: thiếu trong bản COCO")
        if y_boxes is None:
            errors.append(f"{stem}: thiếu tệp nhãn trong bản YOLO")
        c_boxes, y_boxes = c_boxes or [], y_boxes or []
        width, height = sizes[stem]
        for box in c_boxes:
            if area(box["xyxy"]) < 1:
                errors.append(f"{stem}: hộp diện tích 0 ({box['source']})")
            if box["label"] not in CLASS_NAMES:
                errors.append(f"{stem}: lớp lạ {box['label']!r}")
            if box["truncated"] is None:
                errors.append(f"{stem}: hộp {box['source']} thiếu thuộc tính truncated")
            elif box["truncated"] != _touches_edge(box["xyxy"], width, height):
                state = "chạm mép ảnh nhưng truncated=false" if not box["truncated"] else "truncated=true nhưng không chạm mép"
                warnings.append(f"{stem}: hộp {box['source']} {state} — kiểm tra lại")
            if box["occluded"] is None:
                warnings.append(f"{stem}: hộp {box['source']} không có cờ occluded trong COCO")
        matched = _match(y_boxes, c_boxes, 0.98, class_aware=True)
        if len(c_boxes) != len(y_boxes) or matched["tp"] != len(c_boxes):
            errors.append(
                f"{stem}: COCO có {len(c_boxes)} hộp, YOLO có {len(y_boxes)}, chỉ {matched['tp']} hộp trùng — "
                "hai bản xuất không cùng một trạng thái nhãn"
            )
        per_image.append(
            {
                "image_id": stem,
                "boxes": len(c_boxes),
                "occluded": sum(1 for b in c_boxes if b["occluded"]),
                "truncated": sum(1 for b in c_boxes if b["truncated"]),
                **{name: sum(1 for b in c_boxes if b["label"] == name) for name in CLASS_NAMES},
            }
        )
    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "per_image": per_image,
        "total_boxes": sum(r["boxes"] for r in per_image),
        "lock": {Path(p).name: sha256_file(p) for p in (coco_path, yolo_path) if Path(p).is_file()},
    }


# ---------------------------------------------------------------- CP4/CP5: ghép hộp, precision/recall

def _match(pred: list[dict], ref: list[dict], threshold: float, class_aware: bool) -> dict:
    """Ghép tham lam theo IoU giảm dần (mỗi hộp chỉ ghép một lần)."""
    pairs = []
    for i, p in enumerate(pred):
        for j, r in enumerate(ref):
            if class_aware and p["label"] != r["label"]:
                continue
            value = iou(p["xyxy"], r["xyxy"])
            if value >= threshold:
                pairs.append((value, i, j))
    used_p, used_r, matches = set(), set(), []
    for value, i, j in sorted(pairs, reverse=True):
        if i in used_p or j in used_r:
            continue
        used_p.add(i)
        used_r.add(j)
        matches.append((i, j, value))
    return {
        "tp": len(matches),
        "matches": matches,
        "fp": [i for i in range(len(pred)) if i not in used_p],
        "fn": [j for j in range(len(ref)) if j not in used_r],
    }


def precision_recall(tp: int, fp: int, fn: int) -> tuple[float, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return precision, recall


def compare(mine: dict, reference: dict, threshold: float = MATCH_IOU) -> tuple[dict, list[dict]]:
    """So nhãn của bạn với nhãn tham chiếu. Coi tham chiếu là "đúng" để đếm:

    - TP: hộp của bạn ghép được (IoU >= threshold, bỏ qua lớp);
    - FP (thừa): hộp của bạn không ghép được;
    - FN (bỏ sót): hộp tham chiếu không ai ghép.
    """
    rows, tp, fp, fn, class_ok, ious = [], 0, 0, 0, 0, []
    for stem in sorted(set(mine["images"]) | set(reference["images"])):
        a, b = mine["images"].get(stem, []), reference["images"].get(stem, [])
        result = _match(a, b, threshold, class_aware=False)
        tp, fp, fn = tp + result["tp"], fp + len(result["fp"]), fn + len(result["fn"])
        for i, j, value in result["matches"]:
            ious.append(value)
            same = a[i]["label"] == b[j]["label"]
            class_ok += same
            ratio = area(a[i]["xyxy"]) / max(area(b[j]["xyxy"]), 1e-9)
            issue = []
            if not same:
                issue.append("sai lớp")
            if value < REVIEW_IOU:
                issue.append("box lỏng" if ratio > 1 else "box chật/lệch")
            rows.append(_row(stem, "match", a[i], b[j], value, ratio, ", ".join(issue)))
        rows += [_row(stem, "extra", a[i], None, None, None, "thừa (FP)") for i in result["fp"]]
        rows += [_row(stem, "missed", None, b[j], None, None, "bỏ sót (FN)") for j in result["fn"]]
    precision, recall = precision_recall(tp, fp, fn)
    summary = {
        "iou_threshold": threshold,
        "tp": tp,
        "fp_extra": fp,
        "fn_missed": fn,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "class_agreement_on_matches": round(class_ok / tp, 3) if tp else 0.0,
        "mean_iou_on_matches": round(sum(ious) / len(ious), 3) if ious else 0.0,
        "review_rows": sum(1 for r in rows if r["issue"]),
    }
    return summary, rows


def _row(stem, kind, mine, ref, value, ratio, issue) -> dict:
    fmt = lambda box: " ".join(f"{v:.0f}" for v in box["xyxy"]) if box else ""
    return {
        "image_id": stem,
        "kind": kind,
        "my_label": mine["label"] if mine else "",
        "ref_label": ref["label"] if ref else "",
        "iou": f"{value:.3f}" if value is not None else "",
        "area_ratio_mine_over_ref": f"{ratio:.2f}" if ratio is not None else "",
        "my_xyxy": fmt(mine),
        "ref_xyxy": fmt(ref),
        "issue": issue,
    }


def load_predictions(path: str | Path = DATA / "model-predictions" / "yolo11n-predictions.json", min_score: float = 0.25) -> dict:
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    images = {
        stem: [{"label": b["label"], "xyxy": b["xyxy"]} for b in boxes if b["score"] >= min_score]
        for stem, boxes in doc["images"].items()
    }
    return {"format": "predictions", "names": [], "images": images, "problems": [], "meta": doc}


def model_check(labels: dict, predictions: dict | None = None, threshold: float = MATCH_IOU) -> dict:
    """Chấm dự đoán của mô hình bằng một bộ nhãn. Nhãn khác nhau -> điểm của cùng mô hình khác nhau."""
    predictions = predictions or load_predictions()
    summary, _ = compare(predictions, labels, threshold)
    return {k: summary[k] for k in ("iou_threshold", "tp", "fp_extra", "fn_missed", "precision", "recall")}


# ---------------------------------------------------------------- ảnh phủ hộp

def draw_overlay(stem: str, mine: dict, reference: dict | None, target: str | Path) -> Path:
    from PIL import Image, ImageDraw

    image = Image.open(DATA / "images" / f"{stem}.jpg").convert("RGB")
    draw = ImageDraw.Draw(image)
    for box in (reference or {}).get("images", {}).get(stem, []):
        draw.rectangle(box["xyxy"], outline=(0, 200, 0), width=2)
    for box in mine["images"].get(stem, []):
        color = (255, 140, 0) if box.get("occluded") or box.get("truncated") else (220, 30, 30)
        draw.rectangle(box["xyxy"], outline=color, width=2)
        tag = box["label"] + ("·occ" if box.get("occluded") else "") + ("·trunc" if box.get("truncated") else "")
        draw.text((box["xyxy"][0] + 2, box["xyxy"][1] + 1), tag, fill=color)
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target)
    return target


# ---------------------------------------------------------------- dòng lệnh

def _write(out: Path, name: str, payload) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / name
    if name.endswith(".csv"):
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(payload[0]) if payload else ["image_id"])
            writer.writeheader()
            writer.writerows(payload)
    else:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("audit", help="CP3: kiểm tra bản xuất COCO + YOLO")
    p.add_argument("--coco", required=True)
    p.add_argument("--yolo", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("compare", help="CP4: so với nhãn tham chiếu, tính precision/recall")
    p.add_argument("--mine", required=True)
    p.add_argument("--reference", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--iou", type=float, default=MATCH_IOU)
    p = sub.add_parser("model-check", help="CP5: chấm dự đoán YOLO11n bằng một bộ nhãn")
    p.add_argument("--labels", required=True, nargs="+")
    p.add_argument("--iou", type=float, default=MATCH_IOU)
    p = sub.add_parser("overlay", help="vẽ hộp của bạn (đỏ/cam) và tham chiếu (xanh) lên ảnh")
    p.add_argument("--mine", required=True)
    p.add_argument("--reference")
    p.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    if args.command == "audit":
        report = audit(args.coco, args.yolo)
        path = _write(Path(args.out), "audit.json", report)
        print(f"Kết quả: {report['status'].upper()} — {report['total_boxes']} hộp")
        for line in report["errors"]:
            print("  LỖI     ", line)
        for line in report["warnings"]:
            print("  CẢNH BÁO", line)
        print(f"Đã ghi {path}")
        return 0 if report["status"] == "pass" else 1
    if args.command == "compare":
        summary, rows = compare(load_export(args.mine), load_export(args.reference), args.iou)
        _write(Path(args.out), "compare-summary.json", summary)
        path = _write(Path(args.out), "compare-rows.csv", rows)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print(f"Danh sách từng hộp: {path}")
        return 0
    if args.command == "model-check":
        for label_path in args.labels:
            print(Path(label_path).name, json.dumps(model_check(load_export(label_path), threshold=args.iou)))
        return 0
    if args.command == "overlay":
        mine = load_export(args.mine)
        reference = load_export(args.reference) if args.reference else None
        for stem in sorted(_image_sizes()):
            print(draw_overlay(stem, mine, reference, Path(args.out) / f"{stem}-overlay.png"))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
