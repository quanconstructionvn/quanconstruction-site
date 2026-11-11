# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Tạo 12 biểu mẫu Word (mẫu tham khảo, để trống) cho trang /so-tay-xay-dung/bieu-mau.html
# Chạy từ thư mục gốc website:  python3 _cong-cu/tao-bieu-mau.py   -> so-tay-xay-dung/bieu-mau/*.docx
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "so-tay-xay-dung", "bieu-mau")
CHAM = "……………………………………………………"
NGAN = "…………………"


def moi():
    d = Document()
    s = d.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(3), Cm(2), Cm(2), Cm(2)
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"; st.font.size = Pt(13)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.paragraph_format.space_after = Pt(3)
    d.core_properties.author = "Quang Mai Phú"
    d.core_properties.comments = "Mẫu tham khảo – Quan Construction biên soạn (quanconstruction.biz.vn/so-tay-xay-dung/bieu-mau.html)"
    p = d.add_paragraph(); r = p.add_run("Mẫu tham khảo – Quan Construction biên soạn"); r.italic = True; r.font.size = Pt(9)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    return d


def dau(d, ben="TÊN ĐƠN VỊ LẬP", so="Số: ……/……"):
    t = d.add_table(rows=1, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    a, b = t.rows[0].cells
    a.width, b.width = Cm(6.5), Cm(9.5)
    pa = a.paragraphs[0]; pa.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = pa.add_run(ben + "\n" + NGAN); r.bold = True; r.font.size = Pt(12)
    pa2 = a.add_paragraph(so); pa2.alignment = WD_ALIGN_PARAGRAPH.CENTER; pa2.runs[0].font.size = Pt(12)
    pb = b.paragraphs[0]; pb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = pb.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n"); r.bold = True; r.font.size = Pt(12)
    r = pb.add_run("Độc lập - Tự do - Hạnh phúc"); r.bold = True; r.underline = True; r.font.size = Pt(13)
    pb2 = b.add_paragraph("……, ngày …… tháng …… năm ……"); pb2.alignment = WD_ALIGN_PARAGRAPH.CENTER; pb2.runs[0].italic = True
    d.add_paragraph()


def tieu_de(d, ten, phu=None):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(ten); r.bold = True; r.font.size = Pt(14)
    if phu:
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(phu); r.italic = True; r.font.size = Pt(12)


def muc(d, chu):
    p = d.add_paragraph(); r = p.add_run(chu); r.bold = True
    p.paragraph_format.space_before = Pt(6)


def dong(d, nhan, dai=True):
    d.add_paragraph(f"{nhan}: " + (CHAM if dai else NGAN))


def bang(d, cot, so_dong=4, rong=None):
    t = d.add_table(rows=1 + so_dong, cols=len(cot)); t.style = "Table Grid"
    for i, c in enumerate(cot):
        cell = t.rows[0].cells[i]; cell.text = ""; r = cell.paragraphs[0].add_run(c); r.bold = True; r.font.size = Pt(12)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row in t.rows[1:]:
        for cell in row.cells: cell.paragraphs[0].add_run(" ").font.size = Pt(12)
    if rong:
        for row in t.rows:
            for i, w in enumerate(rong): row.cells[i].width = Cm(w)
    d.add_paragraph()
    return t


def ky(d, ben):
    t = d.add_table(rows=1, cols=len(ben))
    for i, b in enumerate(ben):
        p = t.rows[0].cells[i].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(b + "\n"); r.bold = True; r.font.size = Pt(12)
        r = p.add_run("(Ký, ghi rõ họ tên, chức vụ" + (", đóng dấu)" if "ĐẠI DIỆN" in b else ")")); r.italic = True; r.font.size = Pt(11)


def thanh_phan(d, ds):
    bang(d, ["Bên / vai trò", "Họ và tên", "Chức vụ"], 0, [7.5, 4.5, 4])
    t = d.tables[-1]
    for b in ds:
        cells = t.add_row().cells; cells[0].text = b; cells[1].text = ""; cells[2].text = ""
        for c in cells: c.paragraphs[0].runs and setattr(c.paragraphs[0].runs[0].font, "size", Pt(12))


def thong_tin_ct(d):
    dong(d, "Công trình"); dong(d, "Hạng mục"); dong(d, "Địa điểm xây dựng")


def luu(d, ten):
    # áp độ rộng cột của dòng đầu cho mọi dòng (kể cả dòng thêm sau)
    for t in d.tables:
        t.autofit = False
        w = [c.width for c in t.rows[0].cells]
        if all(w):
            for i, col in enumerate(t.columns):
                col.width = w[i]
            for row in t.rows:
                for i, c in enumerate(row.cells):
                    if i < len(w): c.width = w[i]
    os.makedirs(OUT, exist_ok=True)
    d.save(os.path.join(OUT, ten + ".docx"))


GS_CDT = "Người trực tiếp giám sát thi công xây dựng của chủ đầu tư"
KT_NT = "Người trực tiếp phụ trách kỹ thuật thi công của nhà thầu thi công (nhà thầu chính)"
KT_NTP = "Người trực tiếp phụ trách kỹ thuật thi công của nhà thầu phụ (nếu có)"


def phieu_yeu_cau_nghiem_thu():
    d = moi(); dau(d, "NHÀ THẦU THI CÔNG"); tieu_de(d, "PHIẾU YÊU CẦU NGHIỆM THU", "(công việc xây dựng / vật liệu, thiết bị / giai đoạn)")
    d.add_paragraph("Kính gửi: " + CHAM + " (chủ đầu tư / tư vấn giám sát)")
    thong_tin_ct(d)
    muc(d, "1. Đối tượng đề nghị nghiệm thu"); dong(d, "Tên công việc / vật liệu / bộ phận"); dong(d, "Vị trí, trục, cao độ")
    muc(d, "2. Thời gian đề nghị nghiệm thu"); d.add_paragraph("Vào lúc …… giờ …… ngày …… tháng …… năm …… tại công trường.")
    muc(d, "3. Tài liệu kèm theo");
    for x in ["Bản vẽ thi công / bản vẽ hoàn công phần việc: " + NGAN, "Kết quả thí nghiệm, kiểm tra (nếu có): " + NGAN, "Nhật ký thi công các ngày: " + NGAN, "Biên bản nghiệm thu nội bộ của nhà thầu (nếu có): " + NGAN]:
        d.add_paragraph(x, style="List Bullet")
    d.add_paragraph("Nhà thầu đã tự kiểm tra và xác nhận phần việc trên đạt yêu cầu thiết kế, chỉ dẫn kỹ thuật; đề nghị bên giám sát tổ chức nghiệm thu.")
    p = d.add_paragraph("Lưu ý: người giám sát thi công thực hiện nghiệm thu công việc xây dựng trong không quá 24 giờ kể từ khi nhận được đề nghị; không đồng ý phải thông báo lý do bằng văn bản (khoản 3 Điều 22 Nghị định 207/2026/NĐ-CP).")
    p.runs[0].italic = True; p.runs[0].font.size = Pt(11)
    muc(d, "Ý kiến tiếp nhận của bên giám sát"); d.add_paragraph(CHAM); d.add_paragraph("Thời điểm nhận phiếu: …… giờ …… ngày ……/……/……")
    ky(d, ["BÊN GIÁM SÁT TIẾP NHẬN", "NHÀ THẦU THI CÔNG"]); luu(d, "phieu-yeu-cau-nghiem-thu")


def bb_vat_lieu():
    d = moi(); dau(d, "BAN QUẢN LÝ / CHỦ ĐẦU TƯ"); tieu_de(d, "BIÊN BẢN NGHIỆM THU VẬT LIỆU, SẢN PHẨM, CẤU KIỆN, THIẾT BỊ ĐƯA VÀO CÔNG TRÌNH")
    thong_tin_ct(d)
    muc(d, "1. Đối tượng nghiệm thu")
    bang(d, ["STT", "Tên vật liệu / thiết bị", "Chủng loại, quy cách", "Nguồn gốc, nhà sản xuất", "Đơn vị", "Số lượng"], 4, [1.2, 4, 3.2, 3.2, 1.6, 1.8])
    muc(d, "2. Thời gian, địa điểm nghiệm thu"); d.add_paragraph("Bắt đầu: …… giờ …… ngày ……/……/……   Kết thúc: …… giờ …… ngày ……/……/……   Tại: " + NGAN)
    muc(d, "3. Thành phần trực tiếp nghiệm thu"); thanh_phan(d, [GS_CDT, KT_NT, "Đại diện nhà thầu cung ứng / sản xuất (nếu có)"])
    muc(d, "4. Căn cứ và tài liệu kiểm tra")
    for x in ["Yêu cầu của thiết kế, chỉ dẫn kỹ thuật, hợp đồng: " + NGAN, "Chứng chỉ xuất xưởng, chứng nhận chất lượng (CO, CQ): " + NGAN, "Giấy chứng nhận hợp quy / công bố hợp quy (nếu thuộc danh mục phải công bố): " + NGAN, "Kết quả thí nghiệm mẫu (nếu có): " + NGAN]:
        d.add_paragraph(x, style="List Bullet")
    muc(d, "5. Đánh giá"); bang(d, ["Nội dung kiểm tra", "Yêu cầu", "Kết quả", "Đạt / Không đạt"], 4, [5, 4, 4, 2.5])
    muc(d, "6. Kết luận"); d.add_paragraph("☐ Chấp nhận nghiệm thu, cho phép sử dụng vào công trình.   ☐ Không chấp nhận, yêu cầu: " + CHAM)
    ky(d, ["GIÁM SÁT THI CÔNG", "KỸ THUẬT NHÀ THẦU", "NHÀ CUNG ỨNG"]); luu(d, "bien-ban-nghiem-thu-vat-lieu-thiet-bi")


def bb_cong_viec():
    d = moi(); dau(d, "BAN QUẢN LÝ / CHỦ ĐẦU TƯ"); tieu_de(d, "BIÊN BẢN NGHIỆM THU CÔNG VIỆC XÂY DỰNG")
    muc(d, "1. Tên công việc được nghiệm thu"); thong_tin_ct(d); dong(d, "Công việc nghiệm thu"); dong(d, "Vị trí, trục, cao độ"); dong(d, "Theo phiếu yêu cầu nghiệm thu số", False)
    muc(d, "2. Thời gian và địa điểm nghiệm thu"); d.add_paragraph("Bắt đầu: …… giờ …… ngày ……/……/……   Kết thúc: …… giờ …… ngày ……/……/……   Tại: công trường")
    muc(d, "3. Thành phần ký biên bản nghiệm thu"); thanh_phan(d, [GS_CDT, KT_NT, KT_NTP])
    muc(d, "4. Căn cứ nghiệm thu")
    for x in ["Hồ sơ thiết kế bản vẽ thi công số " + NGAN + " và chỉ dẫn kỹ thuật được phê duyệt; thay đổi thiết kế đã được chấp thuận", "Quy chuẩn, tiêu chuẩn áp dụng: " + NGAN, "Kết quả kiểm tra, thí nghiệm vật liệu, thiết bị: " + NGAN, "Kết quả quan trắc (nếu có): " + NGAN, "Nhật ký thi công, biên bản nghiệm thu vật liệu liên quan: " + NGAN]:
        d.add_paragraph(x, style="List Bullet")
    muc(d, "5. Đánh giá công việc đã thực hiện"); bang(d, ["Nội dung kiểm tra", "Yêu cầu", "Kết quả", "Đạt / Không đạt"], 5, [5, 4, 4, 2.5])
    muc(d, "6. Kết luận nghiệm thu")
    d.add_paragraph("☐ Chấp nhận nghiệm thu, đồng ý cho triển khai các công việc tiếp theo.")
    d.add_paragraph("☐ Không chấp nhận nghiệm thu. Yêu cầu sửa chữa, hoàn thiện: " + CHAM)
    d.add_paragraph("Ý kiến khác (nếu có): " + CHAM)
    muc(d, "7. Phụ lục kèm theo (nếu có)"); d.add_paragraph(CHAM)
    ky(d, ["GIÁM SÁT THI CÔNG CỦA CHỦ ĐẦU TƯ", "KỸ THUẬT NHÀ THẦU CHÍNH", "KỸ THUẬT NHÀ THẦU PHỤ"]); luu(d, "bien-ban-nghiem-thu-cong-viec")


def bb_giai_doan():
    d = moi(); dau(d, "BAN QUẢN LÝ / CHỦ ĐẦU TƯ"); tieu_de(d, "BIÊN BẢN NGHIỆM THU GIAI ĐOẠN THI CÔNG / BỘ PHẬN CÔNG TRÌNH")
    muc(d, "1. Đối tượng nghiệm thu"); thong_tin_ct(d); dong(d, "Giai đoạn / bộ phận công trình (hoặc gói thầu)")
    muc(d, "2. Thời gian và địa điểm nghiệm thu"); d.add_paragraph("Bắt đầu: …… giờ …… ngày ……/……/……   Kết thúc: …… giờ …… ngày ……/……/……   Tại: " + NGAN)
    muc(d, "3. Thành phần tham gia nghiệm thu"); thanh_phan(d, ["Giám sát trưởng", "Đại diện chủ đầu tư", "Đại diện nhà thầu thi công", "Thành phần khác theo thỏa thuận (thiết kế, nhà thầu phụ…)"])
    muc(d, "4. Hồ sơ, tài liệu làm căn cứ")
    for x in ["Các biên bản nghiệm thu công việc xây dựng thuộc giai đoạn / bộ phận: từ số …… đến số ……", "Kết quả thí nghiệm, kiểm tra, kiểm định, thử nghiệm, chạy thử: " + NGAN, "Bản vẽ hoàn công giai đoạn / bộ phận: " + NGAN, "Văn bản pháp lý liên quan trong giai đoạn thi công (nếu có): " + NGAN]:
        d.add_paragraph(x, style="List Bullet")
    muc(d, "5. Đánh giá theo điều kiện nghiệm thu đã thỏa thuận"); bang(d, ["Điều kiện / nội dung", "Kết quả kiểm tra", "Đạt / Không đạt"], 4, [7, 6, 2.5])
    muc(d, "6. Kết luận"); d.add_paragraph("☐ Chấp nhận nghiệm thu, đồng ý chuyển sang giai đoạn thi công tiếp theo.   ☐ Không chấp nhận, yêu cầu: " + CHAM)
    ky(d, ["GIÁM SÁT TRƯỞNG", "ĐẠI DIỆN CHỦ ĐẦU TƯ", "ĐẠI DIỆN NHÀ THẦU"]); luu(d, "bien-ban-nghiem-thu-giai-doan")


def bb_hoan_thanh():
    d = moi(); dau(d, "CHỦ ĐẦU TƯ"); tieu_de(d, "BIÊN BẢN NGHIỆM THU HOÀN THÀNH HẠNG MỤC CÔNG TRÌNH / CÔNG TRÌNH XÂY DỰNG ĐƯA VÀO SỬ DỤNG")
    muc(d, "1. Hạng mục công trình / công trình được nghiệm thu"); thong_tin_ct(d); d.add_paragraph("☐ Toàn bộ   ☐ Một phần công trình (ghi rõ): " + NGAN + "   ☐ Nghiệm thu có điều kiện")
    muc(d, "2. Thời gian và địa điểm nghiệm thu"); d.add_paragraph("Bắt đầu: …… giờ …… ngày ……/……/……   Kết thúc: …… giờ …… ngày ……/……/……   Tại: " + NGAN)
    muc(d, "3. Thành phần ký biên bản nghiệm thu"); thanh_phan(d, ["Người đại diện theo pháp luật của chủ đầu tư hoặc người được ủy quyền", "Người đại diện theo pháp luật của nhà thầu giám sát thi công xây dựng hoặc người được ủy quyền", "Người đại diện theo pháp luật của nhà thầu thi công xây dựng chính hoặc người được ủy quyền", "Thành phần khác (nếu có)"])
    muc(d, "4. Đánh giá việc đáp ứng các điều kiện nghiệm thu")
    bang(d, ["Điều kiện", "Đánh giá"], 0, [9.5, 6]); t = d.tables[-1]
    for x in ["Công việc xây dựng đã thi công đầy đủ theo hồ sơ thiết kế được phê duyệt", "Đã nghiệm thu đầy đủ công việc, bộ phận, giai đoạn trong quá trình thi công", "Kết quả thí nghiệm, quan trắc, kiểm tra, kiểm định, thử nghiệm, chạy thử đạt yêu cầu thiết kế", "Tuân thủ quy định về PCCC và CNCH, bảo vệ môi trường và pháp luật chuyên ngành", "Sự phù hợp so với thiết kế, chỉ dẫn kỹ thuật và yêu cầu khác của hợp đồng"]:
        c = t.add_row().cells; c[0].text = x; c[1].text = ""
    d.add_paragraph()
    muc(d, "5. Đánh giá sự phù hợp với thiết kế đã thẩm định về phòng cháy, chữa cháy")
    d.add_paragraph("(khoảng cách PCCC; đường, bãi đỗ, khoảng trống cho xe chữa cháy; giải pháp thoát nạn; bậc chịu lửa, ngăn cháy, chống cháy lan; chống khói…) " + CHAM)
    muc(d, "6. Kết luận nghiệm thu"); d.add_paragraph("☐ Chấp thuận nghiệm thu hoàn thành, đưa vào sử dụng.   ☐ Không chấp thuận.")
    d.add_paragraph("Yêu cầu sửa chữa, hoàn thiện bổ sung / tồn tại cần khắc phục và thời hạn (nếu có): " + CHAM)
    muc(d, "7. Bảo hành"); d.add_paragraph("Thời điểm bắt đầu tính bảo hành: ngày ……/……/……   Thời gian bảo hành: …… tháng.")
    muc(d, "8. Phụ lục kèm theo (nếu có)"); d.add_paragraph(CHAM)
    ky(d, ["ĐẠI DIỆN CHỦ ĐẦU TƯ", "ĐẠI DIỆN GIÁM SÁT", "ĐẠI DIỆN NHÀ THẦU THI CÔNG"]); luu(d, "bien-ban-nghiem-thu-hoan-thanh")


def nhat_ky():
    d = moi()
    for _ in range(4): d.add_paragraph()
    tieu_de(d, "NHẬT KÝ THI CÔNG XÂY DỰNG CÔNG TRÌNH", "Quyển số: ……")
    d.add_paragraph()
    for x in ["Công trình", "Hạng mục", "Địa điểm xây dựng", "Chủ đầu tư", "Nhà thầu giám sát thi công", "Nhà thầu thi công", "Chỉ huy trưởng công trường", "Ngày khởi công"]:
        dong(d, x)
    d.add_paragraph("Nhật ký gồm …… trang, đánh số từ 01 đến ……, đóng dấu giáp lai của nhà thầu thi công.")
    p = d.add_paragraph("Ghi chú: nhà thầu lập nhật ký thi công theo Phụ lục II Nghị định 207/2026/NĐ-CP; khi hợp đồng hoặc chủ đầu tư yêu cầu mẫu cụ thể thì dùng mẫu đó."); p.runs[0].italic = True; p.runs[0].font.size = Pt(11)
    ky(d, ["ĐẠI DIỆN CHỦ ĐẦU TƯ", "ĐẠI DIỆN NHÀ THẦU THI CÔNG"])
    d.add_page_break()
    tieu_de(d, "TRANG NHẬT KÝ – NGÀY ……/……/……")
    d.add_paragraph("Thời tiết: sáng " + NGAN + "  chiều " + NGAN + "   Nhiệt độ: ……")
    muc(d, "1. Nhân lực, máy, thiết bị trên công trường"); bang(d, ["Loại", "Số lượng", "Ghi chú"], 4, [7, 3, 5.5])
    muc(d, "2. Công việc thực hiện trong ngày (vị trí, khối lượng)"); d.add_paragraph(CHAM); d.add_paragraph(CHAM)
    muc(d, "3. Vật liệu, thiết bị nhập về công trường; thí nghiệm, kiểm tra"); d.add_paragraph(CHAM)
    muc(d, "4. Nghiệm thu trong ngày"); d.add_paragraph(CHAM)
    muc(d, "5. Sai sót, sự cố, an toàn lao động và biện pháp xử lý"); d.add_paragraph(CHAM)
    muc(d, "6. Ý kiến, yêu cầu của giám sát / thiết kế / chủ đầu tư"); d.add_paragraph(CHAM)
    ky(d, ["GIÁM SÁT THI CÔNG", "KỸ THUẬT THI CÔNG NHÀ THẦU"]); luu(d, "nhat-ky-thi-cong")


def bao_cao_ngay():
    d = moi(); dau(d, "NHÀ THẦU THI CÔNG"); tieu_de(d, "BÁO CÁO THI CÔNG NGÀY", "Ngày ……/……/……")
    d.add_paragraph("Kính gửi: " + CHAM); thong_tin_ct(d)
    muc(d, "1. Tiến độ công việc"); bang(d, ["Công việc", "Vị trí", "KL kế hoạch", "KL thực hiện", "Lũy kế (%)", "Ghi chú"], 5, [4, 2.6, 2.2, 2.2, 2, 2.5])
    muc(d, "2. Nhân lực, máy thi công"); d.add_paragraph("Nhân lực: …… người (kỹ sư ……, công nhân ……).   Máy: " + NGAN)
    muc(d, "3. Vật tư nhập / sử dụng"); bang(d, ["Vật tư", "Đơn vị", "Nhập", "Sử dụng", "Tồn"], 3, [5, 2, 2.5, 2.5, 2.5])
    muc(d, "4. Chất lượng, nghiệm thu, an toàn, vệ sinh môi trường"); d.add_paragraph(CHAM)
    muc(d, "5. Vướng mắc, kiến nghị"); d.add_paragraph(CHAM)
    muc(d, "6. Kế hoạch ngày tiếp theo"); d.add_paragraph(CHAM)
    ky(d, ["NGƯỜI LẬP", "CHỈ HUY TRƯỞNG CÔNG TRƯỜNG"]); luu(d, "bao-cao-ngay")


def de_nghi_thanh_toan():
    d = moi(); dau(d, "BÊN NHẬN THẦU"); tieu_de(d, "ĐỀ NGHỊ THANH TOÁN", "Lần thanh toán thứ: ……   Giai đoạn: từ ……/……/…… đến ……/……/……")
    d.add_paragraph("Kính gửi: " + CHAM + " (bên giao thầu)")
    dong(d, "Hợp đồng số", False); d.add_paragraph("ngày ……/……/……   Loại giá hợp đồng: ☐ trọn gói  ☐ đơn giá cố định  ☐ đơn giá điều chỉnh  ☐ theo thời gian  ☐ khác")
    thong_tin_ct(d)
    muc(d, "1. Giá trị đề nghị thanh toán (đồng)")
    bang(d, ["STT", "Nội dung", "Giá trị (đồng)"], 0, [1.2, 10, 4.3]); t = d.tables[-1]
    for i, x in enumerate(["Giá trị hợp đồng (kể cả phụ lục điều chỉnh, nếu có)", "Giá trị khối lượng hoàn thành theo hợp đồng trong giai đoạn", "Giá trị khối lượng công việc phát sinh (nếu có)", "Giá trị điều chỉnh giá (nếu có, theo thỏa thuận hợp đồng)", "Giảm trừ tiền tạm ứng", "Các khoản giảm trừ khác (giữ lại, phạt… theo hợp đồng)", "Giá trị đề nghị thanh toán kỳ này (= 2 + 3 + 4 – 5 – 6)", "Lũy kế giá trị đã thanh toán đến kỳ trước", "Lũy kế sau kỳ này"], 1):
        c = t.add_row().cells; c[0].text = str(i); c[1].text = x; c[2].text = ""
    d.add_paragraph("Bằng chữ: " + CHAM)
    muc(d, "2. Hồ sơ kèm theo")
    for x in ["Biên bản nghiệm thu khối lượng, công việc hoàn thành trong giai đoạn thanh toán", "Bảng xác định giá trị khối lượng hoàn thành / bảng tính giá trị công việc phát sinh, công việc chưa có đơn giá (nếu có)", "Bảng tính điều chỉnh giá (nếu có)", "Tài liệu khác theo hợp đồng: " + NGAN]:
        d.add_paragraph(x, style="List Bullet")
    muc(d, "3. Thông tin nhận tiền"); dong(d, "Tài khoản số", False); dong(d, "Tại ngân hàng")
    ky(d, ["XÁC NHẬN CỦA BÊN GIAO THẦU / TƯ VẤN", "ĐẠI DIỆN BÊN NHẬN THẦU"]); luu(d, "de-nghi-thanh-toan")


def bang_khoi_luong():
    d = moi(); dau(d, "BÊN NHẬN THẦU"); tieu_de(d, "BẢNG XÁC ĐỊNH GIÁ TRỊ KHỐI LƯỢNG HOÀN THÀNH", "Đề nghị thanh toán lần ……   Giai đoạn: từ ……/……/…… đến ……/……/……")
    dong(d, "Hợp đồng số", False); thong_tin_ct(d)
    bang(d, ["STT", "Tên công việc", "Đơn vị", "KL theo hợp đồng", "KL lũy kế đến kỳ trước", "KL thực hiện kỳ này", "Đơn giá", "Thành tiền kỳ này"], 6, [1, 4, 1.4, 1.8, 1.9, 1.8, 1.8, 2.3])
    d.add_paragraph("Tổng giá trị kỳ này: ……………… đồng.   Bằng chữ: " + CHAM)
    d.add_paragraph("Công việc phát sinh ngoài hợp đồng / chưa có đơn giá (nếu có): lập bảng riêng thể hiện khối lượng và đơn giá.")
    ky(d, ["ĐẠI DIỆN BÊN GIAO THẦU", "ĐẠI DIỆN TƯ VẤN GIÁM SÁT", "ĐẠI DIỆN BÊN NHẬN THẦU"]); luu(d, "bang-xac-dinh-khoi-luong-hoan-thanh")


def bb_ban_giao():
    d = moi(); dau(d, "CHỦ ĐẦU TƯ"); tieu_de(d, "BIÊN BẢN BÀN GIAO HẠNG MỤC CÔNG TRÌNH / CÔNG TRÌNH XÂY DỰNG")
    thong_tin_ct(d)
    muc(d, "1. Thành phần"); d.add_paragraph("Bên giao: " + CHAM); d.add_paragraph("Bên nhận: " + CHAM)
    thanh_phan(d, ["Đại diện bên giao", "Đại diện bên nhận", "Thành phần khác (nếu có)"])
    muc(d, "2. Căn cứ"); d.add_paragraph("Biên bản nghiệm thu hoàn thành số …… ngày ……/……/……; hợp đồng số …… ngày ……/……/……")
    muc(d, "3. Phạm vi, hiện trạng công trình bàn giao"); d.add_paragraph(CHAM); d.add_paragraph(CHAM)
    muc(d, "4. Tài liệu bàn giao kèm theo")
    bang(d, ["STT", "Tài liệu", "Số lượng", "Ghi chú"], 0, [1.2, 9, 2, 3.3]); t = d.tables[-1]
    for i, x in enumerate(["Bản vẽ hoàn công", "Quy trình vận hành (nếu có)", "Quy trình bảo trì công trình", "Danh mục thiết bị, phụ tùng, vật tư dự trữ thay thế", "Hồ sơ phục vụ quản lý, sử dụng công trình", "Tài liệu khác"], 1):
        c = t.add_row().cells; c[0].text = str(i); c[1].text = x
    d.add_paragraph()
    muc(d, "5. Thiết bị, chìa khóa, tài sản bàn giao (nếu có)"); d.add_paragraph(CHAM)
    muc(d, "6. Thời hạn bảo hành và đầu mối liên hệ bảo hành"); d.add_paragraph("Bảo hành từ ……/……/…… đến ……/……/……   Đầu mối: " + CHAM)
    d.add_paragraph("Kể từ thời điểm ký biên bản, bên nhận chịu trách nhiệm quản lý, khai thác và bảo trì công trình theo quy trình đã bàn giao.")
    ky(d, ["ĐẠI DIỆN BÊN GIAO", "ĐẠI DIỆN BÊN NHẬN"]); luu(d, "bien-ban-ban-giao-cong-trinh")


def phieu_bao_hanh():
    d = moi(); dau(d, "CHỦ ĐẦU TƯ / CHỦ SỞ HỮU"); tieu_de(d, "PHIẾU YÊU CẦU BẢO HÀNH CÔNG TRÌNH")
    d.add_paragraph("Kính gửi: " + CHAM + " (nhà thầu thi công / cung ứng thiết bị)")
    thong_tin_ct(d); dong(d, "Hợp đồng số", False); d.add_paragraph("Thời hạn bảo hành theo hợp đồng / biên bản nghiệm thu: từ ……/……/…… đến ……/……/……")
    muc(d, "1. Hư hỏng, khiếm khuyết phát hiện"); bang(d, ["STT", "Vị trí", "Mô tả hư hỏng", "Ngày phát hiện", "Ảnh / tài liệu kèm"], 4, [1.2, 3, 6, 2.5, 3])
    muc(d, "2. Yêu cầu"); d.add_paragraph("Đề nghị nhà thầu kiểm tra hiện trường trước ngày ……/……/…… và hoàn thành sửa chữa trước ngày ……/……/……")
    d.add_paragraph("Đầu mối liên hệ: " + NGAN + "   Điện thoại: " + NGAN)
    muc(d, "3. Xác nhận kết quả bảo hành"); d.add_paragraph("Ngày hoàn thành: ……/……/……   ☐ Đạt   ☐ Chưa đạt, yêu cầu: " + CHAM)
    ky(d, ["BÊN YÊU CẦU", "NHÀ THẦU BẢO HÀNH"]); luu(d, "phieu-yeu-cau-bao-hanh")


def bb_hien_truong():
    d = moi(); dau(d, "BAN QUẢN LÝ / CHỦ ĐẦU TƯ"); tieu_de(d, "BIÊN BẢN HIỆN TRƯỜNG", "(sự cố, sai sót kỹ thuật, vi phạm an toàn / chất lượng)")
    thong_tin_ct(d)
    muc(d, "1. Thời gian, địa điểm lập biên bản"); d.add_paragraph("…… giờ …… ngày ……/……/……   Tại: " + NGAN)
    muc(d, "2. Thành phần"); thanh_phan(d, ["Đại diện chủ đầu tư / giám sát", "Đại diện nhà thầu thi công", "Thành phần khác (thiết kế, an toàn, chính quyền… nếu có)"])
    muc(d, "3. Loại sự việc"); d.add_paragraph("☐ Sự cố công trình   ☐ Sự cố mất an toàn lao động   ☐ Sai sót kỹ thuật / chất lượng   ☐ Vi phạm biện pháp thi công, an toàn, vệ sinh môi trường   ☐ Khác")
    muc(d, "4. Mô tả hiện trạng"); d.add_paragraph("Vị trí, thời điểm xảy ra, tình trạng công trình, thiệt hại về người và tài sản (nếu có): " + CHAM); d.add_paragraph(CHAM)
    muc(d, "5. Nguyên nhân sơ bộ"); d.add_paragraph(CHAM)
    muc(d, "6. Biện pháp xử lý tạm thời và yêu cầu"); d.add_paragraph(CHAM)
    muc(d, "7. Thông báo, báo cáo"); d.add_paragraph("☐ Đã thông báo UBND cấp xã và cơ quan cấp trên (nếu có) lúc …… giờ ……/……/……   ☐ Báo cáo bằng văn bản tới UBND cấp tỉnh trong 24 giờ (đối với sự cố công trình)")
    p = d.add_paragraph("Ghi chú: trình tự báo cáo, giải quyết sự cố công trình theo Điều 45, 46 Nghị định 207/2026/NĐ-CP; sự cố gây mất an toàn lao động theo Điều 49."); p.runs[0].italic = True; p.runs[0].font.size = Pt(11)
    muc(d, "8. Tài liệu kèm theo"); d.add_paragraph("Ảnh hiện trường, sơ đồ, số liệu đo đạc: " + NGAN)
    ky(d, ["ĐẠI DIỆN CHỦ ĐẦU TƯ / GIÁM SÁT", "ĐẠI DIỆN NHÀ THẦU", "THÀNH PHẦN KHÁC"]); luu(d, "bien-ban-hien-truong")


if __name__ == "__main__":
    for f in [phieu_yeu_cau_nghiem_thu, bb_vat_lieu, bb_cong_viec, bb_giai_doan, bb_hoan_thanh, nhat_ky, bao_cao_ngay,
              de_nghi_thanh_toan, bang_khoi_luong, bb_ban_giao, phieu_bao_hanh, bb_hien_truong]:
        f()
    print("Đã tạo", len(os.listdir(OUT)), "biểu mẫu trong", OUT)
