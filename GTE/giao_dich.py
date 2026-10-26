"""Giao dịch mua sản phẩm: class GiaoDich (một giao dịch) và QuanLyGiaoDich (xử lý mua, xem lịch sử)."""
from datetime import datetime

import tien_ich


class GiaoDich:
    TIEU_DE_CSV = ["ma_gd", "ma_sp", "ten_sp", "nguoi_mua", "nguoi_ban", "so_luong", "don_gia", "tong_tien", "thoi_gian"]

    def __init__(self, ma_gd, ma_sp, ten_sp, nguoi_mua, nguoi_ban, so_luong, don_gia, tong_tien, thoi_gian):
        self.ma_gd = ma_gd
        self.ma_sp = ma_sp
        self.ten_sp = ten_sp          # tên tại thời điểm giao dịch
        self.nguoi_mua = nguoi_mua
        self.nguoi_ban = nguoi_ban
        self.so_luong = so_luong
        self.don_gia = don_gia        # đơn giá tại thời điểm giao dịch
        self.tong_tien = tong_tien
        self.thoi_gian = thoi_gian

    def lien_quan_den(self, ten_dang_nhap):
        """True nếu tài khoản này là người mua hoặc người bán của giao dịch."""
        return self.nguoi_mua == ten_dang_nhap or self.nguoi_ban == ten_dang_nhap

    def chuyen_thanh_dong_csv(self):
        return {
            "ma_gd": self.ma_gd,
            "ma_sp": self.ma_sp,
            "ten_sp": self.ten_sp,
            "nguoi_mua": self.nguoi_mua,
            "nguoi_ban": self.nguoi_ban,
            "so_luong": self.so_luong,
            "don_gia": self.don_gia,
            "tong_tien": self.tong_tien,
            "thoi_gian": self.thoi_gian,
        }

    @classmethod
    def tu_dong_csv(cls, dong):
        """Tạo GiaoDich từ một dòng CSV. Trả về None nếu dòng sai định dạng."""
        try:
            return cls(
                (dong["ma_gd"] or "").strip(),
                (dong["ma_sp"] or "").strip(),
                (dong["ten_sp"] or "").strip(),
                (dong["nguoi_mua"] or "").strip(),
                (dong["nguoi_ban"] or "").strip(),
                int(dong["so_luong"]),
                int(dong["don_gia"]),
                int(dong["tong_tien"]),
                (dong["thoi_gian"] or "").strip(),
            )
        except (KeyError, TypeError, ValueError, AttributeError):
            return None


class QuanLyGiaoDich:
    def __init__(self, csdl, ql_san_pham):
        self.csdl = csdl
        self.ql_san_pham = ql_san_pham
        self.danh_sach = csdl.doc_giao_dich()

    def tao_ma_gd(self):
        """Mã giao dịch tự tăng: GD001, GD002, ..."""
        so_lon_nhat = 0
        for gd in self.danh_sach:
            phan_so = gd.ma_gd[2:]
            if gd.ma_gd.upper().startswith("GD") and phan_so.isdigit():
                so_lon_nhat = max(so_lon_nhat, int(phan_so))
        return f"GD{so_lon_nhat + 1:03d}"

    def mua_san_pham(self, tai_khoan):
        """Mua sản phẩm: kiểm tra, xác nhận, trừ tồn kho, ghi lịch sử."""
        print("\n----- MUA SẢN PHẨM -----")
        ma = tien_ich.nhap_chuoi("Nhập mã sản phẩm muốn mua (Enter để hủy)", bat_buoc=False)
        if not ma:
            print("Đã hủy.")
            return
        san_pham = self.ql_san_pham.tim_theo_ma(ma)
        if san_pham is None:
            print(f"Không tìm thấy sản phẩm có mã '{ma}'.")
            return
        if san_pham.nguoi_ban == tai_khoan.ten_dang_nhap:
            print("Bạn không thể mua sản phẩm do chính mình đăng bán.")
            return
        if san_pham.so_luong <= 0:
            print("Sản phẩm này đã hết hàng.")
            return

        print()
        san_pham.hien_thi()
        # Nhập số lượng (Enter để hủy), lặp lại đến khi hợp lệ
        while True:
            so_luong = tien_ich.nhap_so_nguyen("Nhập số lượng muốn mua (Enter để hủy)", toi_thieu=1, cho_phep_trong=True)
            if so_luong is None:
                print("Đã hủy.")
                return
            if so_luong > san_pham.so_luong:
                print(f"  Không đủ hàng, trong kho chỉ còn {san_pham.so_luong}.")
                continue
            break

        tong_tien = san_pham.gia * so_luong
        print("\n--- XÁC NHẬN GIAO DỊCH ---")
        print(f"  Sản phẩm : {san_pham.ten_sp} ({san_pham.ma_sp})")
        print(f"  Người bán: {san_pham.nguoi_ban}")
        print(f"  Đơn giá  : {tien_ich.dinh_dang_gia(san_pham.gia)}")
        print(f"  Số lượng : {so_luong}")
        print(f"  Tổng tiền: {tien_ich.dinh_dang_gia(tong_tien)}")
        if not tien_ich.xac_nhan("Xác nhận mua hàng?"):
            print("Đã hủy giao dịch, số lượng hàng không thay đổi.")
            return

        # Chỉ trừ hàng sau khi người mua đã xác nhận
        giao_dich = GiaoDich(
            self.tao_ma_gd(), san_pham.ma_sp, san_pham.ten_sp, tai_khoan.ten_dang_nhap,
            san_pham.nguoi_ban, so_luong, san_pham.gia, tong_tien,
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )
        san_pham.so_luong -= so_luong
        try:
            self.csdl.ghi_san_pham(self.ql_san_pham.danh_sach)
            self.csdl.them_giao_dich(giao_dich)
        except OSError as loi:
            san_pham.so_luong += so_luong  # hoàn lại trong bộ nhớ
            print(f"Lỗi: không ghi được dữ liệu, giao dịch bị hủy ({loi}).")
            return
        self.danh_sach.append(giao_dich)
        print(f"Mua hàng thành công! Mã giao dịch: {giao_dich.ma_gd}. Tổng tiền: {tien_ich.dinh_dang_gia(tong_tien)}.")

    def xem_lich_su(self, tai_khoan):
        """Admin xem tất cả; user chỉ xem giao dịch liên quan đến mình."""
        if tai_khoan.la_admin():
            ds = self.danh_sach
            print("\n----- LỊCH SỬ GIAO DỊCH (TẤT CẢ) -----")
        else:
            ds = [gd for gd in self.danh_sach if gd.lien_quan_den(tai_khoan.ten_dang_nhap)]
            print("\n----- LỊCH SỬ GIAO DỊCH CỦA BẠN -----")
        if not ds:
            print("Chưa có giao dịch nào.")
            return
        cot = [("Mã GD", 6, False), ("Mã SP", 6, False), ("Tên sản phẩm", 20, False),
               ("Người mua", 10, False), ("Người bán", 10, False), ("SL", 3, True),
               ("Đơn giá", 13, True), ("Tổng tiền", 14, True), ("Thời gian", 19, False)]
        hang = [[gd.ma_gd, gd.ma_sp, gd.ten_sp, gd.nguoi_mua, gd.nguoi_ban, gd.so_luong,
                 tien_ich.dinh_dang_gia(gd.don_gia), tien_ich.dinh_dang_gia(gd.tong_tien), gd.thoi_gian]
                for gd in ds]
        tien_ich.in_bang(cot, hang)
        print(f"Tổng cộng: {len(ds)} giao dịch.")
