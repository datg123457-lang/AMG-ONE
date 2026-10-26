"""Class TaiKhoan: thông tin tài khoản và chức năng đăng nhập."""
import tien_ich

SO_LAN_THU_TOI_DA = 3


class TaiKhoan:
    TIEU_DE_CSV = ["ten_dang_nhap", "mat_khau", "vai_tro", "so_du"]

    def __init__(self, ten_dang_nhap, mat_khau, vai_tro="user", so_du=0):
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro  # "admin" hoặc "user"
        self.so_du = max(0, int(so_du))

    def la_admin(self):
        return self.vai_tro == "admin"

    def kiem_tra_dang_nhap(self, ten_dang_nhap, mat_khau):
        """Trả về True nếu tên đăng nhập và mật khẩu khớp với tài khoản này."""
        return self.ten_dang_nhap == ten_dang_nhap and self.mat_khau == mat_khau

    @staticmethod
    def dang_nhap(danh_sach_tai_khoan):
        """Cho người dùng nhập tài khoản, mật khẩu (tối đa 3 lần).

        Trả về đối tượng TaiKhoan nếu đúng, None nếu hủy hoặc sai quá số lần.
        Mật khẩu được nhập bằng getpass nên không hiện lên màn hình.
        """
        print("\n----- ĐĂNG NHẬP -----")
        for lan in range(1, SO_LAN_THU_TOI_DA + 1):
            ten = tien_ich.chuan_hoa(input("Tên đăng nhập (Enter để quay lại): "))
            if not ten:
                return None
            mat_khau = input("Mật khẩu: ")
            for tai_khoan in danh_sach_tai_khoan:
                if tai_khoan.kiem_tra_dang_nhap(ten, mat_khau):
                    print(f"Đăng nhập thành công! Xin chào {tai_khoan.ten_dang_nhap} ({tai_khoan.vai_tro}).")
                    return tai_khoan
            print(f"Sai tên đăng nhập hoặc mật khẩu. (Lần {lan}/{SO_LAN_THU_TOI_DA})")
        print("Bạn đã nhập sai quá nhiều lần, quay về menu đầu.")
        return None

    @staticmethod
    def dang_ky(danh_sach_tai_khoan, csdl):
        print("\n----- ĐĂNG KÝ TÀI KHOẢN -----")
        ten = tien_ich.nhap_chuoi("Tên đăng nhập (Enter để hủy)", bat_buoc=False)
        if not ten:
            print("Đã hủy đăng ký.")
            return
        if any(tk.ten_dang_nhap.casefold() == ten.casefold() for tk in danh_sach_tai_khoan):
            print("Tên đăng nhập đã tồn tại.")
            return
        mat_khau = input("Mật khẩu: ")
        if not mat_khau.strip():
            print("Mật khẩu không được để trống.")
            return
        # Quyền không nhận từ dữ liệu nhập; tài khoản tự đăng ký luôn là user.
        tai_khoan = TaiKhoan(ten, mat_khau, "user", 0)
        danh_sach_tai_khoan.append(tai_khoan)
        try:
            csdl.ghi_tai_khoan(danh_sach_tai_khoan)
        except OSError as loi:
            danh_sach_tai_khoan.remove(tai_khoan)
            print(f"Đăng ký thất bại: không ghi được dữ liệu ({loi}).")
            return
        print("Đăng ký thành công. Số dư ban đầu: 0 VNĐ.")

    def chuyen_thanh_dong_csv(self):
        """Chuyển thành dict để ghi vào accounts.csv."""
        return {"ten_dang_nhap": self.ten_dang_nhap, "mat_khau": self.mat_khau, "vai_tro": self.vai_tro, "so_du": self.so_du}

    @classmethod
    def tu_dong_csv(cls, dong):
        """Tạo TaiKhoan từ một dòng CSV. Trả về None nếu dòng thiếu dữ liệu."""
        ten = (dong.get("ten_dang_nhap") or "").strip()
        mat_khau = dong.get("mat_khau") or ""
        vai_tro = (dong.get("vai_tro") or "user").strip().lower()
        if not ten or not mat_khau:
            return None
        if vai_tro not in ("admin", "user"):
            vai_tro = "user"
        try:
            so_du = int(dong.get("so_du") or 0)
        except (TypeError, ValueError):
            so_du = 0
        return cls(ten, mat_khau, vai_tro, so_du)
