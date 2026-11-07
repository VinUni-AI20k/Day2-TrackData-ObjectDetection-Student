# Ngày 2 — Gán nhãn phát hiện vật thể: box, thuộc tính, COCO/YOLO

> **Bài cá nhân** · 4 giờ trên lớp · Deadline mặc định **23:59 GMT+7 ngày lab** (chi tiết: [SUBMISSION.md](SUBMISSION.md))

Bạn gán nhãn 4 ảnh giao thông trong CVAT, xuất ra **COCO** và **YOLO**, kiểm tra bản xuất, rồi so với nhãn tham chiếu
bằng **IoU, precision, recall**. Cuối bài, bạn thấy cùng một mô hình bị chấm điểm khác đi khi nhãn khác đi — vì vậy
nhãn nộp cho mô hình phải đúng và đúng định dạng.

## Mục tiêu

Sau bài, bạn có thể:

1. Tính IoU và đổi tọa độ YOLO `xc yc w h` / COCO `[x, y, w, h]` sang điểm ảnh.
2. Vẽ box sát phần nhìn thấy, đúng 1 trong 4 lớp `car, truck, bus, van`, gắn đúng `occluded` / `truncated`.
3. Xuất COCO 1.0 + Ultralytics YOLO và chứng minh hai bản cùng một trạng thái nhãn.
4. Đọc precision/recall để tìm lỗi **bỏ sót**, **box thừa**, **box lỏng**, **sai lớp**, rồi sửa có minh chứng.
5. Giải thích vì sao nhãn sai làm sai điểm của mô hình.

## Chuẩn bị trước buổi học

- CVAT chạy được tại `http://localhost:8080` — làm theo [docs/cvat-setup.md](docs/cvat-setup.md).
- Python 3.10+ với `pip install -r src/requirements.txt` (hoặc dùng Google Colab, xem [src/README.md](src/README.md)).
- Một repo GitHub cá nhân để nộp bài, đặt tên theo [SUBMISSION.md](SUBMISSION.md).

## Đọc theo thứ tự

1. [RULES.md](RULES.md) — quy định, dùng AI, nộp muộn
2. [CHECKPOINTS.md](CHECKPOINTS.md) — 5 bước làm bài
3. [src/README.md](src/README.md) — lệnh chạy và tệp được sửa
4. [RUBRIC.md](RUBRIC.md) — cách chấm
5. [SUBMISSION.md](SUBMISSION.md) — nộp gì, ở đâu

Hướng dẫn chi tiết từng thao tác nằm trong [docs/](docs/README.md).

## Cấu trúc

```text
README.md  RULES.md  CHECKPOINTS.md  RUBRIC.md  SUBMISSION.md
src/       mã kiểm tra, ảnh, dự đoán mô hình dựng sẵn, bài CP1
docs/      hướng dẫn CVAT, quy tắc gán nhãn, kiến thức box/IoU/COCO/YOLO
report/individual/MSSV_HoTen.md   mẫu báo cáo — đổi tên thành MSSV_HoTen của bạn
```
