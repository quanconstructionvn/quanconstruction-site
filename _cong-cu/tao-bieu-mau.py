# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Tạo biểu mẫu tải về cho Sổ tay xây dựng: mỗi mẫu 3 bản Word (.docx), Excel (.xlsx), PDF (.pdf)
# từ file mô tả _cong-cu/bieu-mau/<ma>.json (chép đúng mẫu trong phụ lục văn bản pháp luật).
# Chạy từ thư mục gốc website:  python3 _cong-cu/tao-bieu-mau.py   (cần python-docx, openpyxl, LibreOffice để xuất PDF)
#
# Cấu trúc JSON một mẫu:
# {"ma": "nd217-pl2-mau01", "ten": "Đơn đề nghị cấp giấy phép xây dựng", "nhom": "...",
#  "nguon": "Mẫu số 01 Phụ lục II Nghị định 217/2026/NĐ-CP", "loai": "chinh-thuc" | "noi-dung",
#  "can_cu": [["217-2026-nd-cp", "60", "khoản 1 Điều 60"]], "dung_khi": "...",
#  "khoi": [ ["mau_so", "Mẫu số 01"],
#            ["quoc_hieu", {"trai": ["TÊN CƠ QUAN", "Số: ……"], "ngay": "……, ngày … tháng … năm ……"}],
#            ["tieu_de", ["ĐƠN ĐỀ NGHỊ …", "dòng phụ"]],
#            ["p", "đoạn văn"] | ["p", {"t": "…", "b": true, "i": true, "can": "center|right|left", "thut": 0}],
#            ["table", {"cot": ["…"], "dong": [["…"]], "rong": [1, 3, 2]}],
#            ["ky", [["NGƯỜI ĐỀ NGHỊ", "(Ký, ghi rõ họ tên)"], …]],
#            ["ghi_chu", ["Ghi chú: …", "…"]],
#            ["ngat_trang"] ] }
# "loai": "noi-dung" = pháp luật không ban hành mẫu, trình bày theo nội dung bắt buộc của điều luật (in rõ trên mẫu).
import json, os, glob, subprocess, shutil, sys
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_cong-cu", "bieu-mau")
OUT = os.path.join(ROOT, "so-tay-xay-dung", "bieu-mau")
FONT = "Times New Roman"
AL = {"center": WD_ALIGN_PARAGRAPH.CENTER, "right": WD_ALIGN_PARAGRAPH.RIGHT, "left": WD_ALIGN_PARAGRAPH.LEFT, "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}
NHAN_NOIDUNG = "Pháp luật không ban hành mẫu – trình bày theo nội dung bắt buộc tại {cc}"


def P(x):
    return x if isinstance(x, dict) else {"t": x}


# ---------------- Word ----------------
def run(par, text, b=False, i=False, size=13):
    r = par.add_run(text); r.bold = b; r.italic = i; r.font.size = Pt(size); r.font.name = FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    return r


def para(doc_or_cell, t, b=False, i=False, can="left", size=13, thut=0, space=3):
    p = doc_or_cell.add_paragraph()
    p.alignment = AL.get(can, WD_ALIGN_PARAGRAPH.JUSTIFY)
    pf = p.paragraph_format; pf.space_after = Pt(space); pf.space_before = Pt(0)
    if thut: pf.first_line_indent = Cm(thut)
    for k, line in enumerate(str(t).split("\n")):
        if k: run(p, "").add_break()
        run(p, line, b, i, size)
    return p


def no_border(tbl):
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
        x = OxmlElement(f"w:{e}"); x.set(qn("w:val"), "nil"); b.append(x)
    tblPr.append(b)


def cell_text(c, t, b=False, i=False, can="left", size=12):
    c.paragraphs[0].text = ""
    p = c.paragraphs[0]; p.alignment = AL.get(can, WD_ALIGN_PARAGRAPH.LEFT); p.paragraph_format.space_after = Pt(0)
    for k, line in enumerate(str(t).split("\n")):
        if k: run(p, "").add_break()
        run(p, line, b, i, size)


def docx_of(m, path):
    d = Document()
    s = d.sections[0]; s.page_height, s.page_width = Cm(29.7), Cm(21)
    rong_bang = max([0] + [max([len(b[1].get("cot", []))] + [len(r) for r in b[1]["dong"]]) for b in m["khoi"] if b[0] == "table"])
    if rong_bang > 8:  # bảng nhiều cột: khổ ngang
        from docx.enum.section import WD_ORIENT
        s.orientation = WD_ORIENT.LANDSCAPE; s.page_height, s.page_width = Cm(21), Cm(29.7)
    s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(3), Cm(2), Cm(2), Cm(2)
    st = d.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(13); st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    d.core_properties.author = "Quang Mai Phú"; d.core_properties.title = m["ten"]
    d.core_properties.comments = f'{m["nguon"]} – Quan Construction (quanconstruction.biz.vn/so-tay-xay-dung/bieu-mau.html)'
    if m["loai"] == "noi-dung":
        para(d, NHAN_NOIDUNG.format(cc=m["nguon"]), i=True, can="right", size=10)
    for blk in m["khoi"]:
        k, v = blk[0], (blk[1] if len(blk) > 1 else None)
        if k == "mau_so":
            para(d, v, b=True, can="right", size=12)
        elif k == "quoc_hieu":
            t = d.add_table(rows=1, cols=2); no_border(t); t.alignment = WD_TABLE_ALIGNMENT.CENTER
            l, r = t.rows[0].cells
            t.autofit = False
            for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), (6.5, 9.5)): gc.set(qn("w:w"), str(int(w * 567)))
            l.width, r.width = Cm(6.5), Cm(9.5)
            cell_text(l, "\n".join(v.get("trai", [])) or " ", b=True, can="center", size=12)
            cell_text(r, "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n---------------", b=True, can="center", size=12)
            if v.get("ngay"): para(d, v["ngay"], i=True, can="right", size=13)
        elif k == "tieu_de":
            for j, line in enumerate(v):
                para(d, line, b=(j == 0), can="center", size=14 if j == 0 else 13, space=2)
        elif k == "p":
            x = P(v); para(d, x["t"], x.get("b", False), x.get("i", False), x.get("can", "left"), thut=x.get("thut", 0))
        elif k == "table":
            cot, dong = v.get("cot", []), v["dong"]
            n = max([len(cot)] + [len(r) for r in dong])
            t = d.add_table(rows=(1 if cot else 0) + len(dong), cols=n); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
            ri = 0
            if cot:
                for j, c in enumerate(cot): cell_text(t.rows[0].cells[j], c, b=True, can="center")
                ri = 1
            for r in dong:
                for j in range(n): cell_text(t.rows[ri].cells[j], r[j] if j < len(r) else "")
                ri += 1
            rong = (v.get("rong") or [1] * n)[:n] + [1] * max(0, n - len(v.get("rong") or []))
            t.autofit = False
            tot = sum(rong); W = 24.7 if rong_bang > 8 else 16.0
            grid = t._tbl.tblGrid
            for j, gc in enumerate(grid.findall(qn("w:gridCol"))): gc.set(qn("w:w"), str(int(W * rong[j] / tot * 567)))
            for row in t.rows:
                for j, c in enumerate(row.cells): c.width = Cm(W * rong[j] / tot)
            para(d, "", space=2)
        elif k == "ky":
            t = d.add_table(rows=1, cols=len(v)); no_border(t)
            for j, (a, b) in enumerate(v):
                cell_text(t.rows[0].cells[j], f"{a}\n{b}\n\n\n\n", b=False, can="center")
                t.rows[0].cells[j].paragraphs[0].runs[0].bold = True
        elif k == "ghi_chu":
            for line in v: para(d, line, i=True, size=11, space=1)
        elif k == "ngat_trang":
            d.add_page_break()
        else:
            raise ValueError(f'{m["ma"]}: khối lạ {k}')
    d.save(path)


