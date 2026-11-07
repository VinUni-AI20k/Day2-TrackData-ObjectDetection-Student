# Báo cáo Ngày 2 — Object Detection

> **Cách dùng mẫu này**
> - Đổi tên tệp thành `MSSV_HoTen.md`, ví dụ `20241234_NguyenVanAn.md`.
> - Thay mọi `...` bằng nội dung của bạn. Xóa các dòng `>` hướng dẫn trước khi nộp.
> - Mỗi mục ghi **bằng chứng** (số, tên tệp, dòng CSV, ảnh overlay), không chỉ kết luận.
> - Viết ngắn: mỗi ý 1–3 câu. Coach chấm theo [RUBRIC.md](../../RUBRIC.md), không chấm độ dài.

## 1. Thông tin học viên

- Họ và tên: ...
- MSSV: ...
- Lớp: L2 / L3
- Link repo: ...

## 2. CP1 — Box, IoU, tọa độ (C1)

> Ghi phép tính bằng tay, có số trung gian. Chép kết quả từ máy mà không có bước tính thì không đủ điểm.
>
> CP1 làm trước khi gán nhãn, nên dùng box có sẵn trong `src/data/model-predictions/yolo11n-predictions.json`
> (mọi ảnh 640×640), **không** dùng `exports/` (chỉ có sau CP3).

- Kết quả `python src/cp1_box_math.py`: 6/6 OK? ...
- Box đã chọn (ảnh, `label`, `xyxy`): ...
- `bbox` COCO tính tay `[x, y, w, h]`: ...
- Dòng YOLO tính tay `class xc yc w h` (mã lớp theo thứ tự 4 lớp của bài): ...
- Đổi ngược dòng YOLO về `[x1, y1, x2, y2]` (có số trung gian), khớp `xyxy` ban đầu không: ...
  > Ví dụ cách trình bày: `0 0.5 0.5 0.25 0.5`, ảnh 640×640 → tâm (320, 320), rộng 160, cao 320 →
  > `[240, 160, 400, 480]`.
- Một phép tính IoU viết tay giữa box trên và chính nó dịch sang phải 20 điểm ảnh (giao, hợp, kết quả): ...

## 3. CP2 — Gán nhãn (C2)

> Tình huống khó là chỗ bạn phải chọn giữa hai cách gán. Ghi đủ 4 ý: ảnh, vị trí box, bạn chọn gì, quy tắc nào
> trong `docs/label-rules.md`.

- Tổng số box: ... (`occluded`: ..., `truncated`: ...)
- Tình huống khó 1 (ảnh, vị trí, quyết định, quy tắc dùng): ...
- Tình huống khó 2: ...

## 4. CP3 — Xuất và kiểm tra (C3)

- `audit` v1: PASS / FAIL — số lần xuất lại: ...
- Lỗi/cảnh báo đã gặp và cách xử lý (ghi nguyên dòng `LỖI`/`CẢNH BÁO`, rồi bạn sửa hay giữ): ...
- Đối chiếu 1 xe: dòng YOLO trong `exports/yolo-v1.zip` và `bbox` trong `exports/coco-v1.zip`, cả hai đổi ra
  `[x1, y1, x2, y2]`: ...
- Commit khóa v1 (hash): ...
- Vì sao phải nộp cả COCO và YOLO (1–2 câu): ...

## 5. CP4 — So với tham chiếu và sửa (C4)

> Số trong bảng phải khớp `outputs/v1/compare-summary.json` và `outputs/v2/compare-summary.json`.

| Chỉ số | v1 | v2 |
|---|---:|---:|
| TP | ... | ... |
| FP (thừa) | ... | ... |
| FN (bỏ sót) | ... | ... |
| Precision | ... | ... |
| Recall | ... | ... |
| IoU trung bình | ... | ... |
| Sai lớp | ... | ... |

3 lỗi đã phân tích (mỗi lỗi truy được về một dòng trong `outputs/v1/compare-rows.csv`):

| # | Ảnh / dòng CSV | Loại lỗi | Nguyên nhân | Quy tắc liên quan | Sửa hay giữ, vì sao |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

> Giữ một box khác tham chiếu vẫn được điểm nếu bạn ghi bằng chứng (ảnh overlay, quy tắc).

## 6. CP5 — Nhãn và điểm của mô hình (C5)

| Nhãn dùng để chấm | Precision mô hình | Recall mô hình |
|---|---:|---:|
| v1 của tôi | ... | ... |
| v2 của tôi | ... | ... |
| Tham chiếu | ... | ... |

Giải thích (3–5 câu, chỉ ra ít nhất 1 box cụ thể: ảnh, vị trí, vì sao bị tính FP hoặc FN): ...

