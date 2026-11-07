# Checkpoints

Tổng 240 phút. Làm theo thứ tự; mỗi checkpoint có sản phẩm riêng trong repo nộp bài.

| CP | Nội dung | Phút |
| --- | --- | ---: |
| CP0 | Mở CVAT, tạo repo nộp bài, cài thư viện | 15 |
| CP1 | Box, IoU, tọa độ COCO/YOLO | 30 |
| CP2 | Gán nhãn 4 ảnh trong CVAT | 75 |
| CP3 | Xuất COCO + YOLO, kiểm tra, khóa bài | 30 |
| CP4 | So với tham chiếu, đọc precision/recall, sửa lỗi | 60 |
| CP5 | Nhãn ảnh hưởng điểm của mô hình thế nào | 30 |

## CP1 — Box, IoU, tọa độ

- **Mục tiêu:** đọc được một box ở cả hai định dạng và tính được độ trùng giữa hai box.
- **Cần làm:** đọc [docs/concepts.md](docs/concepts.md); điền 3 hàm `TODO CP1` trong `src/cp1_box_math.py`;
  chạy `python src/cp1_box_math.py`.
- **Sản phẩm:** `src/cp1_box_math.py` đã điền; mục CP1 trong báo cáo: chọn **1 box** trong
  `src/data/model-predictions/yolo11n-predictions.json` (ảnh 640×640, tọa độ `xyxy`), tính tay ra `bbox` COCO và
  dòng YOLO, đổi dòng YOLO ngược về `[x1, y1, x2, y2]`; 1 phép tính IoU viết tay.
- **Lưu ý:** CP1 **chưa cần** `exports/` — tệp xuất chỉ có sau CP3. Phép đối chiếu YOLO ↔ COCO trên nhãn của chính
  bạn làm ở bước tự kiểm tra của CP3.
- **Cần hiểu:** YOLO chuẩn hóa theo kích thước ảnh và lấy **tâm**; COCO dùng điểm ảnh và lấy **góc trên-trái**.
- **Tự kiểm tra:** cả 6 dòng in `OK`; đổi ngược dòng YOLO tính tay ra đúng `xyxy` ban đầu (sai số làm tròn ≤ 1 điểm
  ảnh).

## CP2 — Gán nhãn trong CVAT

- **Mục tiêu:** nhãn đúng quy tắc, có thể dùng làm dữ liệu cho mô hình.
- **Cần làm:** tạo project theo [docs/cvat-step-by-step.md](docs/cvat-step-by-step.md) (4 lớp, thuộc tính
  `truncated`); gán nhãn đủ 4 ảnh theo [docs/label-rules.md](docs/label-rules.md); bật `occluded` khi xe bị che,
  tích `truncated` khi xe bị mép ảnh cắt. Làm **độc lập**, không xem bài người khác.
- **Sản phẩm:** task CVAT đã lưu; mục CP2 trong báo cáo (2 tình huống khó và quyết định của bạn).
- **Cần hiểu:** box sát phần **nhìn thấy**; không đoán phần bị che; một xe = một box.
- **Tự kiểm tra:** đi lại từng ảnh ở mức phóng 100%; không còn xe nhìn rõ mà chưa có box.

## CP3 — Xuất và kiểm tra

- **Mục tiêu:** nộp được bản xuất mà máy đọc đúng.
- **Cần làm:** xuất **COCO 1.0** và **Ultralytics YOLO Detection** (không kèm ảnh) từ cùng task, lưu vào
  `exports/coco-v1.zip`, `exports/yolo-v1.zip`; chạy lệnh `audit` trong [src/README.md](src/README.md); sửa trong
  CVAT và xuất lại tới khi `PASS`. **Commit + push** trước khi nhận nhãn tham chiếu.
- **Sản phẩm:** 2 tệp ZIP, `outputs/v1/audit.json`, commit "lock v1".
- **Cần hiểu:** YOLO **bỏ mất** thuộc tính; COCO giữ `occluded`, `truncated` trong `attributes`. Vì vậy nộp cả hai.
- **Tự kiểm tra:** `audit` in `PASS`; đọc hết mọi dòng `CẢNH BÁO` và quyết định có sửa hay không; lấy 1 xe, đổi
  dòng YOLO trong `yolo-v1.zip` và `bbox` trong `coco-v1.zip` ra `[x1, y1, x2, y2]` (dùng hàm CP1) — hai kết quả
  phải gần như trùng.

## CP4 — So với tham chiếu và sửa

- **Mục tiêu:** dùng precision/recall để tìm và sửa lỗi nhãn của chính mình.
- **Cần làm:** nhận `day2-reference.zip` từ Lab Coach (chỉ phát sau khi bạn đã push CP3); chạy `compare` và
  `overlay`; chọn **3 lỗi** trong `compare-rows.csv` (bỏ sót, box lỏng, sai lớp, thừa); với mỗi lỗi: nguyên nhân, quy
  tắc liên quan, bạn sửa hay giữ và vì sao. Sửa trong CVAT, xuất `*-v2.zip`, chạy lại `audit` + `compare`.
- **Sản phẩm:** `outputs/v1/` và `outputs/v2/`; bảng trước/sau trong báo cáo.
- **Cần hiểu:** coi tham chiếu là đúng thì **recall thấp = bạn bỏ sót**, **precision thấp = bạn vẽ thừa**; box lỏng
  vẫn được tính đúng ở IoU 0.5 nhưng bị đánh dấu khi IoU < 0.75. Tham chiếu cũng có thể sai — nếu bạn giữ quyết định,
  hãy ghi bằng chứng.
- **Tự kiểm tra:** số trong báo cáo khớp `compare-summary.json`; không sửa box chỉ để "khớp" khi không đồng ý với
  tham chiếu.

## CP5 — Nhãn và điểm của mô hình

- **Mục tiêu:** thấy rằng điểm của mô hình phụ thuộc vào nhãn dùng để chấm.
- **Cần làm:** chạy `model-check` với nhãn v1, v2 và tham chiếu (dự đoán YOLO11n đã dựng sẵn trong `src/data/`).
- **Sản phẩm:** bảng 3 dòng precision/recall của **cùng một mô hình** trong báo cáo + 3–5 câu giải thích.
- **Cần hiểu:** mô hình không đổi, chỉ nhãn đổi. Nhãn bỏ sót làm dự đoán đúng bị tính là "thừa"; nếu đem nhãn đó đi
  huấn luyện, mô hình học rằng chiếc xe ấy là nền.
- **Tự kiểm tra:** giải thích được ít nhất một box mô hình bị tính FP nhưng thực ra là xe bạn bỏ sót (xem overlay).
