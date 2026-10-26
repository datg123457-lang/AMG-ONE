"""Lớp LuuTruCSV: đọc/ghi toàn bộ dữ liệu bằng file CSV (UTF-8).

Các class quản lý chỉ gọi các phương thức công khai ở đây (doc_san_pham, ghi_san_pham, ...)
nên sau này muốn đổi sang cách lưu khác (MySQL, SQLite...) chỉ cần viết lại class này.

Quy tắc dữ liệu mẫu (nhất quán): khi data.csv / accounts.csv chưa tồn tại hoặc chưa có dòng
dữ liệu nào (file rỗng hoặc chỉ có tiêu đề) thì chương trình tạo dữ liệu mẫu.
"""
import csv
import os

from account import TaiKhoan
from giao_dich import GiaoDich
from san_pham import SanPham

# utf-8-sig: ghi UTF-8 có BOM để mở bằng Excel không lỗi tiếng Việt; đọc được cả file UTF-8 thường
MA_HOA = "utf-8-sig"

SAN_PHAM_MAU = [
    ("SP001", "Gundam RX-78-2", "Gundam", "Bandai", 450000, 10, "Mô hình RG 1/144 RX-78-2 nguyên bản", "admin"),
    ("SP002", "MG Barbatos", "Gundam", "Bandai", 1250000, 5, "Master Grade 1/100 Gundam Barbatos", "user1"),
    ("SP003", "Nendoroid Rem", "Figure", "Good Smile Company", 1850000, 3, "Nendoroid Rem (Re:Zero)", "user1"),
    ("SP004", "Hatsune Miku Figure", "Figure", "Taito", 650000, 8, "Figure Hatsune Miku bản prize", "user2"),
    ("SP005", "Optimus Prime", "Transformers", "Hasbro", 1500000, 4, "Robot biến hình Optimus Prime", "admin"),
]

TAI_KHOAN_MAU = [
    ("admin", "admin123", "admin"),
    ("user1", "user123", "user"),
    ("user2", "user123", "user"),
]


