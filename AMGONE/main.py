"""GTE - Hệ thống quản lý mua bán mô hình (chạy bằng: python main.py)."""
import sys

from account import TaiKhoan
from database import LuuTruCSV
from giao_dich import QuanLyGiaoDich
from gacha import QuanLyGacha
from quan_ly_san_pham import QuanLySanPham
import tien_ich


def tao_menu(tai_khoan):
    """Trả về danh sách (mã chức năng, tên hiển thị) theo vai trò. Số thứ tự đánh tự động."""
    if tai_khoan.la_admin():
        return [
            ("hien_thi", "Hiển thị danh sách sản phẩm"),
            ("them", "Thêm sản phẩm"),
            ("sua", "Sửa sản phẩm"),
            ("xoa", "Xóa sản phẩm"),
            ("thong_ke", "Thống kê sản phẩm"),
            ("tim_kiem", "Tìm kiếm sản phẩm"),
            ("mua", "Mua sản phẩm"),
            ("lich_su", "Xem lịch sử giao dịch (tất cả)"),
            ("vi", "Xem ví tiền"),
            ("nap_tien", "Nạp tiền mô phỏng"),
            ("gacha", "Gacha mô hình (4.000.000 VNĐ/lượt)"),
            ("lich_su_gacha", "Xem lịch sử Gacha"),
            ("dang_xuat", "Đăng xuất"),
        ]
    return [
        ("hien_thi", "Hiển thị danh sách sản phẩm"),
        ("them", "Đăng bán sản phẩm"),
        ("sua", "Sửa sản phẩm của tôi"),
        ("xoa", "Xóa sản phẩm của tôi"),
        ("tim_kiem", "Tìm kiếm sản phẩm"),
        ("mua", "Mua sản phẩm"),
        ("lich_su", "Xem lịch sử giao dịch của tôi"),
        ("vi", "Xem ví tiền"),
        ("nap_tien", "Nạp tiền mô phỏng"),
        ("gacha", "Gacha mô hình (4.000.000 VNĐ/lượt)"),
        ("lich_su_gacha", "Xem lịch sử Gacha"),
        ("dang_xuat", "Đăng xuất"),
    ]


def thuc_hien_chuc_nang(ma_chuc_nang, tai_khoan, ql_sp, ql_gd, ql_gacha, csdl):
    """Gọi phương thức tương ứng với chức năng được chọn."""
    if ma_chuc_nang == "hien_thi":
        print("\n----- DANH SÁCH SẢN PHẨM -----")
        ql_sp.hien_thi_danh_sach()
    elif ma_chuc_nang == "them":
        ql_sp.them_san_pham(tai_khoan)
    elif ma_chuc_nang == "sua":
        ql_sp.sua_san_pham(tai_khoan)
    elif ma_chuc_nang == "xoa":
        ql_sp.xoa_san_pham(tai_khoan)
    elif ma_chuc_nang == "thong_ke":
        ql_sp.thong_ke()
    elif ma_chuc_nang == "tim_kiem":
        ql_sp.tim_kiem()
    elif ma_chuc_nang == "mua":
        ql_gd.mua_san_pham(tai_khoan)
    elif ma_chuc_nang == "lich_su":
        ql_gd.xem_lich_su(tai_khoan)
    elif ma_chuc_nang == "vi":
        print(f"\nSố dư ví hiện tại: {tien_ich.dinh_dang_gia(tai_khoan.so_du)}")
    elif ma_chuc_nang == "nap_tien":
        so_tien = tien_ich.nhap_so_nguyen("Số tiền muốn nạp (VNĐ, Enter để hủy)", toi_thieu=1, cho_phep_trong=True)
        if so_tien is None:
            print("Đã hủy nạp tiền.")
            return
        so_du_cu = tai_khoan.so_du
        tai_khoan.so_du += so_tien
        try:
            ds_tk = csdl.doc_tai_khoan()
            for tk in ds_tk:
                if tk.ten_dang_nhap == tai_khoan.ten_dang_nhap:
                    tk.so_du = tai_khoan.so_du
            csdl.ghi_tai_khoan(ds_tk)
        except OSError as loi:
            tai_khoan.so_du = so_du_cu
            print(f"Nạp tiền thất bại: không ghi được dữ liệu ({loi}).")
            return
        print(f"Đã nạp {tien_ich.dinh_dang_gia(so_tien)}. Số dư mới: {tien_ich.dinh_dang_gia(tai_khoan.so_du)}")
    elif ma_chuc_nang == "gacha":
        ql_gacha.quay(tai_khoan)
    elif ma_chuc_nang == "lich_su_gacha":
        ql_gacha.xem_lich_su(tai_khoan)


def chay_menu_chinh(tai_khoan, ql_sp, ql_gd, ql_gacha, csdl):
    """Vòng lặp menu chính, thoát khi người dùng chọn Đăng xuất."""
    menu = tao_menu(tai_khoan)
    cac_lua_chon = {str(i): ma for i, (ma, _) in enumerate(menu, start=1)}
    while True:
        print("\n========== GTE – QUẢN LÝ MÔ HÌNH ==========")
        print(f"Tài khoản: {tai_khoan.ten_dang_nhap} ({tai_khoan.vai_tro})\n")
        for i, (_, ten) in enumerate(menu, start=1):
            print(f"{i}. {ten}")
        print("===========================================")
        lua_chon = input("Lựa chọn: ").strip()
        if lua_chon not in cac_lua_chon:
            print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
            continue
        if cac_lua_chon[lua_chon] == "dang_xuat":
            print("Đã đăng xuất.")
            return
        thuc_hien_chuc_nang(cac_lua_chon[lua_chon], tai_khoan, ql_sp, ql_gd, ql_gacha, csdl)
        tien_ich.tam_dung()


def main():
    # Đảm bảo nhập/xuất tiếng Việt đúng khi chạy trên CMD/terminal
    for luong in (sys.stdin, sys.stdout):
        try:
            luong.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError, OSError):
            pass

    csdl = LuuTruCSV()
    csdl.khoi_tao()
    danh_sach_tai_khoan = csdl.doc_tai_khoan()
    ql_sp = QuanLySanPham(csdl)
    ql_gd = QuanLyGiaoDich(csdl, ql_sp)
    ql_gacha = QuanLyGacha(csdl, ql_sp)

    try:
        while True:
            print("\n========== GTE – HỆ THỐNG MUA BÁN MÔ HÌNH ==========")
            print("1. Đăng nhập")
            print("2. Đăng ký tài khoản")
            print("3. Thoát chương trình")
            lua_chon = input("Lựa chọn: ").strip()
            if lua_chon == "1":
                danh_sach_tai_khoan = csdl.doc_tai_khoan()
                tai_khoan = TaiKhoan.dang_nhap(danh_sach_tai_khoan)
                if tai_khoan is not None:
                    chay_menu_chinh(tai_khoan, ql_sp, ql_gd, ql_gacha, csdl)
                    # Làm mới dữ liệu sau khi đăng xuất để số dư luôn mới nhất.
                    danh_sach_tai_khoan = csdl.doc_tai_khoan()
                    ql_sp.danh_sach = csdl.doc_san_pham()
                    ql_gd.danh_sach = csdl.doc_giao_dich()
            elif lua_chon == "2":
                TaiKhoan.dang_ky(danh_sach_tai_khoan, csdl)
            elif lua_chon == "3":
                print("Tạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
    except (EOFError, KeyboardInterrupt):
        print("\nĐã thoát chương trình.")


if __name__ == "__main__":
    main()
