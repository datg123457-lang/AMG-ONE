"""Class TaiKhoan: thông tin tài khoản và chức năng đăng nhập."""
import getpass

import tien_ich

SO_LAN_THU_TOI_DA = 3


class TaiKhoan:
    TIEU_DE_CSV = ["ten_dang_nhap", "mat_khau", "vai_tro"]

    def __init__(self, ten_dang_nhap, mat_khau, vai_tro="user"):
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro  # "admin" hoặc "user"

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
            mat_khau = getpass.getpass("Mật khẩu: ")
            for tai_khoan in danh_sach_tai_khoan:
                if tai_khoan.kiem_tra_dang_nhap(ten, mat_khau):
                    print(f"Đăng nhập thành công! Xin chào {tai_khoan.ten_dang_nhap} ({tai_khoan.vai_tro}).")
                    return tai_khoan
            print(f"Sai tên đăng nhập hoặc mật khẩu. (Lần {lan}/{SO_LAN_THU_TOI_DA})")
        print("Bạn đã nhập sai quá nhiều lần, quay về menu đầu.")
        return None

    def chuyen_thanh_dong_csv(self):
        """Chuyển thành dict để ghi vào accounts.csv."""
        return {"ten_dang_nhap": self.ten_dang_nhap, "mat_khau": self.mat_khau, "vai_tro": self.vai_tro}

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
        return cls(ten, mat_khau, vai_tro)
