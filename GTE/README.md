# GTE – Hệ thống quản lý mua bán mô hình

Bài tập lớn giữa kỳ môn Python.

## 1. Giới thiệu và mục tiêu

GTE là chương trình chạy trên Terminal/CMD giúp quản lý và mua bán các sản phẩm mô hình (Gundam, Figure, Transformers, ...).
Mục tiêu: áp dụng lập trình hướng đối tượng (class, đối tượng, `__init__`, `self`), làm việc với list, file CSV, xử lý lỗi nhập liệu
và chia chương trình thành nhiều module.

## 2. Công nghệ sử dụng

- Python 3.8 trở lên, chỉ dùng thư viện có sẵn (`csv`, `os`, `getpass`, `datetime`, `re`, `unicodedata`). **Không cần cài thêm gì.**
- Lập trình hướng đối tượng (OOP).
- Giao diện menu văn bản trên Terminal/CMD.
- Lưu dữ liệu bằng file CSV (UTF-8).

## 3. Cấu trúc mã nguồn

```
GTE/
├── main.py               # Chương trình chính: đăng nhập, hiển thị menu theo vai trò
├── account.py            # Class TaiKhoan + đăng nhập
├── san_pham.py           # Class SanPham (một sản phẩm)
├── quan_ly_san_pham.py   # Class QuanLySanPham (thêm, sửa, xóa, thống kê, tìm kiếm...)
├── giao_dich.py          # Class GiaoDich, QuanLyGiaoDich (mua hàng, lịch sử giao dịch)
├── database.py           # Class LuuTruCSV (đọc/ghi CSV)
├── tien_ich.py           # Hàm dùng chung: nhập dữ liệu an toàn, định dạng giá, in bảng
├── data.csv              # Dữ liệu sản phẩm
├── accounts.csv          # Dữ liệu tài khoản
├── giao_dich.csv         # Lịch sử giao dịch (tự tạo khi chạy)
└── README.md
```

`tien_ich.py` là file bổ sung duy nhất, dùng để không phải viết lại các đoạn nhập/in bảng ở nhiều nơi.

## 4. Chức năng chính

| Chức năng | admin | user |
|---|:---:|:---:|
| Đăng nhập / đăng xuất (không hiện mật khẩu khi gõ) | ✔ | ✔ |
| Hiển thị danh sách sản phẩm dạng bảng | ✔ | ✔ |
| Thêm sản phẩm / Đăng bán sản phẩm (người bán = tài khoản đang đăng nhập) | ✔ | ✔ |
| Sửa sản phẩm (Enter để giữ giá trị cũ) | tất cả | chỉ của mình |
| Xóa sản phẩm (có xác nhận; từ chối nếu đã có giao dịch) | tất cả | chỉ của mình |
| Thống kê sản phẩm | ✔ | – |
| Tìm kiếm (mã, tên, loại, thương hiệu, khoảng giá, người bán) | ✔ | ✔ |
| Mua sản phẩm (không được mua hàng của chính mình) | ✔ | ✔ |
| Xem lịch sử giao dịch | tất cả | chỉ giao dịch liên quan đến mình |

Ghi chú:
- Tìm kiếm không phân biệt chữ hoa/thường, không phân biệt dấu và cho phép tìm một phần (ví dụ `nendo` tìm ra "Nendoroid Rem").
- Giá nhập được dạng `1500000` hoặc `1.500.000`; hiển thị theo định dạng Việt Nam (`1.500.000 đ`).
- Menu của user và admin được đánh số tự động theo các chức năng mà vai trò đó có.

## 5. Hướng dẫn chạy

**Bằng CMD / Terminal:**

```
cd GTE
python main.py
```

**Bằng VS Code:** mở thư mục `GTE`, mở file `main.py`, nhấn nút ▶ *Run Python File* (hoặc gõ `python main.py` trong Terminal của VS Code).

> Nếu nhập mật khẩu trong một số khung Run/Debug của VS Code thấy mật khẩu bị hiện ra, hãy chạy bằng Terminal thật (CMD hoặc Terminal tích hợp).

## 6. Tài khoản mẫu

| Tên đăng nhập | Mật khẩu | Vai trò |
|---|---|---|
| admin | admin123 | admin |
| user1 | user123 | user |
| user2 | user123 | user |

(Mật khẩu lưu dạng chữ thường trong `accounts.csv` vì đây chỉ là bài tập, không phải hệ thống thương mại.)

## 7. Mô tả ngắn các class

- **TaiKhoan** (`account.py`): thuộc tính `ten_dang_nhap`, `mat_khau`, `vai_tro`. Phương thức `kiem_tra_dang_nhap()` so khớp tài khoản/mật khẩu; `dang_nhap()` cho nhập thông tin (tối đa 3 lần) và trả về tài khoản đúng.
- **SanPham** (`san_pham.py`): thuộc tính `ma_sp`, `ten_sp`, `loai_mo_hinh`, `thuong_hieu`, `gia`, `so_luong`, `mo_ta`, `nguoi_ban`. Phương thức `hien_thi()`, `cap_nhat()`, `kiem_tra_hop_le()`, `chuyen_thanh_dong_csv()`.
- **QuanLySanPham** (`quan_ly_san_pham.py`): giữ danh sách `SanPham`; các phương thức `hien_thi_danh_sach()`, `them_san_pham()`, `sua_san_pham()`, `xoa_san_pham()`, `thong_ke()`, `tim_kiem()`.
- **GiaoDich** (`giao_dich.py`): một giao dịch (mã GD, mã SP, tên SP và đơn giá tại thời điểm mua, người mua, người bán, số lượng, tổng tiền, thời gian).
- **QuanLyGiaoDich** (`giao_dich.py`): `mua_san_pham()` (kiểm tra, xác nhận, trừ tồn kho, ghi lịch sử) và `xem_lich_su()`.
- **LuuTruCSV** (`database.py`): đọc/ghi các file CSV. Các class quản lý chỉ gọi các phương thức của lớp này nên sau này có thể thay bằng cách lưu khác mà không phải viết lại phần quản lý.

## 8. Dữ liệu CSV được lưu như thế nào

- Cả 3 file nằm cùng thư mục với chương trình, mã hóa UTF-8 (có BOM để Excel mở đúng tiếng Việt), dòng đầu là tiêu đề cột.
- `data.csv`: `ma_sp, ten_sp, loai_mo_hinh, thuong_hieu, gia, so_luong, mo_ta, nguoi_ban` – ghi lại sau mỗi lần thêm, sửa, xóa hoặc mua hàng.
- `accounts.csv`: `ten_dang_nhap, mat_khau, vai_tro`.
- `giao_dich.csv`: `ma_gd, ma_sp, ten_sp, nguoi_mua, nguoi_ban, so_luong, don_gia, tong_tien, thoi_gian` – mỗi giao dịch được thêm vào cuối file, không ghi đè dữ liệu cũ.
- Dữ liệu được nạp lại mỗi khi khởi động chương trình.
- **Quy tắc dữ liệu mẫu:** nếu `data.csv` / `accounts.csv` chưa tồn tại hoặc chưa có dòng dữ liệu nào (rỗng hoặc chỉ có tiêu đề) thì chương trình tự tạo dữ liệu mẫu; ngược lại giữ nguyên dữ liệu hiện có (không tạo trùng).
- Dòng dữ liệu sai định dạng (giá không phải số, trùng mã, ...) bị bỏ qua kèm cảnh báo, chương trình không bị dừng.
- Nên đóng file CSV trong Excel trước khi chạy chương trình, nếu không chương trình sẽ báo lỗi không ghi được file.
