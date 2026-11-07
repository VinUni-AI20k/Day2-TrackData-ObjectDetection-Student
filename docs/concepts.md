# Kiến thức cần cho bài

## 1. Box và hai định dạng

Box là hình chữ nhật bao quanh vật thể. Công cụ trong bài dùng dạng chung `[x1, y1, x2, y2]` (góc trên-trái,
góc dưới-phải, đơn vị điểm ảnh).

| Định dạng | Một box ghi là | Đơn vị | Gốc tọa độ |
|---|---|---|---|
| YOLO (`labels/*.txt`) | `class xc yc w h` | chuẩn hóa 0–1 theo rộng/cao ảnh | **tâm** box |
| COCO (`instances_*.json`) | `"bbox": [x, y, w, h]` | điểm ảnh | **góc trên-trái** |

Ví dụ ảnh 640×640, xe `car` (lớp 0) từ (100, 200) đến (300, 300):

- COCO: `[100, 200, 200, 100]`
- YOLO: `0 0.3125 0.390625 0.3125 0.15625` vì `xc = 200/640`, `yc = 250/640`, `w = 200/640`, `h = 100/640`

| Khác biệt quan trọng | YOLO | COCO |
|---|---|---|
| Tên lớp | `data.yaml` → `names: {0: car, 1: truck, …}`; **thứ tự = mã lớp** | `categories` có `id` + `name` |
| Thuộc tính `occluded`, `truncated` | **mất** khi xuất | giữ trong `annotation.attributes` |
| Ảnh không có xe | tệp `.txt` rỗng | ảnh có trong `images`, không có annotation |

Sai thứ tự lớp trong YOLO không báo lỗi: mô hình chỉ học nhầm `truck` thành `bus`. Vì vậy `audit` kiểm thứ tự lớp.

## 2. IoU

IoU (Intersection over Union) = diện tích phần giao / diện tích phần hợp của hai box.

Ví dụ A = `[0, 0, 10, 10]`, B = `[5, 0, 15, 10]`: giao = 5 × 10 = 50; hợp = 100 + 100 − 50 = 150;
IoU = 50 / 150 ≈ **0.33**.

- IoU = 1: trùng khít. IoU = 0: không chạm.
- Bài dùng IoU ≥ **0.5** để coi hai box là cùng một xe (ngưỡng phổ biến, như mAP50).
- Box khớp nhưng IoU < **0.75** bị đánh dấu để xem lại: `box lỏng` nếu box của bạn to hơn, `box chật/lệch` nếu nhỏ
  hơn hoặc lệch. Đây là gợi ý để xem lại, không phải chuẩn chấm.

## 3. Precision và recall

So box của bạn với tham chiếu, ghép từng cặp theo IoU cao nhất:

| Kết quả | Nghĩa trong bài |
|---|---|
| TP | box của bạn khớp một box tham chiếu |
| FP | box của bạn không khớp box nào → **thừa** |
| FN | box tham chiếu không có box nào của bạn khớp → **bỏ sót** |

- precision = TP / (TP + FP): trong số box bạn vẽ, bao nhiêu là đúng.
- recall = TP / (TP + FN): trong số xe cần gán, bạn tìm được bao nhiêu.

Ví dụ: tham chiếu 50 xe, bạn vẽ 38 box, 30 khớp → TP 30, FP 8, FN 20; precision = 30/38 ≈ 0.79,
recall = 30/50 = 0.60. Recall thấp → đi tìm xe bỏ sót trước.

Sai lớp được báo riêng (`class_agreement_on_matches`): box vẫn khớp vị trí nhưng lớp khác.

## 4. Vì sao nhãn ảnh hưởng mô hình

Khi chấm mô hình, nhãn là "đáp án". Nếu đáp án thiếu một xe, mô hình phát hiện đúng xe đó vẫn bị tính **FP**.
Nếu đem nhãn đó đi huấn luyện, mô hình bị dạy rằng chỗ đó là nền (Co-mining, AAAI 2021). Box lỏng dạy mô hình vẽ box
lỏng và làm giảm điểm ở ngưỡng IoU cao (mAP50-95). CP5 cho bạn thấy điều này bằng số.

Tên lỗi trong bài gần với cách chia lỗi của TIDE (ECCV 2020), công cụ phân tích lỗi của mô hình phát hiện vật thể:

| Trong bài | Trong TIDE | Ghi chú |
|---|---|---|
| bỏ sót (FN) | Miss | |
| thừa (FP) | Background / Duplicate | vẽ chỗ không có xe, hoặc 2 box cho 1 xe |
| sai lớp | Classification | |
| box lỏng, box chật/lệch | không có | quy ước riêng của bài: khớp ở IoU 0.5 nhưng IoU < 0.75. TIDE gọi "Localization" cho IoU 0.1–0.5, tức là box lệch tới mức không còn được tính là khớp |

Nguồn: [sources.md](sources.md#lỗi-nhãn-và-ảnh-hưởng-lên-mô-hình).
