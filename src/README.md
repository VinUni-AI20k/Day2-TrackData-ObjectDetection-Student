# src

| Mục | Nội dung |
|---|---|
| Tệp bắt đầu | `cp1_box_math.py` (CP1), sau đó `day2_lab.py` (CP3–CP5) |
| Tệp được sửa | chỉ `cp1_box_math.py` |
| Không sửa | `day2_lab.py`, `data/`, `tests/` |
| Input | 4 ảnh trong `data/images/`, bản xuất CVAT của bạn trong `exports/`, `day2-reference.zip` do Coach phát |
| Output | `outputs/v1/`, `outputs/v2/` (JSON, CSV, ảnh overlay) |

## Cài đặt

```bash
python -m pip install -r src/requirements.txt
```

Chạy mọi lệnh từ **thư mục gốc repo**.

## Lệnh theo checkpoint

```bash
# CP1 — tự kiểm tra 3 hàm của bạn
python src/cp1_box_math.py

# CP3 — kiểm tra hai bản xuất (in PASS/FAIL, ghi audit.json)
python src/day2_lab.py audit --coco exports/coco-v1.zip --yolo exports/yolo-v1.zip --out outputs/v1

# CP4 — so với tham chiếu và vẽ overlay
python src/day2_lab.py compare --mine exports/coco-v1.zip --reference day2-reference.zip --out outputs/v1
python src/day2_lab.py overlay --mine exports/coco-v1.zip --reference day2-reference.zip --out outputs/v1

# CP4 — sau khi sửa, lặp lại với v2
python src/day2_lab.py audit   --coco exports/coco-v2.zip --yolo exports/yolo-v2.zip --out outputs/v2
python src/day2_lab.py compare --mine exports/coco-v2.zip --reference day2-reference.zip --out outputs/v2
python src/day2_lab.py overlay --mine exports/coco-v2.zip --reference day2-reference.zip --out outputs/v2

# CP5 — chấm cùng một mô hình bằng 3 bộ nhãn
python src/day2_lab.py model-check --labels exports/coco-v1.zip exports/coco-v2.zip day2-reference.zip
```

`day2-reference.zip` để ở thư mục gốc nhưng **không commit** (đã có trong `.gitignore`).

## Đọc kết quả

| Tệp | Ý nghĩa |
|---|---|
| `audit.json` | `status`, `errors` (phải sửa), `warnings` (tự quyết định), số box, `occluded`/`truncated` mỗi ảnh |
| `compare-summary.json` | TP, FP (thừa), FN (bỏ sót), precision, recall, IoU trung bình |
| `compare-rows.csv` | mỗi dòng một box: loại lỗi, IoU, tọa độ của bạn và tham chiếu |
| `*-overlay.png` | xanh = tham chiếu, đỏ = bạn, cam = box có `occluded`/`truncated` |

## Dùng Google Colab

Repo bài nộp là private nên Colab không tự tải được. Tải lên Colab: `src/` (cả thư mục) và `exports/`, rồi chạy
`!pip install pillow pyyaml` và các lệnh trên với tiền tố `!`. Tải `outputs/` về và commit từ máy.

## Kiểm thử của repo

```bash
python -m unittest discover -s src/tests -v
```
