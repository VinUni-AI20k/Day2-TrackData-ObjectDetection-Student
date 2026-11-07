# docs

Đọc khi checkpoint cần. Không phải đọc hết trước khi bắt đầu.

| Tệp | Đọc ở | Nội dung |
|---|---|---|
| [cvat-setup.md](cvat-setup.md) | trước buổi học | cài Docker + CVAT, mở `localhost:8080` |
| [concepts.md](concepts.md) | CP1, CP4 | box, YOLO vs COCO, IoU, precision, recall, ví dụ có số |
| [cvat-step-by-step.md](cvat-step-by-step.md) | CP2, CP3 | tạo project, gán nhãn, bật thuộc tính, xuất 2 định dạng |
| [label-rules.md](label-rules.md) | CP2, CP4 | 4 lớp, quy tắc box, `occluded`/`truncated`, lỗi thường gặp |
| [sources.md](sources.md) | khi cần | tài liệu gốc và phiên bản đã kiểm |

## Thuật ngữ

| Tiếng Việt | Tên trong công cụ | Nghĩa |
|---|---|---|
| box | bounding box, rectangle | hình chữ nhật bao quanh một xe |
| nhãn / lớp | label, class | `car`, `truck`, `bus`, `van` |
| bị che | `occluded` | một phần xe bị vật khác che |
| bị cắt | `truncated` | một phần xe nằm ngoài mép ảnh |
| xuất | export | lưu nhãn ra tệp COCO hoặc YOLO |
| tham chiếu | reference | nhãn mẫu của Lab Coach dùng để so |
| độ trùng | IoU | phần giao chia phần hợp của hai box, từ 0 đến 1 |
| bỏ sót / thừa | FN / FP | xe có mà không vẽ / vẽ mà không có xe |
