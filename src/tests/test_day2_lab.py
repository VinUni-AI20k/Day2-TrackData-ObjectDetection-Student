"""Kiểm thử công cụ Ngày 2 bằng nhãn giả lập (không dùng nhãn tham chiếu thật)."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC))
import day2_lab as lab  # noqa: E402

STEMS = ["drive_008", "drive_022", "drive_033", "drive_038"]
BOXES = {  # [label, x1, y1, x2, y2, occluded, truncated]
    "drive_008": [["car", 100, 100, 160, 140, False, False], ["bus", 0, 200, 120, 330, True, True]],
    "drive_022": [["van", 300, 300, 380, 360, False, False]],
    "drive_033": [["truck", 500, 50, 640, 180, False, True]],
    "drive_038": [["car", 20, 400, 70, 440, True, False], ["car", 200, 420, 250, 470, False, False]],
}


def coco_zip(path: Path, boxes=BOXES, truncated_key=True, names=lab.CLASS_NAMES) -> Path:
    cats = [{"id": i + 1, "name": n} for i, n in enumerate(names)]
    ids = {n: i + 1 for i, n in enumerate(names)}
    doc = {"images": [], "annotations": [], "categories": cats}
    ann_id = 1
    for image_id, stem in enumerate(STEMS, start=1):
        doc["images"].append({"id": image_id, "file_name": f"{stem}.jpg", "width": 640, "height": 640})
        for label, x1, y1, x2, y2, occ, trunc in boxes.get(stem, []):
            attrs = {"occluded": occ}
            if truncated_key:
                attrs["truncated"] = trunc
            doc["annotations"].append(
                {"id": ann_id, "image_id": image_id, "category_id": ids[label], "bbox": [x1, y1, x2 - x1, y2 - y1],
                 "area": (x2 - x1) * (y2 - y1), "iscrowd": 0, "attributes": attrs}
            )
            ann_id += 1
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("annotations/instances_default.json", json.dumps(doc))
    return path


def yolo_zip(path: Path, boxes=BOXES, names=lab.CLASS_NAMES) -> Path:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("data.yaml", "path: .\ntrain: train.txt\nnames:\n" + "".join(f"  {i}: {n}\n" for i, n in enumerate(names)))
        for stem in STEMS:
            lines = []
            for label, x1, y1, x2, y2, *_ in boxes.get(stem, []):
                lines.append(f"{names.index(label)} {(x1 + x2) / 1280:.6f} {(y1 + y2) / 1280:.6f} {(x2 - x1) / 640:.6f} {(y2 - y1) / 640:.6f}")
            archive.writestr(f"labels/train/{stem}.txt", "\n".join(lines))
    return path


class BoxMath(unittest.TestCase):
    def test_conversions_and_iou(self):
        self.assertEqual(lab.yolo_to_xyxy("1 0.5 0.5 0.25 0.5", 640, 640), (1, [240.0, 160.0, 400.0, 480.0]))
        self.assertEqual(lab.coco_to_xyxy([10, 20, 30, 40]), [10.0, 20.0, 40.0, 60.0])
        self.assertAlmostEqual(lab.iou([0, 0, 10, 10], [5, 0, 15, 10]), 1 / 3)
        self.assertEqual(lab.iou([0, 0, 1, 1], [2, 2, 3, 3]), 0.0)
        self.assertEqual(lab.precision_recall(8, 2, 4), (0.8, 8 / 12))


class Audit(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_matching_exports_pass(self):
        report = lab.audit(coco_zip(self.tmp / "c.zip"), yolo_zip(self.tmp / "y.zip"))
        self.assertEqual(report["status"], "pass", report["errors"])
        self.assertEqual(report["total_boxes"], 6)
        self.assertEqual(sum(r["truncated"] for r in report["per_image"]), 2)
        self.assertEqual(sum(r["occluded"] for r in report["per_image"]), 2)
        self.assertEqual(len(report["lock"]), 2)

    def test_different_annotation_state_fails(self):
        changed = {**BOXES, "drive_022": []}
        report = lab.audit(coco_zip(self.tmp / "c.zip"), yolo_zip(self.tmp / "y.zip", changed))
        self.assertEqual(report["status"], "fail")
        self.assertTrue(any("drive_022" in e for e in report["errors"]))

    def test_wrong_class_order_and_missing_truncated_fail(self):
        names = ["car", "bus", "truck", "van"]
        report = lab.audit(coco_zip(self.tmp / "c.zip", truncated_key=False), yolo_zip(self.tmp / "y.zip", names=names))
        self.assertTrue(any("Thứ tự lớp" in e for e in report["errors"]))
        self.assertTrue(any("truncated" in e for e in report["errors"]))

    def test_edge_mismatch_is_warning(self):
        boxes = {**BOXES, "drive_022": [["van", 0, 300, 80, 360, False, False]]}
        report = lab.audit(coco_zip(self.tmp / "c.zip", boxes), yolo_zip(self.tmp / "y.zip", boxes))
        self.assertEqual(report["status"], "pass")
        self.assertTrue(any("chạm mép" in w for w in report["warnings"]))

    def test_zip_slip_member_ignored(self):
        path = coco_zip(self.tmp / "c.zip")
        with zipfile.ZipFile(path, "a") as archive:
            archive.writestr("../evil.json", "{}")
        self.assertEqual(lab.load_export(path)["format"], "coco")


class Compare(unittest.TestCase):
    def test_missed_extra_loose_and_class(self):
        ref = lab.load_export(coco_zip(Path(tempfile.mkdtemp()) / "r.zip"))
        mine = json.loads(json.dumps(ref))
        mine["images"]["drive_038"].pop()                       # bỏ sót 1
        mine["images"]["drive_022"][0]["xyxy"] = [290, 290, 390, 370]  # box lỏng (IoU 0.6)
        mine["images"]["drive_033"][0]["label"] = "bus"          # sai lớp
        mine["images"]["drive_008"].append({"label": "car", "xyxy": [400, 400, 420, 420]})  # thừa
        summary, rows = lab.compare(mine, ref)
        self.assertEqual((summary["tp"], summary["fp_extra"], summary["fn_missed"]), (5, 1, 1))
        self.assertEqual(summary["precision"], round(5 / 6, 3))
        self.assertEqual(summary["recall"], round(5 / 6, 3))
        issues = " | ".join(r["issue"] for r in rows)
        for word in ("bỏ sót", "thừa", "box lỏng", "sai lớp"):
            self.assertIn(word, issues)

    def test_model_check_depends_on_labels(self):
        ref = lab.load_export(coco_zip(Path(tempfile.mkdtemp()) / "r.zip"))
        preds = {"images": {s: [{"label": b["label"], "xyxy": b["xyxy"]} for b in v] for s, v in ref["images"].items()}}
        fewer = json.loads(json.dumps(ref))
        fewer["images"]["drive_038"] = []
        self.assertEqual(lab.model_check(ref, preds)["precision"], 1.0)
        self.assertLess(lab.model_check(fewer, preds)["precision"], 1.0)

    def test_shipped_predictions_cover_all_images(self):
        preds = lab.load_predictions()
        self.assertEqual(sorted(preds["images"]), STEMS)


class RepositoryContract(unittest.TestCase):
    root = SRC.parent

    def test_images_match_manifest(self):
        import csv

        with (SRC / "data" / "image-manifest.csv").open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(sorted(r["image_id"] for r in rows), STEMS)
        for row in rows:
            self.assertEqual(lab.sha256_file(self.root / row["local_path"]), row["sha256"], row["image_id"])
        with zipfile.ZipFile(SRC / "data" / "day2-cvat-input.zip") as archive:
            for row in rows:
                data = archive.read(f"{row['image_id']}.jpg")
                self.assertEqual(lab.hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_no_reference_labels_shipped(self):
        for path in self.root.rglob("*"):
            if ".git" in path.parts:
                continue
            self.assertNotIn(path.suffix, {".txt"} if "labels" in path.parts else set(), path)
            self.assertFalse(path.name.startswith("day2-reference"), path)

    def test_skeleton_files_and_no_placeholders(self):
        for name in ("README.md", "CHECKPOINTS.md", "RUBRIC.md", "RULES.md", "SUBMISSION.md", "src/README.md",
                     "report/individual/MSSV_HoTen.md"):
            self.assertTrue((self.root / name).is_file(), name)
        for md in self.root.rglob("*.md"):
            if "report" in md.parts or ".git" in md.parts:
                continue
            self.assertNotIn("...", md.read_text(encoding="utf-8"), md)

    def test_rubric_totals_100(self):
        import re

        text = (self.root / "RUBRIC.md").read_text(encoding="utf-8")
        core = [int(m) for m in re.findall(r"^\| C\d+\b[^|]*\|\s*(\d+)\s*\|", text, re.M)]
        bonus = [int(m) for m in re.findall(r"^\| B\d+\b[^|]*\|\s*(\d+)\s*\|", text, re.M)]
        self.assertEqual(sum(core), 100)
        self.assertLessEqual(sum(bonus), 10)

    def test_learner_todo_markers_present(self):
        text = (SRC / "cp1_box_math.py").read_text(encoding="utf-8")
        self.assertEqual(text.count("# TODO CP1"), 3)


if __name__ == "__main__":
    unittest.main()
