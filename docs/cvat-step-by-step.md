# CVAT từng bước (CP2–CP3)

Bài dùng CVAT `v2.82.0`. Ảnh chụp lấy từ `v2.74.1`; tên nút giữ nguyên, vị trí có thể hơi khác.

## 1. Tạo project và nhãn

1. **Projects → + → Create a new project**, tên `day2-od`.
2. Mở tab **Raw** của Labels, xóa nội dung, dán đoạn dưới rồi **Done → Submit & Open**:

```json
[
  {"name": "car",   "type": "rectangle", "attributes": [{"name": "truncated", "input_type": "checkbox", "mutable": false, "values": ["false"], "default_value": "false"}]},
  {"name": "truck", "type": "rectangle", "attributes": [{"name": "truncated", "input_type": "checkbox", "mutable": false, "values": ["false"], "default_value": "false"}]},
  {"name": "bus",   "type": "rectangle", "attributes": [{"name": "truncated", "input_type": "checkbox", "mutable": false, "values": ["false"], "default_value": "false"}]},
  {"name": "van",   "type": "rectangle", "attributes": [{"name": "truncated", "input_type": "checkbox", "mutable": false, "values": ["false"], "default_value": "false"}]}
]
```

Thứ tự `car, truck, bus, van` quyết định mã lớp YOLO `0, 1, 2, 3`. Không đổi thứ tự.
`occluded` là cờ có sẵn của mọi box trong CVAT nên không cần khai báo.

Kết quả: tab **Constructor** hiện 4 nhãn theo đúng thứ tự `car, truck, bus, van`.

## 2. Tạo task

1. Trong project: **+ → Create a new task**, tên `day2-v1`.
2. **Select files → My computer** → chọn `src/data/day2-cvat-input.zip` → **Submit & Open**.
3. Mở **Job #1**. Kiểm tra có đủ 4 ảnh.

![Tạo task và tải ảnh](assets/day2-e2e/cvat-task-upload-real.png)

## 3. Vẽ box và đặt thuộc tính

1. Chọn công cụ **Draw new rectangle** (phím `N`), chọn nhãn, kéo box sát xe.
2. Ở danh sách **Objects** bên phải:
   - bấm biểu tượng **occluded** khi xe bị che;
   - tích **truncated** khi xe bị mép ảnh cắt.
3. Sửa box: kéo các điểm góc; đổi nhãn bằng menu nhãn của object.
4. Lưu thường xuyên: **Save** (`Ctrl+S`). Chuyển ảnh bằng `F` / `D`.

![Vẽ và lưu box](assets/day2-e2e/cvat-rectangle-save-real.png)

## 4. Xuất 2 định dạng từ cùng một task (CP3)

Lưu trước khi xuất. Từ trang task: **Actions → Export task dataset**.

| Lần | Export format | Save images | Đổi tên tệp tải về thành |
|---|---|---|---|
| 1 | `COCO 1.0` | tắt | `exports/coco-v1.zip` |
| 2 | `Ultralytics YOLO Detection 1.0` | tắt | `exports/yolo-v1.zip` |

![Hộp thoại xuất dữ liệu](assets/day2-e2e/cvat-export-controls-real.png)

Kết quả: thư mục `exports/` có `coco-v1.zip` và `yolo-v1.zip`.

Nếu không thấy tệp tải về: vào **Requests** (thanh trên) và bấm tải.
Sau đó chạy `audit` theo [src/README.md](../src/README.md).

## 5. Sửa thành v2 (CP4)

Sửa ngay trong task `day2-v1` (bản v1 đã được khóa bằng commit), lưu, rồi xuất lại thành `exports/coco-v2.zip` và
`exports/yolo-v2.zip`.

## Sự cố thường gặp

| Hiện tượng | Cách xử lý |
|---|---|
| `audit`: thứ tự lớp sai | project có nhãn sai thứ tự → sửa tab Raw, xuất lại |
| `audit`: thiếu `truncated` | nhãn chưa có thuộc tính → thêm theo bước 1, kiểm lại từng box |
| `audit`: COCO và YOLO khác nhau | hai bản xuất ở hai thời điểm khác nhau → lưu rồi xuất lại cả hai |
| Không mở được `localhost:8080` | xem [cvat-setup.md](cvat-setup.md) |
