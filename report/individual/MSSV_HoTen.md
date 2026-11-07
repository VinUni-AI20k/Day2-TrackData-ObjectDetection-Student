# Báo cáo Ngày 2 — Object Detection

- Họ và tên: ...
- MSSV: ...
- Lớp: L2 / L3
- Link repo: ...

## CP1 — Box, IoU, tọa độ

- Kết quả `python src/cp1_box_math.py`: 6/6 OK? ...
- Một dòng YOLO lấy từ `exports/yolo-v1.zip` và tọa độ điểm ảnh tính tay: ...
- Một `bbox` COCO của cùng xe và `[x1, y1, x2, y2]`: ...
- Một phép tính IoU viết tay (giao, hợp, kết quả): ...

## CP2 — Gán nhãn

- Tổng số box: ... (`occluded`: ..., `truncated`: ...)
- Tình huống khó 1 (ảnh, vị trí, quyết định, quy tắc dùng): ...
- Tình huống khó 2: ...

## CP3 — Xuất và kiểm tra

- `audit` v1: PASS / FAIL — số lần xuất lại: ...
- Lỗi/cảnh báo đã gặp và cách xử lý: ...
- Commit khóa v1 (hash): ...
- Vì sao phải nộp cả COCO và YOLO: ...

## CP4 — So với tham chiếu và sửa

| Chỉ số | v1 | v2 |
|---|---:|---:|
| TP | ... | ... |
| FP (thừa) | ... | ... |
| FN (bỏ sót) | ... | ... |
| Precision | ... | ... |
| Recall | ... | ... |
| IoU trung bình | ... | ... |
| Sai lớp | ... | ... |

3 lỗi đã phân tích:

| # | Ảnh / dòng CSV | Loại lỗi | Nguyên nhân | Quy tắc liên quan | Sửa hay giữ, vì sao |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

## CP5 — Nhãn và điểm của mô hình

| Nhãn dùng để chấm | Precision mô hình | Recall mô hình |
|---|---:|---:|
| v1 của tôi | ... | ... |
| v2 của tôi | ... | ... |
| Tham chiếu | ... | ... |

Giải thích (3–5 câu, chỉ ra ít nhất 1 box cụ thể): ...

## Bonus (nếu làm)

...

## Công cụ AI đã dùng

...
