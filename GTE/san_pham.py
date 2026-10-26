"""Class SanPham: một sản phẩm mô hình."""
import tien_ich


class SanPham:
    # Thứ tự cột trong data.csv
    TIEU_DE_CSV = ["ma_sp", "ten_sp", "loai_mo_hinh", "thuong_hieu", "gia", "so_luong", "mo_ta", "nguoi_ban"]

    def __init__(self, ma_sp, ten_sp, loai_mo_hinh, thuong_hieu, gia, so_luong, mo_ta, nguoi_ban):
        self.ma_sp = ma_sp
        self.ten_sp = ten_sp
        self.loai_mo_hinh = loai_mo_hinh
        self.thuong_hieu = thuong_hieu
        self.gia = gia
        self.so_luong = so_luong
        self.mo_ta = mo_ta
        self.nguoi_ban = nguoi_ban

    def hien_thi(self):
        """In đầy đủ thông tin của sản phẩm."""
        print(f"  Mã sản phẩm : {self.ma_sp}")
        print(f"  Tên sản phẩm: {self.ten_sp}")
        print(f"  Loại mô hình: {self.loai_mo_hinh}")
        print(f"  Thương hiệu : {self.thuong_hieu}")
        print(f"  Giá bán     : {tien_ich.dinh_dang_gia(self.gia)}")
        print(f"  Số lượng    : {self.so_luong}")
        print(f"  Mô tả       : {self.mo_ta if self.mo_ta else '(không có)'}")
        print(f"  Người bán   : {self.nguoi_ban}")

    def kiem_tra_hop_le(self):
        """Kiểm tra dữ liệu cơ bản. Trả về (True/False, thông báo lỗi)."""
        if not str(self.ma_sp).strip():
            return False, "Mã sản phẩm không được để trống."
        if not str(self.ten_sp).strip():
            return False, "Tên sản phẩm không được để trống."
        if not str(self.loai_mo_hinh).strip():
            return False, "Loại mô hình không được để trống."
        if not str(self.thuong_hieu).strip():
            return False, "Thương hiệu không được để trống."
        if not isinstance(self.gia, int) or self.gia <= 0:
            return False, "Giá bán phải là số nguyên lớn hơn 0."
        if not isinstance(self.so_luong, int) or self.so_luong < 0:
            return False, "Số lượng phải là số nguyên không âm."
        if not str(self.nguoi_ban).strip():
            return False, "Người bán không được để trống."
        return True, ""

    def sao_luu(self):
        """Lưu lại giá trị hiện tại để có thể khôi phục nếu cập nhật thất bại."""
        return dict(self.__dict__)

    def khoi_phuc(self, ban_sao):
        self.__dict__.update(ban_sao)

    def cap_nhat(self, ten_sp=None, loai_mo_hinh=None, thuong_hieu=None, gia=None, so_luong=None, mo_ta=None):
        """Cập nhật các trường được truyền vào (trường None thì giữ nguyên).

        Trả về (True/False, thông báo). Nếu dữ liệu mới không hợp lệ thì khôi phục dữ liệu cũ.
        """
        ban_sao = self.sao_luu()
        if ten_sp is not None:
            self.ten_sp = ten_sp
        if loai_mo_hinh is not None:
            self.loai_mo_hinh = loai_mo_hinh
        if thuong_hieu is not None:
            self.thuong_hieu = thuong_hieu
        if gia is not None:
            self.gia = gia
        if so_luong is not None:
            self.so_luong = so_luong
        if mo_ta is not None:
            self.mo_ta = mo_ta
        hop_le, thong_bao = self.kiem_tra_hop_le()
        if not hop_le:
            self.khoi_phuc(ban_sao)
        return hop_le, thong_bao

    def chuyen_thanh_dong_csv(self):
        """Chuyển thông tin sản phẩm thành dict để ghi vào CSV."""
        return {
            "ma_sp": self.ma_sp,
            "ten_sp": self.ten_sp,
            "loai_mo_hinh": self.loai_mo_hinh,
            "thuong_hieu": self.thuong_hieu,
            "gia": self.gia,
            "so_luong": self.so_luong,
            "mo_ta": self.mo_ta,
            "nguoi_ban": self.nguoi_ban,
        }

    @classmethod
    def tu_dong_csv(cls, dong):
        """Tạo SanPham từ một dòng CSV. Trả về None nếu dòng sai định dạng."""
        try:
            return cls(
                (dong["ma_sp"] or "").strip(),
                (dong["ten_sp"] or "").strip(),
                (dong["loai_mo_hinh"] or "").strip(),
                (dong["thuong_hieu"] or "").strip(),
                int(dong["gia"]),
                int(dong["so_luong"]),
                (dong.get("mo_ta") or "").strip(),
                (dong["nguoi_ban"] or "").strip(),
            )
        except (KeyError, TypeError, ValueError, AttributeError):
            return None
