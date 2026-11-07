# Rules

## AI và công cụ

- Được dùng AI để hỏi khái niệm (IoU, COCO, YOLO), đọc lỗi khi chạy lệnh và sửa câu chữ báo cáo.
- **Không** dùng AI hoặc mô hình tự động để vẽ box thay bạn (kể cả tính năng tự gán nhãn của CVAT). Nhãn v1 phải do
  bạn tự vẽ.
- Phần CP1 tự viết. Nếu AI gợi ý code, bạn phải giải thích được từng dòng khi Coach hỏi.
- Ghi công cụ AI đã dùng vào mục cuối báo cáo.

## Làm bài và liêm chính

- Bài cá nhân. Không xem hoặc chép nhãn của người khác trước khi bạn đã push CP3.
- Không sửa nhãn v1 sau khi nhận tham chiếu. Mọi sửa đổi đi vào v2.
- Không chia sẻ `day2-reference.zip` ra ngoài lớp và không commit nó vào repo.
- Ghi nguồn khi dùng tài liệu ngoài.

## Dữ liệu, secret và API key

- Chỉ dùng 4 ảnh trong `src/data/`. Không đưa ảnh cá nhân, dữ liệu doanh nghiệp hay dữ liệu khách hàng vào repo.
- Không commit mật khẩu CVAT, token GitHub, API key hoặc tệp `.env`.

## Nộp muộn, sửa bài và lỗi kỹ thuật

- Deadline theo `SUBMISSION.md`. Nộp muộn bị trừ điểm theo thông báo của Key Coach.
- Commit sau deadline không được chấm, trừ khi Coach đã đồng ý gia hạn.
- Nếu CVAT hoặc máy lỗi: ghi lỗi, ảnh chụp màn hình và thời điểm vào báo cáo, báo Coach ngay trong buổi học.