## 7. Khó khăn và cách xử lý

> Ghi sự cố kỹ thuật (CVAT, Docker, Python) theo [RULES.md](../../RULES.md): lỗi gì, lúc nào, đã làm gì, đã báo Coach
> chưa. Không có sự cố thì ghi "Không có".

| Lúc nào (CP) | Lỗi / thông báo | Đã làm gì | Kết quả |
|---|---|---|---|
| ... | ... | ... | ... |

## 8. Bonus (không bắt buộc, tối đa 10)

> Chỉ làm sau khi xong CP0–CP5. Điều kiện và cách chấm từng mục ở phần Bonus trong [RUBRIC.md](../../RUBRIC.md).
> Mục nào không làm thì xóa.

### B1 — So khớp chặt hơn ở IoU 0.75

- Lệnh đã chạy: ...
- Bảng v2 ở IoU 0.5 và 0.75 (TP, FP, FN, precision, recall): ...
- Ít nhất 1 box đổi trạng thái (ảnh, dòng CSV, IoU): ...
- Giải thích (3–5 câu): ...

### B2 — Đề xuất quy tắc gán nhãn cho một ca mơ hồ

- Ca mơ hồ (ảnh, vị trí, ảnh chụp/crop trong repo): ...
- Quy tắc hiện tại nói gì, chỗ nào chưa đủ: ...
- Quy tắc đề xuất (1 câu, làm được và kiểm được): ...
- Ví dụ đúng / ví dụ sai theo quy tắc mới: ...
- Ảnh hưởng tới số liệu nếu áp dụng (box nào đổi, precision/recall đổi ra sao): ...

### B3 — Tự chạy YOLO11n và so với dự đoán dựng sẵn

- Nơi chạy và phiên bản (`ultralytics`, ngưỡng `conf`): ...
- Lệnh hoặc link notebook: ...
- Bảng số box dự đoán mỗi ảnh (của bạn / dựng sẵn): ...
- Ít nhất 1 khác biệt và lý do có thể: ...

## 9. Công cụ AI đã dùng

> Bắt buộc điền, kể cả khi không dùng. Quy định ở mục "AI và công cụ" trong [RULES.md](../../RULES.md):
> - **Được:** hỏi khái niệm (IoU, COCO, YOLO), đọc lỗi khi chạy lệnh, sửa câu chữ báo cáo.
> - **Không được:** dùng AI hoặc tự gán nhãn của CVAT để vẽ box v1; để AI viết phần phân tích lỗi CP4 hoặc giải
>   thích CP5 thay bạn.
> - Code CP1 do AI gợi ý: bạn phải giải thích được từng dòng khi Coach hỏi.
>
> Không dùng AI: xóa bảng, giữ dòng "Tôi không dùng công cụ AI cho bài này."

| Công cụ (tên, phiên bản nếu biết) | Dùng ở CP nào | Dùng để làm gì | Tóm tắt câu hỏi/prompt | Tôi đã kiểm tra hoặc sửa gì |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

> Ví dụ một dòng hợp lệ: `ChatGPT` · CP1 · hỏi vì sao IoU ra 0 · "IoU hai box không chạm nhau bằng bao nhiêu" ·
> tự tính lại bằng tay, khớp kết quả `cp1_box_math.py`.

- [ ] Tôi xác nhận nhãn v1 do tôi tự vẽ, và phần phân tích CP4–CP5 do tôi tự viết.

## 10. Tự đánh giá

> Đối chiếu với [RUBRIC.md](../../RUBRIC.md). Coach dùng mục này để góp ý, không cộng điểm theo số bạn tự chấm.

| Tiêu chí | Đã có bằng chứng? | Chỗ còn yếu |
|---|---|---|
| C1 — CP1 | Có / Một phần / Chưa | ... |
| C2 — Nhãn v1 | Có / Một phần / Chưa | ... |
| C3 — Xuất và khóa | Có / Một phần / Chưa | ... |
| C4 — Phân tích lỗi | Có / Một phần / Chưa | ... |
| C5 — Nhãn và mô hình | Có / Một phần / Chưa | ... |
| C6 — Quy ước nộp | Có / Một phần / Chưa | ... |

## 11. Tài liệu tham khảo

> Ghi nguồn ngoài repo bạn đã dùng (trang web, bài báo, video). Chỉ dùng tài liệu trong repo thì ghi "Chỉ dùng tài
> liệu trong repo".

- ...

## Phiếu 1 phút (không chấm điểm)

- Điều rõ nhất hôm nay:
- Điều còn rối nhất:
