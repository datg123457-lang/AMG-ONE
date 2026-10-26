"""Gacha mô hình: dùng trực tiếp danh sách sản phẩm đang bán."""
import os
import random
from datetime import datetime

import tien_ich

GIA_QUAY = 4_000_000


class QuanLyGacha:
    def __init__(self, csdl, ql_san_pham):
        self.csdl = csdl
        self.ql_san_pham = ql_san_pham

    def _san_pham_hop_le(self):
        ket_qua = []
        for sp in self.ql_san_pham.danh_sach:
            hop_le, _ = sp.kiem_tra_hop_le()
            if hop_le and sp.gia > 0 and sp.so_luong > 0:
                ket_qua.append(sp)
        return ket_qua

    def quay(self, tai_khoan):
        print("\n----- GACHA MÔ HÌNH -----")
        danh_sach = self._san_pham_hop_le()
        if not danh_sach:
            print("Hiện chưa có sản phẩm hợp lệ để quay.")
            return
        print("Danh sách sản phẩm có thể nhận:")
        self.ql_san_pham.hien_thi_danh_sach(danh_sach)
        print(f"Giá quay: {tien_ich.dinh_dang_gia(GIA_QUAY)} / lượt")
        print(f"Số dư ví: {tien_ich.dinh_dang_gia(tai_khoan.so_du)}")
        if tai_khoan.so_du < GIA_QUAY:
            print("Số dư không đủ để quay Gacha.")
            return
        if not tien_ich.xac_nhan("Xác nhận quay một lượt?"):
            print("Đã hủy. Ví tiền và tồn kho không thay đổi.")
            return

        # Giá được chuẩn hóa theo triệu VNĐ; công thức vẫn tương đương w = 1/gia.
        danh_sach = self._san_pham_hop_le()
        if not danh_sach:
            print("Không còn sản phẩm hợp lệ để quay.")
            return
        trong_so = [1 / (sp.gia / 1_000_000) for sp in danh_sach]
        trung = random.choices(danh_sach, weights=trong_so, k=1)[0]
        if trung not in self.ql_san_pham.danh_sach or trung.so_luong <= 0 or trung.gia <= 0:
            print("Sản phẩm vừa thay đổi trạng thái. Vui lòng thử lại; ví tiền không thay đổi.")
            return

        file_du_phong = {}
        for path in (self.csdl.file_san_pham, self.csdl.file_tai_khoan, self.csdl.file_gacha):
            try:
                with open(path, "rb") as f:
                    file_du_phong[path] = f.read()
            except FileNotFoundError:
                file_du_phong[path] = None
        so_du_cu, so_luong_cu = tai_khoan.so_du, trung.so_luong
        tai_khoan.so_du -= GIA_QUAY
        trung.so_luong -= 1
        ds_tk = self.csdl.doc_tai_khoan()
        for tk in ds_tk:
            if tk.ten_dang_nhap == tai_khoan.ten_dang_nhap:
                tk.so_du = tai_khoan.so_du
        ds_lich_su = self.csdl.doc_lich_su_gacha()
        ma_luot = f"GC{len(ds_lich_su) + 1:04d}"
        dong = {
            "ma_luot_quay": ma_luot,
            "nguoi_quay": tai_khoan.ten_dang_nhap,
            "ma_sp": trung.ma_sp,
            "ten_sp": trung.ten_sp,
            "gia_tri": trung.gia,
            "gia_quay": GIA_QUAY,
            "thoi_gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        try:
            self.csdl.ghi_san_pham(self.ql_san_pham.danh_sach)
            self.csdl.ghi_tai_khoan(ds_tk)
            self.csdl.them_lich_su_gacha(dong)
        except (OSError, ValueError) as loi:
            tai_khoan.so_du = so_du_cu
            trung.so_luong = so_luong_cu
            for path, content in file_du_phong.items():
                try:
                    if content is None:
                        if os.path.exists(path): os.remove(path)
                    else:
                        with open(path, "wb") as f: f.write(content)
                except OSError:
                    pass
            print(f"Lượt quay thất bại; đã thử khôi phục dữ liệu. Chi tiết: {loi}")
            return
        print("\nCHÚC MỪNG! Bạn đã nhận được:")
        print(f"  {trung.ten_sp} ({trung.ma_sp})")
        print(f"  Giá trị tại thời điểm quay: {tien_ich.dinh_dang_gia(trung.gia)}")
        print(f"  Số dư còn lại: {tien_ich.dinh_dang_gia(tai_khoan.so_du)}")

    def xem_lich_su(self, tai_khoan):
        ds = self.csdl.doc_lich_su_gacha()
        if not tai_khoan.la_admin():
            ds = [dong for dong in ds if dong.get("nguoi_quay") == tai_khoan.ten_dang_nhap]
        print("\n----- LỊCH SỬ GACHA -----")
        if not ds:
            print("Chưa có lượt quay nào.")
            return
        cot = [("Mã lượt", 9, False), ("Người quay", 14, False), ("Mã SP", 7, False),
               ("Tên sản phẩm", 25, False), ("Giá trị", 16, True), ("Giá quay", 16, True), ("Thời gian", 19, False)]
        hang = [[d.get("ma_luot_quay", ""), d.get("nguoi_quay", ""), d.get("ma_sp", ""),
                 d.get("ten_sp", ""), tien_ich.dinh_dang_gia(int(d.get("gia_tri") or 0)),
                 tien_ich.dinh_dang_gia(int(d.get("gia_quay") or 0)), d.get("thoi_gian", "")] for d in ds]
        tien_ich.in_bang(cot, hang)
