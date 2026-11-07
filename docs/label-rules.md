# Quy tắc gán nhãn

## Phạm vi

- Chỉ gán 4 lớp dưới đây. Không gán người, xe máy, xe đạp, biển báo, bóng phản chiếu.
- Một xe = một box. Không gộp nhiều xe.
- Xe quá nhỏ hoặc mờ tới mức không phân lớp được: **không gán**, ghi lý do trong báo cáo.

## 4 lớp (thứ tự cố định)

| Mã | Lớp | Gán khi thấy | Không phải lớp này |
|---:|---|---|---|
| 0 | `car` | sedan, hatchback, SUV, taxi, bán tải dùng như xe con | có thùng/ben rõ; thân xe buýt; van thân hộp |
| 1 | `truck` | thùng, ben, sàn chở hàng, thiết bị chuyên dụng | xe con; xe buýt; van kín một khối |
| 2 | `bus` | thân dài, nhiều cửa sổ hoặc hàng ghế | van nhỏ; xe tải |
| 3 | `van` | thân hộp nhỏ, kín, chở người hoặc hàng | thân xe buýt; khoang hàng tách rời như xe tải |

## Box

- Sát mép **phần nhìn thấy** của xe, kể cả gương nếu thấy rõ. Kiểm ở mức phóng 100%.
- Không vẽ phần bị xe khác che khuất (không "đoán" hình dạng đầy đủ).
- Xe chạm mép ảnh vẫn gán nếu đủ bằng chứng phân lớp; box dừng ở mép ảnh.
- Nhiều xe đứng sát nhau: vẫn mỗi xe một box. Bài không dùng box nhóm (`iscrowd` của COCO).

## Thuộc tính

| Thuộc tính | Cách đặt trong CVAT | Bật khi |
|---|---|---|
| `occluded` | biểu tượng **occluded** của box trong danh sách Objects | một phần xe bị vật khác che (xe khác, cột, cây, người) |
| `truncated` | checkbox của nhãn | xe bị **mép ảnh** cắt, phần còn lại nằm ngoài ảnh |

Hai thuộc tính độc lập: một xe có thể vừa `occluded` vừa `truncated`. `audit` cảnh báo khi `truncated` không khớp với
việc box chạm mép ảnh — đọc cảnh báo và tự quyết định.

Bài dùng dạng đúng/sai giống Open Images và BDD100K. KITTI chia nhiều mức hơn (`occluded` 0–3, `truncated` 0–1);
bài này không dùng mức. Nguồn: [sources.md](sources.md#định-nghĩa-thuộc-tính).

## Lỗi thường gặp

| Lỗi | Dấu hiệu trong `compare-rows.csv` | Cách tránh |
|---|---|---|
| Bỏ sót | `bỏ sót (FN)` | rà từng ảnh theo lưới trái→phải, trên→dưới; chú ý xe nhỏ, xe xa, xe bị che |
| Box lỏng | `box lỏng`, `area_ratio` > 1 | phóng to, kéo mép box sát xe |
| Box chật/lệch | `box chật/lệch` | không cắt mất phần nhìn thấy; kiểm cả 4 cạnh |
| Box thừa | `thừa (FP)` | không gán bóng, xe máy, hoặc vẽ 2 box cho một xe |
| Sai lớp | `sai lớp` | đối chiếu bảng 4 lớp; ca khó ghi lý do |
| Quên thuộc tính | cảnh báo trong `audit` | mỗi box xong thì kiểm `occluded`/`truncated` |

## Ca mơ hồ cần ghi vào báo cáo (CP2)

- `bus` hay `van`? — độ dài thân, số hàng cửa sổ.
- `truck` hay `van`/`car`? — có khoang hàng tách rời không.
- Bị che, bị cắt, hay quá ít bằng chứng để gán?