class LuuTruCSV:
    def __init__(self, thu_muc=None):
        # Mặc định lưu file cùng thư mục với chương trình, chạy từ đâu cũng được
        if thu_muc is None:
            thu_muc = os.path.dirname(os.path.abspath(__file__))
        self.file_san_pham = os.path.join(thu_muc, "data.csv")
        self.file_tai_khoan = os.path.join(thu_muc, "accounts.csv")
        self.file_giao_dich = os.path.join(thu_muc, "giao_dich.csv")

    # ---------- Hàm dùng nội bộ ----------
    def _doc_dong(self, duong_dan):
        """Đọc file CSV thành list dict. File chưa có hoặc rỗng -> list rỗng."""
        if not os.path.exists(duong_dan):
            return []
        with open(duong_dan, "r", encoding=MA_HOA, newline="") as f:
            return list(csv.DictReader(f))

    def _ghi_tat_ca(self, duong_dan, tieu_de, danh_sach_dong):
        """Ghi lại toàn bộ file. Ghi ra file tạm rồi đổi tên để không hỏng file cũ nếu bị lỗi giữa chừng."""
        file_tam = duong_dan + ".tmp"
        with open(file_tam, "w", encoding=MA_HOA, newline="") as f:
            ghi = csv.DictWriter(f, fieldnames=tieu_de)
            ghi.writeheader()
            ghi.writerows(danh_sach_dong)
        os.replace(file_tam, duong_dan)

    def _doc_danh_sach(self, duong_dan, ten_file, tao_doi_tuong):
        """Đọc file CSV thành list đối tượng, bỏ qua (và báo) các dòng sai."""
        ket_qua = []
        for so_dong, dong in enumerate(self._doc_dong(duong_dan), start=2):
            doi_tuong = tao_doi_tuong(dong)
            if doi_tuong is None:
                print(f"Cảnh báo: bỏ qua dòng {so_dong} của {ten_file} vì dữ liệu không hợp lệ.")
            else:
                ket_qua.append(doi_tuong)
        return ket_qua

    # ---------- Khởi tạo ----------
    def khoi_tao(self):
        """Tạo file + tiêu đề cột nếu chưa có; nạp dữ liệu mẫu nếu file chưa có dữ liệu."""
        if not self._doc_dong(self.file_san_pham):
            dong_mau = [SanPham(*mau).chuyen_thanh_dong_csv() for mau in SAN_PHAM_MAU]
            self._ghi_tat_ca(self.file_san_pham, SanPham.TIEU_DE_CSV, dong_mau)
        if not self._doc_dong(self.file_tai_khoan):
            dong_mau = [TaiKhoan(*mau).chuyen_thanh_dong_csv() for mau in TAI_KHOAN_MAU]
            self._ghi_tat_ca(self.file_tai_khoan, TaiKhoan.TIEU_DE_CSV, dong_mau)
        # Giao dịch: không có dữ liệu mẫu, chỉ cần có file và tiêu đề
        if not os.path.exists(self.file_giao_dich) or os.path.getsize(self.file_giao_dich) == 0:
            self._ghi_tat_ca(self.file_giao_dich, GiaoDich.TIEU_DE_CSV, [])

    # ---------- Sản phẩm ----------
    def doc_san_pham(self):
        danh_sach = []
        ma_da_co = set()
        for san_pham in self._doc_danh_sach(self.file_san_pham, "data.csv", SanPham.tu_dong_csv):
            hop_le, thong_bao = san_pham.kiem_tra_hop_le()
            if not hop_le or san_pham.ma_sp.upper() in ma_da_co:
                print(f"Cảnh báo: bỏ qua sản phẩm '{san_pham.ma_sp}' trong data.csv (dữ liệu sai hoặc trùng mã).")
                continue
            ma_da_co.add(san_pham.ma_sp.upper())
            danh_sach.append(san_pham)
        return danh_sach

    def ghi_san_pham(self, danh_sach_san_pham):
        dong = [sp.chuyen_thanh_dong_csv() for sp in danh_sach_san_pham]
        self._ghi_tat_ca(self.file_san_pham, SanPham.TIEU_DE_CSV, dong)

    # ---------- Tài khoản ----------
    def doc_tai_khoan(self):
        return self._doc_danh_sach(self.file_tai_khoan, "accounts.csv", TaiKhoan.tu_dong_csv)

    # ---------- Giao dịch ----------
    def doc_giao_dich(self):
        return self._doc_danh_sach(self.file_giao_dich, "giao_dich.csv", GiaoDich.tu_dong_csv)

    def them_giao_dich(self, giao_dich):
        """Thêm 1 giao dịch vào cuối file (không ghi đè dữ liệu cũ)."""
        if not os.path.exists(self.file_giao_dich) or os.path.getsize(self.file_giao_dich) == 0:
            self._ghi_tat_ca(self.file_giao_dich, GiaoDich.TIEU_DE_CSV, [])
        # Nếu dòng cuối của file chưa xuống dòng thì xuống dòng trước khi ghi tiếp
        with open(self.file_giao_dich, "rb") as f:
            f.seek(-1, os.SEEK_END)
            thieu_xuong_dong = f.read(1) not in (b"\n", b"\r")
        with open(self.file_giao_dich, "a", encoding=MA_HOA, newline="") as f:
            if thieu_xuong_dong:
                f.write("\r\n")
            csv.DictWriter(f, fieldnames=GiaoDich.TIEU_DE_CSV).writerow(giao_dich.chuyen_thanh_dong_csv())

    def san_pham_co_giao_dich(self, ma_sp):
        """True nếu sản phẩm đã từng phát sinh giao dịch."""
        ma_sp = ma_sp.strip().upper()
        for gd in self.doc_giao_dich():
            if gd.ma_sp.upper() == ma_sp:
                return True
        return False
