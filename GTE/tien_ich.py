"""Các hàm tiện ích dùng chung: nhập dữ liệu an toàn, định dạng giá, in bảng.

File này gom những đoạn code hay lặp lại để các class khác không phải viết lại.
"""
import re
import unicodedata


def chuan_hoa(chuoi):
    """Chuẩn hóa chuỗi: dấu tiếng Việt về dạng dựng sẵn (NFC), bỏ khoảng trắng thừa."""
    chuoi = unicodedata.normalize("NFC", str(chuoi))
    return " ".join(chuoi.split())


def bo_dau(chuoi):
    """Bỏ dấu tiếng Việt và chuyển về chữ thường (dùng cho tìm kiếm)."""
    chuoi = unicodedata.normalize("NFD", str(chuoi).lower())
    chuoi = "".join(kt for kt in chuoi if unicodedata.category(kt) != "Mn")
    return chuoi.replace("đ", "d")


def dinh_dang_gia(gia):
    """Định dạng tiền Việt Nam: 1500000 -> '1.500.000 đ'."""
    return f"{gia:,}".replace(",", ".") + " đ"


def chuyen_so_nguyen(chuoi):
    """Chuyển chuỗi thành số nguyên. Trả về None nếu không hợp lệ.

    Chấp nhận '1500000' hoặc '1.500.000' (dấu . hoặc , ngăn cách hàng nghìn).
    Chuỗi như '1.5' bị từ chối để tránh hiểu nhầm thành 15.
    """
    chuoi = str(chuoi).strip().replace(" ", "")
    if re.fullmatch(r"[+-]?[0-9]+", chuoi) or re.fullmatch(r"[+-]?[0-9]{1,3}([.,][0-9]{3})+", chuoi):
        return int(re.sub(r"[.,]", "", chuoi))
    return None


def nhap_chuoi(thong_bao, mac_dinh=None, bat_buoc=True):
    """Nhập một chuỗi từ bàn phím.

    - mac_dinh: nếu có, nhấn Enter sẽ giữ nguyên giá trị này (dùng khi sửa).
    - bat_buoc: True thì không cho để trống (khi không có mac_dinh).
    """
    while True:
        if mac_dinh:
            gia_tri = chuan_hoa(input(f"{thong_bao} [{mac_dinh}]: "))
        else:
            gia_tri = chuan_hoa(input(f"{thong_bao}: "))
        if gia_tri:
            return gia_tri
        if mac_dinh is not None:
            return mac_dinh
        if not bat_buoc:
            return ""
        print("  Không được để trống, vui lòng nhập lại.")


def nhap_so_nguyen(thong_bao, toi_thieu=0, mac_dinh=None, cho_phep_trong=False):
    """Nhập một số nguyên >= toi_thieu, nhập sai thì hỏi lại (không làm chương trình dừng).

    - mac_dinh: nhấn Enter sẽ giữ nguyên giá trị cũ.
    - cho_phep_trong: nhấn Enter trả về None (dùng cho ô tùy chọn / hủy thao tác).
    """
    while True:
        if mac_dinh is not None:
            dong = input(f"{thong_bao} [{mac_dinh}]: ")
        else:
            dong = input(f"{thong_bao}: ")
        if not dong.strip():
            if mac_dinh is not None:
                return mac_dinh
            if cho_phep_trong:
                return None
            print("  Không được để trống, vui lòng nhập lại.")
            continue
        so = chuyen_so_nguyen(dong)
        if so is None:
            print("  Vui lòng nhập số nguyên (ví dụ: 1500000 hoặc 1.500.000).")
        elif so < toi_thieu:
            print(f"  Giá trị phải từ {toi_thieu} trở lên.")
        else:
            return so


def xac_nhan(thong_bao):
    """Hỏi có/không. Trả về True nếu người dùng đồng ý."""
    while True:
        tra_loi = chuan_hoa(input(f"{thong_bao} (c/k): ")).lower()
        if tra_loi in ("c", "co", "có", "y", "yes"):
            return True
        if tra_loi in ("k", "khong", "không", "n", "no"):
            return False
        print("  Vui lòng nhập c (có) hoặc k (không).")


def tam_dung():
    """Dừng màn hình để người dùng đọc kết quả."""
    input("\nNhấn Enter để tiếp tục...")


def cat_chuoi(chuoi, do_rong):
    """Cắt chuỗi quá dài và thêm '...' để bảng không bị lệch."""
    if len(chuoi) <= do_rong:
        return chuoi
    return chuoi[:do_rong - 3] + "..."


def in_bang(cot, hang):
    """In bảng văn bản.

    cot : danh sách (tiêu đề, độ rộng, căn phải?)
    hang: danh sách các dòng, mỗi dòng là danh sách giá trị theo thứ tự cột.
    """
    tieu_de = " | ".join(ten.ljust(rong) for ten, rong, _ in cot)
    print(tieu_de)
    print("-" * len(tieu_de))
    for dong in hang:
        cac_o = []
        for (_, rong, can_phai), gia_tri in zip(cot, dong):
            gia_tri = cat_chuoi(str(gia_tri), rong)
            cac_o.append(gia_tri.rjust(rong) if can_phai else gia_tri.ljust(rong))
        print(" | ".join(cac_o))