# ---------------- Excel ----------------
def xlsx_of(m, path):
    wb = Workbook(); ws = wb.active; ws.title = "Mau"
    W = max([8] + [max([len(b[1].get("cot", []))] + [len(r) for r in b[1]["dong"]]) for b in m["khoi"] if b[0] == "table"])  # số cột trình bày
    for c in range(1, W + 1): ws.column_dimensions[get_column_letter(c)].width = max(8, 104 // W)
    ws.page_setup.paperSize = ws.PAPERSIZE_A4; ws.page_setup.orientation = 'landscape' if W > 8 else 'portrait'; ws.page_setup.fitToWidth = 1; ws.sheet_properties.pageSetUpPr.fitToPage = True; ws.page_setup.fitToHeight = 0
    wb.properties.creator = "Quang Mai Phú"; wb.properties.title = m["ten"]
    thin = Side(style="thin"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
    row = [1]

    def line(t, b=False, i=False, can="left", size=12, c1=1, c2=W, wrap=True, h=None):
        r = row[0]; ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
        x = ws.cell(r, c1, t); x.font = Font(name=FONT, size=size, bold=b, italic=i)
        x.alignment = Alignment(horizontal="justify" if can == "justify" else can, vertical="top", wrap_text=wrap)
        n = max(1, sum(len(s) // 95 + 1 for s in str(t).split("\n")))
        ws.row_dimensions[r].height = h or 16 * n
        row[0] += 1

    if m["loai"] == "noi-dung":
        line(NHAN_NOIDUNG.format(cc=m["nguon"]), i=True, can="right", size=9)
    for blk in m["khoi"]:
        k, v = blk[0], (blk[1] if len(blk) > 1 else None)
        if k == "mau_so": line(v, b=True, can="right")
        elif k == "quoc_hieu":
            r = row[0]; tr = "\n".join(v.get("trai", []))
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=W * 3 // 8)
            ws.merge_cells(start_row=r, start_column=W * 3 // 8 + 1, end_row=r, end_column=W)
            a = ws.cell(r, 1, tr); a.font = Font(name=FONT, size=11, bold=True); a.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            b = ws.cell(r, W * 3 // 8 + 1, "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc"); b.font = Font(name=FONT, size=11, bold=True); b.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            ws.row_dimensions[r].height = 16 * max(2, tr.count("\n") + 1, len(tr) // 30 + 1); row[0] += 1
            if v.get("ngay"): line(v["ngay"], i=True, can="right")
        elif k == "tieu_de":
            for j, t in enumerate(v): line(t, b=(j == 0), can="center", size=13 if j == 0 else 12)
        elif k == "p":
            x = P(v); line(x["t"], x.get("b", False), x.get("i", False), x.get("can", "left"))
        elif k == "table":
            cot, dong = v.get("cot", []), v["dong"]
            n = max([len(cot)] + [len(r) for r in dong])
            rong = v.get("rong") or [1] * n
            # chia W cột cho n cột bảng theo tỷ lệ
            spans, tot, acc = [], sum(rong[:n]), 0
            for j in range(n):
                w = max(1, round(W * rong[j] / tot)) if j < n - 1 else W - acc
                if acc + w > W - (n - 1 - j): w = max(1, W - (n - 1 - j) - acc)
                spans.append((acc + 1, acc + w)); acc += w
            for rr, data, hd in ([(None, cot, True)] if cot else []) + [(None, r, False) for r in dong]:
                r = row[0]; mx = 1
                for j, (c1, c2) in enumerate(spans):
                    if c2 > c1: ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
                    t = data[j] if j < len(data) else ""
                    x = ws.cell(r, c1, t); x.font = Font(name=FONT, size=11, bold=hd)
                    x.alignment = Alignment(horizontal="center" if hd else "left", vertical="top", wrap_text=True)
                    for cc in range(c1, c2 + 1): ws.cell(r, cc).border = box
                    mx = max(mx, sum(len(s) // max(8, 13 * (c2 - c1 + 1) // 7) + 1 for s in str(t).split("\n")))
                ws.row_dimensions[r].height = 15 * mx; row[0] += 1
            row[0] += 1
        elif k == "ky":
            r = row[0]; n = len(v); per = W // n
            for j, (a, b) in enumerate(v):
                c1 = j * per + 1; c2 = W if j == n - 1 else c1 + per - 1
                ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
                x = ws.cell(r, c1, f"{a}\n{b}"); x.font = Font(name=FONT, size=11, bold=True); x.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            ws.row_dimensions[r].height = 80; row[0] += 1
        elif k == "ghi_chu":
            for t in v: line(t, i=True, size=10)
        elif k == "ngat_trang":
            ws.row_breaks.append(__import__("openpyxl").worksheet.pagebreak.Break(id=row[0] - 1))
    wb.save(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    ma_list = []
    for f in sorted(glob.glob(os.path.join(SRC, "*.json"))):
        m = json.load(open(f, encoding="utf-8")); ma_list.append(m["ma"])
        docx_of(m, os.path.join(OUT, m["ma"] + ".docx"))
        xlsx_of(m, os.path.join(OUT, m["ma"] + ".xlsx"))
    # xóa file cũ không còn trong danh sách
    for f in os.listdir(OUT):
        if os.path.splitext(f)[0] not in ma_list: os.remove(os.path.join(OUT, f))
    # PDF từ Word bằng LibreOffice
    lo = shutil.which("libreoffice") or shutil.which("soffice")
    if lo and "--khong-pdf" not in sys.argv:
        subprocess.run([lo, "--headless", "--convert-to", "pdf", "--outdir", OUT] + [os.path.join(OUT, x + ".docx") for x in ma_list],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # danh sách cho trang Sổ tay xây dựng
    ds = [{k: json.load(open(os.path.join(SRC, x + ".json"), encoding="utf-8"))[k] for k in ("ma", "ten", "nhom", "nguon", "loai", "can_cu", "dung_khi")} for x in ma_list]
    json.dump(ds, open(os.path.join(ROOT, "_cong-cu", "bieu-mau-danh-sach.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Đã tạo {len(ma_list)} mẫu × 3 định dạng")


if __name__ == "__main__":
    main()
