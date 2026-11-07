# Rubric

Điểm chính 100. Bonus ghi riêng, tối đa 10. Mỗi tiêu chí chấm theo bằng chứng có trong repo nộp.

| Tiêu chí | Điểm | Bằng chứng | Mất điểm khi |
|---|---:|---|---|
| C1 — Box, IoU, tọa độ (CP1) | 15 | `src/cp1_box_math.py` chạy ra 6 dòng `OK`; mục CP1 trong báo cáo có phép tính tay | hàm còn `TODO`; phép tính tay sai hoặc chép từ máy mà không giải thích |
| C2 — Chất lượng nhãn v1 (CP2) | 25 | `exports/coco-v1.zip`; overlay v1; mục CP2 trong báo cáo | thiếu ảnh; dùng lớp ngoài 4 lớp; box gộp nhiều xe; nhiều box lỏng hoặc bỏ sót xe nhìn rõ; `occluded`/`truncated` gắn tùy tiện |
| C3 — Xuất đúng định dạng và khóa bài (CP3) | 20 | `exports/coco-v1.zip`, `exports/yolo-v1.zip`, `outputs/v1/audit.json` = `pass`; commit v1 trước giờ phát tham chiếu | thiếu một định dạng; audit `fail`; hai bản xuất khác trạng thái; sửa v1 sau khi nhận tham chiếu |
| C4 — Phân tích lỗi và sửa (CP4) | 25 | `outputs/v1/`, `outputs/v2/`; bảng trước/sau và 3 lỗi có nguyên nhân + quy tắc | chỉ chép số; lỗi không truy được về dòng trong `compare-rows.csv`; sửa cho khớp tham chiếu mà không lý giải |
| C5 — Nhãn ảnh hưởng mô hình (CP5) | 10 | bảng `model-check` 3 dòng + giải thích trong báo cáo | không chỉ ra được box cụ thể; kết luận "mô hình tệ/tốt" mà bỏ qua nhãn |
| C6 — Đúng quy ước nộp bài | 5 | tên repo, tên báo cáo, cấu trúc theo `SUBMISSION.md` | sai tên; thiếu tệp; commit secret hoặc dữ liệu ngoài bài |
| **Tổng điểm chính** | **100** | | |

## Bonus (tối đa 10)

| Tiêu chí | Điểm | Bằng chứng |
|---|---:|---|
| B1 — Chạy lại `compare` ở `--iou 0.75`, giải thích vì sao precision/recall đổi | 4 | `outputs/v2-iou075/` + 3–5 câu |
| B2 — Đề xuất 1 quy tắc gán nhãn mới cho một ca mơ hồ, có ảnh minh họa và lý do | 3 | mục Bonus trong báo cáo |
| B3 — Tự chạy YOLO11n trên 4 ảnh (Colab/máy) và so với dự đoán dựng sẵn | 3 | notebook/lệnh + bảng so sánh |

## Quy tắc chấm

- Precision/recall của bạn **không** quy đổi thẳng ra điểm. Coach chấm cách bạn đọc và sửa lỗi.
- Không có điểm cho việc khớp tham chiếu 100%. Giữ một quyết định khác tham chiếu vẫn được điểm nếu có bằng chứng.
- Nộp muộn bị trừ theo `RULES.md`.
