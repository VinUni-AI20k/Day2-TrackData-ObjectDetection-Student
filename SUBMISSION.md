# Submission

## Loại bài

`Cá nhân`. Mỗi học viên tự tạo repo và tự nộp link.

## Tên repo bài nộp

```text
K4-L2-DAY02-HoVaTen-MSSV-ObjectDetection
```

Học viên level 3 dùng `K4-L3-DAY02-HoVaTen-MSSV-ObjectDetection`. Lớp riêng thay `L2`/`L3` bằng `L2A`, `L2B`,
`L3A`, `L3B`. Không dấu, không khoảng trắng, ngăn cách bằng `-`.
Ví dụ: `K4-L2-DAY02-NguyenVanAn-2A20260000-ObjectDetection`.

## Cấu trúc phải nộp

```text
report/individual/MSSV_HoTen.md      báo cáo (ví dụ 20241234_NguyenVanAn.md)
src/cp1_box_math.py                  bài CP1 đã điền
exports/coco-v1.zip  exports/yolo-v1.zip
exports/coco-v2.zip  exports/yolo-v2.zip
outputs/v1/  outputs/v2/             audit.json, compare-*.json/csv, overlay *.png
```

Không nộp `day2-reference.zip`, ảnh gốc, tệp mô hình `.pt` hoặc thư mục `runs/`.

## Nơi nộp và deadline (GMT+7)

- Nộp link repo trên LMS bằng tài khoản cá nhân.
- Lab sáng: trước **23:59** ngày lab. Lab tối/chiều: trước **11:59** ngày hôm sau.
- Key Coach có thể thông báo deadline khác trong 48 giờ sau buổi lab.
- Commit v1 (CP3) phải có **trước** giờ Coach phát tham chiếu.

## Checklist trước khi nộp

- [ ] Tên repo đúng mẫu.
- [ ] Báo cáo đã đổi tên `MSSV_HoTen.md` và không còn chỗ trống.
- [ ] `python src/cp1_box_math.py` in 6 dòng `OK`.
- [ ] `outputs/v1/audit.json` và `outputs/v2/audit.json` đều `"status": "pass"`.
- [ ] Repo không chứa `day2-reference.zip`, mật khẩu, token hay `.env`.
- [ ] Đã nộp link trên LMS.
