"""Class QuanLySanPham: quản lý danh sách đối tượng SanPham."""
import tien_ich
from san_pham import SanPham


class QuanLySanPham:
    def __init__(self, csdl):
        self.csdl = csdl                        # nơi lưu trữ (LuuTruCSV)
        self.danh_sach = csdl.doc_san_pham()    # nạp dữ liệu khi khởi động

    # ---------- Hàm hỗ trợ ----------
    def luu(self):
        """Ghi danh sách hiện tại ra file. Trả về True nếu thành công."""
        try:
            self.csdl.ghi_san_pham(self.danh_sach)
            return True
        except OSError as loi:
            print(f"Lỗi: không ghi được file dữ liệu ({loi}). Hãy đóng file CSV nếu đang mở bằng Excel.")
            return False

    def tim_theo_ma(self, ma):
        """Tìm sản phẩm theo mã (không phân biệt hoa thường). Không thấy -> None."""
        ma = tien_ich.chuan_hoa(ma).upper()
        for san_pham in self.danh_sach:
            if san_pham.ma_sp.upper() == ma:
                return san_pham
        return None

    def tao_ma_moi(self):
        """Tạo mã duy nhất dạng SP001, SP002, ... (lớn nhất hiện có + 1)."""
        so_lon_nhat = 0
        for san_pham in self.danh_sach:
            phan_so = san_pham.ma_sp[2:]
            if san_pham.ma_sp.upper().startswith("SP") and phan_so.isdigit():
                so_lon_nhat = max(so_lon_nhat, int(phan_so))
        return f"SP{so_lon_nhat + 1:03d}"

    def co_quyen(self, tai_khoan, san_pham):
        """Admin quản lý tất cả; user chỉ quản lý sản phẩm do mình đăng bán."""
        return tai_khoan.la_admin() or san_pham.nguoi_ban == tai_khoan.ten_dang_nhap

    # ---------- 6.2 Hiển thị ----------
    def hien_thi_danh_sach(self, danh_sach=None, thong_bao_rong="Danh sách sản phẩm đang trống."):
        """In danh sách sản phẩm dạng bảng (mặc định in toàn bộ)."""
        if danh_sach is None:
            danh_sach = self.danh_sach
        if not danh_sach:
            print(thong_bao_rong)
            return
        cot = [("Mã", 6, False), ("Tên sản phẩm", 26, False), ("Loại", 13, False),
               ("Thương hiệu", 18, False), ("Giá", 14, True), ("SL", 4, True), ("Người bán", 10, False)]
        hang = [[sp.ma_sp, sp.ten_sp, sp.loai_mo_hinh, sp.thuong_hieu,
                 tien_ich.dinh_dang_gia(sp.gia), sp.so_luong, sp.nguoi_ban] for sp in danh_sach]
        tien_ich.in_bang(cot, hang)
        print(f"Tổng cộng: {len(danh_sach)} sản phẩm.")

    # ---------- 6.3 Thêm ----------
    def them_san_pham(self, tai_khoan):
        """Thêm / đăng bán sản phẩm. Người bán là tài khoản đang đăng nhập."""
        print("\n----- THÊM SẢN PHẨM -----")
        ma_sp = self.tao_ma_moi()
        print(f"Mã sản phẩm (tự động): {ma_sp}")
        ten_sp = tien_ich.nhap_chuoi("Tên sản phẩm")
        loai = tien_ich.nhap_chuoi("Loại mô hình (Gundam, Figure, ...)")
        thuong_hieu = tien_ich.nhap_chuoi("Thương hiệu")
        gia = tien_ich.nhap_so_nguyen("Giá bán (VNĐ)", toi_thieu=1)
        so_luong = tien_ich.nhap_so_nguyen("Số lượng", toi_thieu=0)
        mo_ta = tien_ich.nhap_chuoi("Mô tả (có thể bỏ trống)", bat_buoc=False)

        san_pham = SanPham(ma_sp, ten_sp, loai, thuong_hieu, gia, so_luong, mo_ta, tai_khoan.ten_dang_nhap)
        hop_le, thong_bao = san_pham.kiem_tra_hop_le()
        if not hop_le:
            print(f"Thêm thất bại: {thong_bao}")
            return
        if self.tim_theo_ma(san_pham.ma_sp) is not None:
            print("Thêm thất bại: mã sản phẩm bị trùng.")
            return
        self.danh_sach.append(san_pham)
        if not self.luu():
            self.danh_sach.remove(san_pham)  # ghi lỗi thì hoàn tác
            print("Thêm thất bại.")
            return
        print(f"Đã thêm sản phẩm '{san_pham.ten_sp}' với mã {san_pham.ma_sp}.")

    # ---------- 6.4 Sửa ----------
    def sua_san_pham(self, tai_khoan):
        print("\n----- SỬA SẢN PHẨM -----")
        ma = tien_ich.nhap_chuoi("Nhập mã sản phẩm cần sửa (Enter để hủy)", bat_buoc=False)
        if not ma:
            print("Đã hủy.")
            return
        san_pham = self.tim_theo_ma(ma)
        if san_pham is None:
            print(f"Không tìm thấy sản phẩm có mã '{ma}'.")
            return
        if not self.co_quyen(tai_khoan, san_pham):
            print("Bạn chỉ được sửa sản phẩm do chính mình đăng bán.")
            return

        print("Thông tin hiện tại:")
        san_pham.hien_thi()
        print("Nhấn Enter để giữ nguyên giá trị cũ.")
        ten_sp = tien_ich.nhap_chuoi("Tên sản phẩm", san_pham.ten_sp)
        loai = tien_ich.nhap_chuoi("Loại mô hình", san_pham.loai_mo_hinh)
        thuong_hieu = tien_ich.nhap_chuoi("Thương hiệu", san_pham.thuong_hieu)
        gia = tien_ich.nhap_so_nguyen("Giá bán (VNĐ)", toi_thieu=1, mac_dinh=san_pham.gia)
        so_luong = tien_ich.nhap_so_nguyen("Số lượng", toi_thieu=0, mac_dinh=san_pham.so_luong)
        mo_ta = tien_ich.nhap_chuoi("Mô tả", san_pham.mo_ta)

        ban_sao = san_pham.sao_luu()
        hop_le, thong_bao = san_pham.cap_nhat(ten_sp, loai, thuong_hieu, gia, so_luong, mo_ta)
        if not hop_le:
            print(f"Sửa thất bại: {thong_bao}")
            return
        if not self.luu():
            san_pham.khoi_phuc(ban_sao)
            print("Sửa thất bại.")
            return
        print("Đã cập nhật sản phẩm:")
        san_pham.hien_thi()

    # ---------- 6.5 Xóa ----------
    def xoa_san_pham(self, tai_khoan):
        print("\n----- XÓA SẢN PHẨM -----")
        ma = tien_ich.nhap_chuoi("Nhập mã sản phẩm cần xóa (Enter để hủy)", bat_buoc=False)
        if not ma:
            print("Đã hủy.")
            return
        san_pham = self.tim_theo_ma(ma)
        if san_pham is None:
            print(f"Không tìm thấy sản phẩm có mã '{ma}'.")
            return
        if not self.co_quyen(tai_khoan, san_pham):
            print("Bạn chỉ được xóa sản phẩm do chính mình đăng bán.")
            return
        if self.csdl.san_pham_co_giao_dich(san_pham.ma_sp):
            print("Không thể xóa: sản phẩm đã phát sinh giao dịch (cần giữ lại để bảo toàn lịch sử).")
            return

        san_pham.hien_thi()
        if not tien_ich.xac_nhan("Bạn chắc chắn muốn xóa sản phẩm này?"):
            print("Đã hủy, sản phẩm không bị xóa.")
            return
        vi_tri = self.danh_sach.index(san_pham)
        self.danh_sach.remove(san_pham)
        if not self.luu():
            self.danh_sach.insert(vi_tri, san_pham)  # ghi lỗi thì hoàn tác
            print("Xóa thất bại.")
            return
        print(f"Đã xóa sản phẩm {san_pham.ma_sp}.")

    # ---------- 6.6 Thống kê ----------
    def thong_ke(self):
        print("\n----- THỐNG KÊ SẢN PHẨM -----")
        if not self.danh_sach:
            print("Chưa có sản phẩm nào để thống kê.")
            return
        tong_so_sp = len(self.danh_sach)
        tong_so_luong = sum(sp.so_luong for sp in self.danh_sach)
        tong_gia_tri = sum(sp.gia * sp.so_luong for sp in self.danh_sach)
        dat_nhat = max(self.danh_sach, key=lambda sp: sp.gia)
        re_nhat = min(self.danh_sach, key=lambda sp: sp.gia)

        print(f"Tổng số sản phẩm            : {tong_so_sp}")
        print(f"Tổng số lượng còn lại       : {tong_so_luong}")
        print(f"Tổng giá trị hàng tồn kho   : {tien_ich.dinh_dang_gia(tong_gia_tri)}")
        print(f"Sản phẩm giá cao nhất       : {dat_nhat.ten_sp} ({dat_nhat.ma_sp}) - {tien_ich.dinh_dang_gia(dat_nhat.gia)}")
        print(f"Sản phẩm giá thấp nhất      : {re_nhat.ten_sp} ({re_nhat.ma_sp}) - {tien_ich.dinh_dang_gia(re_nhat.gia)}")

        # Đếm số sản phẩm theo từng loại mô hình
        so_sp_theo_loai = {}
        for sp in self.danh_sach:
            so_sp_theo_loai[sp.loai_mo_hinh] = so_sp_theo_loai.get(sp.loai_mo_hinh, 0) + 1
        print("Số sản phẩm theo loại mô hình:")
        for loai, so_sp in sorted(so_sp_theo_loai.items()):
            print(f"  - {loai}: {so_sp}")

    # ---------- 6.7 Tìm kiếm ----------
    def tim_kiem(self):
        print("\n----- TÌM KIẾM SẢN PHẨM -----")
        print("1. Theo mã sản phẩm")
        print("2. Theo tên sản phẩm")
        print("3. Theo loại mô hình")
        print("4. Theo thương hiệu")
        print("5. Theo khoảng giá")
        print("6. Theo người bán")
        print("0. Quay lại")
        lua_chon = input("Chọn cách tìm: ").strip()
        if lua_chon == "0":
            return

        if lua_chon == "5":
            gia_tu = tien_ich.nhap_so_nguyen("Giá từ (Enter = không giới hạn)", toi_thieu=0, cho_phep_trong=True)
            gia_den = tien_ich.nhap_so_nguyen("Giá đến (Enter = không giới hạn)", toi_thieu=0, cho_phep_trong=True)
            if gia_tu is not None and gia_den is not None and gia_tu > gia_den:
                print("Khoảng giá không hợp lệ: giá 'từ' phải nhỏ hơn hoặc bằng giá 'đến'.")
                return
            ket_qua = [sp for sp in self.danh_sach
                       if (gia_tu is None or sp.gia >= gia_tu) and (gia_den is None or sp.gia <= gia_den)]
        else:
            ten_truong = {"1": "ma_sp", "2": "ten_sp", "3": "loai_mo_hinh", "4": "thuong_hieu", "6": "nguoi_ban"}
            if lua_chon not in ten_truong:
                print("Lựa chọn không hợp lệ.")
                return
            tu_khoa = tien_ich.bo_dau(tien_ich.nhap_chuoi("Nhập từ khóa"))
            # Không phân biệt hoa/thường và dấu, tìm một phần chuỗi
            ket_qua = [sp for sp in self.danh_sach
                       if tu_khoa in tien_ich.bo_dau(getattr(sp, ten_truong[lua_chon]))]

        print("\nKết quả tìm kiếm:")
        self.hien_thi_danh_sach(ket_qua, "Không tìm thấy sản phẩm phù hợp.")
