# Nguồn và phiên bản

Kiểm tra ngày 07/11/2026.

## Công cụ

| Chủ đề | Nguồn | Ghi chú |
|---|---|---|
| Phiên bản CVAT | <https://github.com/cvat-ai/cvat/releases> | bài ghim `v2.82.0` (05/11/2026), bản mới nhất; đã chạy thử 07/11/2026: xuất COCO 1.0 có `attributes.occluded`/`truncated`, YOLO giữ thứ tự lớp, `audit` PASS |
| CVAT COCO 1.0 | <https://docs.cvat.ai/docs/dataset_management/formats/format-coco/> | `occluded` và thuộc tính tự đặt nằm trong `annotation.attributes` |
| CVAT Ultralytics YOLO | <https://docs.cvat.ai/docs/dataset_management/formats/format-yolo-ultralytics/> | `data.yaml` (`names` dạng `0: car`) + `labels/<subset>/*.txt`; **không** xuất thuộc tính |
| Lỗi `occluded` khi xuất COCO | <https://github.com/cvat-ai/cvat/issues/9091> | đã đóng 28/03/2025; bài vẫn kiểm bằng `audit` |
| Cài CVAT | <https://docs.cvat.ai/docs/administration/community/basics/installation/> | image Docker chỉ có bản `amd64`; Mac Apple Silicon cần `DOCKER_DEFAULT_PLATFORM=linux/amd64` rồi chạy qua giả lập |
| CVAT Online (dự phòng) | <https://www.cvat.ai/pricing/cloud> | gói Free: 1 project, 3 task, 1 GB |
| Định dạng YOLO | <https://docs.ultralytics.com/datasets/detect/> | `class xc yc w h`, chuẩn hóa 0–1 |
| IoU, precision, recall, mAP | <https://docs.ultralytics.com/guides/yolo-performance-metrics/> | định nghĩa chỉ số |
| Định dạng COCO | <https://cocodataset.org/#format-data> | `bbox = [x, y, width, height]` |
| Dự đoán dựng sẵn | <https://pypi.org/project/ultralytics/8.4.145/> | `yolo11n.pt`, `conf 0.25`, `imgsz 640`. Bản mới nhất là `8.4.204` và mô hình mới nhất là YOLO26; bài không huấn luyện nên không cần đổi |

## Định nghĩa thuộc tính

| Bộ dữ liệu | Nguồn | Cách định nghĩa |
|---|---|---|
| KITTI | <https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d> (devkit `readme.txt`) | `truncated` 0–1 (mức vật ra khỏi mép ảnh); `occluded` 0–3 (thấy hết / che một phần / che nhiều / không rõ) |
| Open Images V7 | <https://storage.googleapis.com/openimages/web/download_v7.html> | `IsOccluded`: bị vật khác che; `IsTruncated`: vượt ra ngoài mép ảnh; box sát vật |
| BDD100K | <https://github.com/bdd100k/bdd100k/blob/master/doc/source/format.rst> | `occluded`, `truncated` là đúng/sai |

## Lỗi nhãn và ảnh hưởng lên mô hình

| Nguồn | Dùng cho |
|---|---|
| Bolya và cộng sự, *TIDE*, ECCV 2020 — <https://arxiv.org/abs/2008.08115> | cách chia lỗi: sai lớp, sai vị trí, trùng, nhận nhầm nền, bỏ sót |
| Wang và cộng sự, *Co-mining*, AAAI 2021 — <https://arxiv.org/abs/2012.01950> | xe không được gán nhãn bị coi là nền, làm mô hình học sai |
| Tkachenko và cộng sự, *ObjectLab*, 2023 — <https://arxiv.org/abs/2309.00832> | tìm box bị bỏ sót, box lệch, sai lớp trong bộ dữ liệu thật như COCO |
| *Universal Noise Annotation*, 2023 — <https://arxiv.org/abs/2312.13822> | 4 loại nhiễu nhãn: lệch vị trí, bỏ sót, box thừa, sai lớp |
