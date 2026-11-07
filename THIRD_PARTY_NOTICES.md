# Thông báo về dữ liệu và phần mềm bên thứ ba

Tài liệu này ghi nhận nguồn dùng cho mục đích giảng dạy; không phải tư vấn pháp lý.

## Bốn ảnh giao thông

Bốn ảnh được lấy nguyên vẹn từ kho nguồn của giảng viên tại phiên bản
[`710d2c1`](https://github.com/VinUni-AI20k/Day2-TrackData-ObjectDetection/tree/710d2c157c5750f71271354d0d31b24457c64e7c).
Kho nguồn cho biết ảnh bắt nguồn từ UA-DETRAC thông qua bản tái xuất `SQiFeng/traffic-vehicle-detection`, với thẻ
dữ liệu từng công bố giấy phép CC BY 4.0. Tuy nhiên, kho nguồn đã đổi tên ảnh, không giữ mã bản ghi gốc và liên kết
bản tái xuất hiện không còn truy cập được. Đây là giới hạn truy nguyên đã biết; mã SHA-256 chỉ chứng minh ảnh trong
kho học viên khớp kho nguồn, không chứng minh toàn bộ chuỗi quyền sử dụng.

- Trang mô tả bản tái xuất: `https://huggingface.co/datasets/SQiFeng/traffic-vehicle-detection` (không còn truy
  cập được tại thời điểm kiểm tra ngày 13/09/2026)
- [Giấy phép Creative Commons Ghi công 4.0](https://creativecommons.org/licenses/by/4.0/)
- [Bài báo UA-DETRAC](https://faculty.ucmerced.edu/mhyang/papers/cviu2020_detrac.pdf)

ZIP dành cho học viên chỉ chứa ảnh, không chứa nhãn tham chiếu. Nhãn, ảnh phủ hộp và ảnh dự đoán do học viên tạo
phải được sử dụng theo quy định của lớp.

## Ultralytics

`src/data/model-predictions/yolo11n-predictions.json` là kết quả chạy sẵn `yolo11n.pt` với `ultralytics==8.4.145`
trên bốn ảnh. Kho chỉ chứa tọa độ hộp và điểm tin cậy, không chứa trọng số mô hình. Ultralytics công bố phần mềm và
mô hình cộng đồng theo AGPL-3.0, đồng thời có điều khoản doanh nghiệp. Kho mã giảng dạy này không cấp thêm quyền
triển khai mô hình với dữ liệu sở hữu riêng.

- [Mã nguồn Ultralytics](https://github.com/ultralytics/ultralytics)
- [Thông tin giấy phép Ultralytics](https://www.ultralytics.com/license)
- [Gói Ultralytics 8.4.145](https://pypi.org/project/ultralytics/8.4.145/)

## Phạm vi phát hành

Kho mã chưa có giấy phép tổng thể và đang để riêng tư. Không phát hành rộng kho mã, ảnh, nhãn đã tạo hoặc kết quả
mô hình trước khi chủ sở hữu chương trình xác nhận quyền phân phối. Không đưa nhãn tham chiếu, trọng
số mô hình, mật khẩu hoặc mã truy cập vào bài nộp. Bài nộp chỉ gồm bản xuất nhãn của chính học viên (không kèm ảnh).
