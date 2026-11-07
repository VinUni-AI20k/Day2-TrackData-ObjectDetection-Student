# Cài CVAT trước buổi học

Lab Coach (người hướng dẫn thực hành) dùng CVAT Community phiên bản `v2.74.1` để cả lớp có cùng giao diện và
cách xuất dữ liệu. Bản mới nhất lúc soạn bài là `v2.82.0` (05/11/2026). Changelog không đổi cách xuất COCO/YOLO, nhưng bản này chưa
được chạy thử với bài — dùng `v2.74.1`.
Hoàn thành cài đặt trước buổi học.

## Kết quả cần có

- Docker đang chạy.
- Lệnh `docker compose version` in ra số phiên bản.
- CVAT mở được tại `http://localhost:8080` bằng Google Chrome.
- Bạn đăng nhập được bằng tài khoản CVAT do mình tạo.
- Lệnh kiểm tra trạng thái máy chủ không báo lỗi.

Không gửi mật khẩu, mã truy cập hoặc tệp cấu hình bí mật cho người khác.

## 1. Cài Docker và Git

Chỉ làm phần tương ứng với hệ điều hành của bạn. Không trộn lệnh giữa Windows, macOS và Ubuntu.

### Windows 10/11

1. Mở **Windows PowerShell** bằng quyền quản trị và chạy:

   ```powershell
   wsl --install
   ```

2. Khởi động lại máy nếu được yêu cầu. Mở ứng dụng **Ubuntu** và tạo tên người dùng, mật khẩu.
3. Tải [Docker Desktop cho Windows](https://www.docker.com/products/docker-desktop/) từ trang chính thức.
4. Trong **Settings (Cài đặt) → General (Chung)**, bật **Use WSL 2 based engine (Dùng nền WSL 2)**.
5. Trong **Resources (Tài nguyên) → WSL Integration (Tích hợp WSL)**, bật Ubuntu rồi chọn
   **Apply & restart (Áp dụng và khởi động lại)**.
6. Mở Ubuntu và chạy:

   ```bash
   sudo apt update
   sudo apt install -y git
   docker version
   docker compose version
   git --version
   ```

### macOS

1. Chọn ** → About This Mac (Giới thiệu về máy Mac này)** và xem máy dùng Apple Silicon hay Intel.
2. Tải đúng bản [Docker Desktop cho macOS](https://www.docker.com/products/docker-desktop/). Với Apple Silicon:
   CVAT chỉ có image `amd64`, nên Docker chạy qua giả lập — mở chậm hơn nhưng đủ cho 4 ảnh.
3. Mở tệp `Docker.dmg`, kéo Docker vào **Applications (Ứng dụng)** rồi mở Docker.
4. Chọn **Use recommended settings (Dùng thiết lập được khuyên dùng)** và chờ Docker chạy xong.
5. Mở **Terminal (Cửa sổ lệnh)** và chạy:

   ```bash
   git --version
   docker version
   docker compose version
   ```

### Ubuntu 22.04/24.04/26.04

Nếu máy đã có Docker hoặc Podman do trường/công ty quản lý, dừng và hỏi người hướng dẫn trước khi thay đổi.

1. Mở cửa sổ lệnh bằng `Ctrl + Alt + T`.
2. Chạy lần lượt:

   ```bash
   sudo apt update
   sudo apt install -y ca-certificates curl git
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc
   sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
   Types: deb
   URIs: https://download.docker.com/linux/ubuntu
   Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
   Components: stable
   Architectures: $(dpkg --print-architecture)
   Signed-By: /etc/apt/keyrings/docker.asc
   EOF
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   sudo usermod -aG docker $USER
   ```

3. Đóng và mở lại cửa sổ lệnh, sau đó chạy:

   ```bash
   docker version
   docker compose version
   git --version
   ```

Tài liệu chính thức để xử lý lỗi cụ thể:

- [Docker Desktop và WSL 2](https://docs.docker.com/desktop/features/wsl/)
- [Docker Desktop cho macOS](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Docker Engine cho Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

## 2. Tải và chạy CVAT

Mở Ubuntu nếu dùng Windows; mở cửa sổ lệnh nếu dùng macOS hoặc Ubuntu. Chạy:

```bash
git clone --depth 1 --branch v2.74.1 https://github.com/cvat-ai/cvat.git cvat-day2
cd cvat-day2
docker compose pull
docker compose up -d
```

Lần đầu cần tải nhiều thành phần nên có thể mất thời gian. Không đóng cửa sổ khi lệnh còn đang chạy.

## 3. Kiểm tra máy chủ và tạo tài khoản

Trong thư mục `cvat-day2`, chạy:

```bash
docker compose ps
docker exec -t cvat_server python manage.py health_check
```

Nếu có dòng `not working` (không hoạt động), chụp toàn bộ cửa sổ và gửi người hướng dẫn. Nếu mọi thành phần đều
`working` (hoạt động), tạo tài khoản:

```bash
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
```

Màn hình hỏi `Username` (tên đăng nhập), `Email address` (địa chỉ thư điện tử) và `Password` (mật khẩu).
Tự đặt thông tin của bạn và không gửi mật khẩu cho ai.

Mở `http://localhost:8080` trên Chrome và đăng nhập.

## Mở lại hoặc dừng CVAT

Từ thư mục `cvat-day2`:

```bash
# Mở lại
docker compose start

# Dừng sau khi đã lưu và xuất dữ liệu
docker compose stop
```

Không chạy `docker compose down -v`; tùy chọn `-v` có thể xóa tác vụ và nhãn đã lưu.

## Không chạy được CVAT trên máy: dùng CVAT Online

Chỉ dùng khi Lab Coach đồng ý, vì CVAT Online chạy bản mới nhất, không phải `v2.74.1`.

1. Mở <https://app.cvat.ai> và tạo tài khoản bằng email cá nhân của bạn.
2. Làm theo [cvat-step-by-step.md](cvat-step-by-step.md) như bình thường: **1 project, 1 task chứa cả 4 ảnh**.
   Gói Free cho tối đa 1 project, 3 task, 1 GB.
3. Xuất với **Save images tắt** (bài chỉ cần nhãn).

Kết quả: lệnh `audit` vẫn chạy được với tệp xuất từ CVAT Online.

## Khi cần hỗ trợ

Gửi cho người hướng dẫn:

- hệ điều hành và loại bộ xử lý nếu biết;
- kết quả `docker version`, `docker compose version`, `docker compose ps`;
- kết quả lệnh kiểm tra trạng thái hoặc tối đa 200 dòng nhật ký;
- ảnh lỗi đã che mật khẩu, mã truy cập và thư điện tử cá nhân.

Lấy 200 dòng nhật ký gần nhất:

```bash
docker compose logs --tail=200 cvat_server
```

Không gửi tệp `.env`, thông tin đăng nhập Docker hoặc mật khẩu.
