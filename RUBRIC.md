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

Bonus đào sâu đúng kỹ năng của bài: đọc chỉ số, viết quy tắc gán nhãn, kiểm mô hình. Chỉ chấm khi C1–C5 đã có bằng
chứng. Bonus không bù cho phần chính còn thiếu. Ghi bài làm ở mục Bonus trong báo cáo.

| Tiêu chí | Điểm | Bằng chứng |
|---|---:|---|
| B1 — Chạy lại `compare` ở `--iou 0.75`, giải thích vì sao precision/recall đổi | 4 | `outputs/v2-iou075/` + mục B1 trong báo cáo |
| B2 — Đề xuất 1 quy tắc gán nhãn mới cho một ca mơ hồ, có ảnh minh họa và lý do | 3 | mục B2 trong báo cáo + ảnh crop trong repo |
| B3 — Tự chạy YOLO11n trên 4 ảnh (Colab/máy) và so với dự đoán dựng sẵn | 3 | lệnh/notebook + bảng so sánh trong mục B3 |

### Làm gì để được điểm

**B1 (4 điểm).** Chạy:

```bash
python src/day2_lab.py compare --mine exports/coco-v2.zip --reference day2-reference.zip --out outputs/v2-iou075 --iou 0.75
```

| Mức | Điều kiện |
|---|---|
| Đủ 4 | Bảng v2 ở IoU 0.5 và 0.75; chỉ ra ít nhất 1 box đổi từ TP sang FP + FN (ảnh, dòng CSV, IoU); 3–5 câu giải thích vì sao box lỏng bị loại ở ngưỡng chặt hơn |
| 2 | Có bảng và giải thích chung, chưa chỉ ra box cụ thể |
| 0 | Chỉ chép số, hoặc thiếu `outputs/v2-iou075/` |

**B2 (3 điểm).** Chọn một ca mà `docs/label-rules.md` chưa nói rõ (ví dụ xe bị che quá nửa, xe xa chỉ vài điểm
ảnh, xe tải nhỏ khó phân biệt với `van`).

| Mức | Điều kiện |
|---|---|
| Đủ 3 | Ảnh crop của ca đó; quy tắc mới viết thành 1 câu kiểm được; 1 ví dụ đúng và 1 ví dụ sai; nói box nào trong bài sẽ đổi nếu áp dụng |
| 1–2 | Có quy tắc và lý do nhưng thiếu ảnh hoặc thiếu ví dụ |
| 0 | Chỉ lặp lại quy tắc đã có, hoặc quy tắc không kiểm được ("vẽ cho hợp lý") |

**B3 (3 điểm).** Cần cài `ultralytics` và tải trọng số YOLO11n. Không commit tệp `.pt` hoặc thư mục `runs/`.

| Mức | Điều kiện |
|---|---|
| Đủ 3 | Lệnh hoặc link notebook chạy lại được; ghi phiên bản `ultralytics` và ngưỡng `conf`; bảng số box mỗi ảnh (của bạn / dựng sẵn); giải thích ít nhất 1 khác biệt |
| 1–2 | Chạy được nhưng thiếu bảng so sánh hoặc thiếu giải thích |
| 0 | Không có lệnh/notebook để chạy lại |

## Quy tắc chấm

- Precision/recall của bạn **không** quy đổi thẳng ra điểm. Coach chấm cách bạn đọc và sửa lỗi.
- Không có điểm cho việc khớp tham chiếu 100%. Giữ một quyết định khác tham chiếu vẫn được điểm nếu có bằng chứng.
- Nộp muộn bị trừ theo `RULES.md`.
