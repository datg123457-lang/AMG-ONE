# AMGONE – Hệ thống quản lý mua bán mô hình

Bài tập lớn Python theo hướng đối tượng (OOP), chạy trên Terminal/CMD và lưu dữ liệu bằng CSV. Dự án ưu tiên code dễ đọc, phù hợp để trình bày trong lớp; không cần cài thư viện ngoài.

## 1. Chức năng

- Đăng nhập, đăng ký tài khoản user; tài khoản đăng ký mới có số dư 0 VNĐ.
- Quản lý sản phẩm: xem, đăng bán, sửa, xóa (xóa bị từ chối nếu đã có giao dịch), tìm kiếm; admin có thêm thống kê.
- Ví tiền: xem số dư và nạp tiền mô phỏng.
- Mua hàng: kiểm tra tồn kho, số dư, quyền sở hữu; cập nhật ví người mua/người bán, tồn kho và lịch sử giao dịch.
- Quy tắc Admin: Admin không bị trừ tiền khi mua; người bán là user vẫn nhận đủ tiền. Admin mua sản phẩm của chính mình thì không tự cộng tiền cho mình. Tồn kho và lịch sử vẫn được cập nhật.
- Gacha: giá cố định **4.000.000 VNĐ/lượt**, dùng trực tiếp các sản phẩm đang bán còn hàng; tự tính trọng số theo giá hiện tại; không hiển thị tỷ lệ trúng; trừ tiền người quay, giảm một đơn vị tồn kho và ghi lịch sử riêng. Gacha không cộng tiền cho người bán và không tạo giao dịch mua bán thường.
- Lịch sử mua bán và lịch sử Gacha; user chỉ xem lịch sử của mình/liên quan đến mình, admin xem toàn bộ.

## 2. Cấu trúc thư mục

```text
AMGONE/
├── main.py                 # Menu, điều hướng, ví tiền và khởi chạy
├── account.py              # Class TaiKhoan, đăng nhập và đăng ký
├── san_pham.py             # Class SanPham và kiểm tra dữ liệu
├── quan_ly_san_pham.py     # Thêm/sửa/xóa/tìm kiếm/thống kê sản phẩm
├── giao_dich.py            # Mua hàng và lịch sử mua bán
├── gacha.py                # Gacha và lịch sử Gacha
├── database.py              # Đọc/ghi CSV
├── tien_ich.py              # Nhập liệu, định dạng tiền, in bảng
├── data.csv                 # Danh sách sản phẩm đang bán; cũng là nguồn Gacha
├── accounts.csv             # Tài khoản, quyền và số dư
├── giao_dich.csv            # Lịch sử mua bán
├── lich_su_gacha.csv        # Lịch sử lượt quay thành công
└── README.md
```

## 3. Môi trường và cách chạy

- Python 3.8 trở lên.
- Không cần cài package bên ngoài.
- Mở CMD/Terminal tại thư mục `AMGONE`, chạy:

```bash
python main.py
```

## 4. Tài khoản mẫu

| Tên đăng nhập | Mật khẩu | Vai trò |
|---|---|---|
| admin | admin123 | admin |
| user1 | user123 | user |
| user2 | user123 | user |

Đây là tài khoản mẫu cho bài tập; mật khẩu đang lưu dạng văn bản trong CSV, không dùng cho hệ thống thực tế.

## 5. Hướng dẫn sử dụng

1. Chọn **Đăng nhập** để vào tài khoản có sẵn hoặc **Đăng ký tài khoản** để tạo user mới.
2. Trong menu, chọn **Nạp tiền mô phỏng** và nhập số nguyên dương; chấp nhận cách nhập `4000000` hoặc `4.000.000`.
3. Chọn **Đăng bán sản phẩm** để thêm sản phẩm vào danh sách bán. Sản phẩm có giá hợp lệ và tồn kho lớn hơn 0 tự động đủ điều kiện Gacha.
4. Chọn **Mua sản phẩm** để mua hàng thông thường. Người mua user cần đủ tiền; Admin không bị trừ ví nhưng giao dịch vẫn giảm tồn kho và được lưu lịch sử.
5. Chọn **Gacha mô hình** để xem danh sách sản phẩm đủ điều kiện và quay với giá cố định 4.000.000 VNĐ/lượt. Giao diện không hiển thị phần trăm, trọng số hay tỷ lệ trúng.
6. Chọn **Xem lịch sử Gacha** để xem các lượt quay đã lưu.

## 6. Quy tắc Gacha

- Không có danh sách phần thưởng riêng: **danh sách sản phẩm đang bán trong `data.csv` chính là nguồn phần thưởng**. Không tạo `phan_thuong_gacha.csv`.
- Chỉ sản phẩm còn tồn kho, có giá nguyên dương và dữ liệu hợp lệ mới tham gia.
- Trọng số được tính lại ở mỗi lượt từ giá bán hiện tại theo `w = 1 / giá^k`, với `k = 1`. Giá được chuẩn hóa theo triệu VNĐ trước phép tính để dễ xử lý số học; kết quả xác suất tương đối không đổi.
- Sản phẩm rẻ hơn có trọng số cao hơn. Giá thay đổi hoặc sản phẩm mới được đăng bán sẽ được phản ánh tự động.
- Khi trúng: trừ 4.000.000 VNĐ khỏi ví người quay, giảm tồn kho đúng một, lưu tên và giá trị sản phẩm tại thời điểm quay. Không cộng tiền cho người bán và không ghi vào lịch sử mua bán thường.
- Sản phẩm hết hàng không được quay tiếp. Lịch sử cũ vẫn giữ thông tin sản phẩm kể cả khi sản phẩm sau đó thay đổi.

## 7. Các file CSV

- `accounts.csv`: `ten_dang_nhap, mat_khau, vai_tro, so_du`. Khi mở dữ liệu tài khoản cũ thiếu `so_du`, chương trình mặc định số dư bằng 0 và bổ sung cột mà không yêu cầu xóa CSV.
- `data.csv`: `ma_sp, ten_sp, loai_mo_hinh, thuong_hieu, gia, so_luong, mo_ta, nguoi_ban`.
- `giao_dich.csv`: lịch sử mua bán với mã, sản phẩm, người mua/bán, số lượng, đơn giá, tổng tiền và thời gian.
- `lich_su_gacha.csv`: mã lượt quay, người quay, mã/tên sản phẩm, giá trị tại thời điểm quay, giá quay và thời gian.

Các file được lưu cùng thư mục chương trình bằng UTF-8 có BOM để thuận tiện mở bằng Excel. Chương trình có tạo dữ liệu mẫu nếu file sản phẩm/tài khoản chưa tồn tại hoặc chưa có bản ghi; hãy sao lưu CSV trước khi thử nghiệm với dữ liệu quan trọng.

## 8. Lưu ý về dữ liệu

Các thao tác mua hàng và Gacha lưu bản sao nội dung những file liên quan để thử khôi phục nếu bước ghi dữ liệu gặp lỗi. Vì CSV không có transaction nguyên tử như cơ sở dữ liệu, đây là cơ chế hoàn tác ở mức phù hợp với bài tập lớn, không phải bảo đảm giao dịch cấp ngân hàng. Nếu đang mở CSV trong Excel, hãy đóng file trước khi chạy để tránh lỗi ghi.
