"""CP1 — tự viết 3 phép tính hộp. Chạy: python src/cp1_box_math.py

Mỗi hàm chỉ cần 2–5 dòng. Không import day2_lab trong phần bạn viết.
Khi cả 6 dòng tự kiểm tra in "OK", chép kết quả vào báo cáo (mục CP1).
"""

from __future__ import annotations


def yolo_line_to_pixels(line: str, width: int, height: int) -> list[float]:
    """'class xc yc w h' (chuẩn hóa 0..1) -> [x1, y1, x2, y2] theo điểm ảnh."""
    # TODO CP1: tách 5 số; nhân xc, w với width; yc, h với height; x1 = xc - w/2 ...
    raise NotImplementedError("TODO CP1: yolo_line_to_pixels")


def coco_bbox_to_pixels(bbox: list[float]) -> list[float]:
    """COCO [x, y, w, h] (góc trên-trái, điểm ảnh) -> [x1, y1, x2, y2]."""
    # TODO CP1: x2 = x + w, y2 = y + h
    raise NotImplementedError("TODO CP1: coco_bbox_to_pixels")


def box_iou(a: list[float], b: list[float]) -> float:
    """IoU = diện tích giao / diện tích hợp của hai hộp [x1, y1, x2, y2]."""
    # TODO CP1: giao = max(0, min(x2) - max(x1)) * max(0, min(y2) - max(y1)); hợp = A + B - giao
    raise NotImplementedError("TODO CP1: box_iou")


def _check() -> int:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import day2_lab as ref

    cases = [
        ("YOLO giữa ảnh", lambda f: f("0 0.5 0.5 0.25 0.125", 640, 640), lambda: ref.yolo_to_xyxy("0 0.5 0.5 0.25 0.125", 640, 640)[1], yolo_line_to_pixels),
        ("YOLO ảnh chữ nhật", lambda f: f("2 0.1 0.9 0.2 0.2", 1280, 720), lambda: ref.yolo_to_xyxy("2 0.1 0.9 0.2 0.2", 1280, 720)[1], yolo_line_to_pixels),
        ("COCO", lambda f: f([100, 50, 40, 30]), lambda: ref.coco_to_xyxy([100, 50, 40, 30]), coco_bbox_to_pixels),
        ("IoU trùng khít", lambda f: f([0, 0, 10, 10], [0, 0, 10, 10]), lambda: 1.0, box_iou),
        ("IoU lệch nửa", lambda f: f([0, 0, 10, 10], [5, 0, 15, 10]), lambda: ref.iou([0, 0, 10, 10], [5, 0, 15, 10]), box_iou),
        ("IoU không chạm", lambda f: f([0, 0, 10, 10], [20, 20, 30, 30]), lambda: 0.0, box_iou),
    ]
    failed = 0
    for name, call, expected, func in cases:
        try:
            got, want = call(func), expected()
            ok = all(abs(g - w) < 1e-6 for g, w in zip(got, want)) if isinstance(want, list) else abs(got - want) < 1e-6
        except NotImplementedError as error:
            got, want, ok = str(error), expected(), False
        failed += not ok
        print(f"{'OK  ' if ok else 'SAI '} {name}: nhận {got}, cần {want}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_check())
