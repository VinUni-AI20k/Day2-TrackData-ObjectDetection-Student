# Nguồn và phiên bản

Kiểm tra ngày 07/11/2026.

| Chủ đề | Nguồn | Ghi chú |
|---|---|---|
| CVAT COCO 1.0 | <https://docs.cvat.ai/docs/dataset_management/formats/format-coco/> | `occluded` và thuộc tính tự đặt nằm trong `annotation.attributes` |
| CVAT Ultralytics YOLO | <https://docs.cvat.ai/docs/dataset_management/formats/format-yolo-ultralytics/> | `data.yaml` + `labels/<subset>/*.txt`; không xuất thuộc tính |
| Lỗi `occluded` khi xuất COCO | <https://github.com/cvat-ai/cvat/issues/9091> | đã đóng 28/03/2025; bài vẫn kiểm bằng `audit` |
| Phiên bản CVAT | <https://github.com/cvat-ai/cvat/releases> | mới nhất `v2.82.0`; bài dùng `v2.74.1` đã chạy thử |
| Định dạng YOLO | <https://docs.ultralytics.com/datasets/detect/> | `class xc yc w h`, chuẩn hóa 0–1 |
| IoU, precision, recall, mAP | <https://docs.ultralytics.com/guides/yolo-performance-metrics/> | định nghĩa chỉ số |
| Định dạng COCO | <https://cocodataset.org/#format-data> | `bbox = [x, y, width, height]` |
| Ultralytics (dự đoán dựng sẵn) | <https://pypi.org/project/ultralytics/8.4.145/> | `yolo11n.pt`, `conf 0.25`, `imgsz 640` |
