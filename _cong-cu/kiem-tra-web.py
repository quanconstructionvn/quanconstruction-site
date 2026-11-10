# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Kiểm tra định kỳ website (chạy ở thư mục gốc repo): python3 _cong-cu/kiem-tra-web.py
#  1. Liên kết nội bộ (href/src, neo #...) trong mọi trang HTML và content/*.json
#  2. sitemap.xml: mọi URL trỏ tới file có thật; trang công khai nào chưa có trong sitemap
#  3. Thư viện pháp lý: hiệu lực sắp đến/đã đến, trạng thái mâu thuẫn với ngày, văn bản cần kiểm tra
#  4. Bài viết dẫn văn bản đã hết hiệu lực toàn bộ
#  5. Thời hạn tên miền, dịch vụ ghi trong _cong-cu/thoi-han.json
# Kết quả: in báo cáo; mã thoát 1 nếu có LỖI (link chết, thời hạn quá hạn).
import datetime
import glob
import html
import importlib.util
import json
import os
import re
import sys
from urllib.parse import unquote, urlparse

SITE = "quanconstruction.biz.vn"
HOM_NAY = datetime.date.today()
AN = ("hr/", "admin/", "du-an/", "khach-hang/", "_cong-cu/", "node_modules/")
loi, canh_bao, ghi_chu = [], [], []
_ids = {}


def ids(f):
    if f not in _ids:
        s = open(f, encoding="utf-8", errors="ignore").read()
        _ids[f] = set(re.findall(r'\sid="([^"]+)"', s))
    return _ids[f]


def dich(path, goc):
    t = path.lstrip("/") if path.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(goc), path))
    t = unquote(t)
    if t in ("", ".") or t.endswith("/") or os.path.isdir(t):
        t = os.path.join(t, "index.html")
    return t


def kiem_lien_ket(u, f):
    u = html.unescape(u.strip())
    if not u or u.startswith(("mailto:", "tel:", "javascript:", "data:", "{{")):
        return
    if u.startswith("#"):
        if len(u) > 1 and u[1:] not in ids(f):
            loi.append(f"Neo không tồn tại: {f} → {u}")
        return
    p = urlparse(u)
    if p.scheme in ("http", "https"):
        if not p.netloc.endswith(SITE):
            return
        path = p.path or "/"
    elif p.scheme:
        return
    else:
        path = u.split("#")[0].split("?")[0]
    t = dich(path, f)
    if not os.path.exists(t):
        loi.append(f"Link chết: {f} → {u}")
    elif p.fragment and t.endswith(".html") and p.fragment not in ids(t):
        loi.append(f"Neo không tồn tại: {f} → {u}")


# 1. Liên kết trong HTML
trang = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(("node_modules", "_cong-cu"))]
for f in trang:
    s = open(f, encoding="utf-8", errors="ignore").read()
    s = re.sub(r"<script(?![^>]*application/ld\+json)[^>]*>.*?</script>", "", s, flags=re.S)
    for u in re.findall(r'\s(?:href|src)="([^"]*)"', s):
        kiem_lien_ket(u, f)
# Liên kết trong dữ liệu content/*.json
for f in glob.glob("content/*.json"):
    s = open(f, encoding="utf-8").read()
    for u in re.findall(r'"(/[^"\s]+)"', s):
        if re.search(r"\.(html|png|jpe?g|webp|svg|gif|pdf)(#.*)?$", u, re.I):
            kiem_lien_ket(u, "index.html")

# 2. Sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
locs = re.findall(r"<loc>https://" + re.escape(SITE) + r"(/[^<]*)</loc>", sm)
for path in locs:
    if not os.path.exists(dich(path, "index.html")):
        loi.append(f"Sitemap trỏ tới trang không có: {path}")
co = {dich(p, "index.html") for p in locs}
for f in trang:
    if f.startswith(AN) or f.startswith("google") or f in co:
        continue
    canh_bao.append(f"Trang công khai chưa có trong sitemap: {f}")

# 3. Thư viện pháp lý
dm = json.load(open("phap-ly/danh-muc.json", encoding="utf-8"))
vb = {x["id"]: x for x in dm["vanBan"]}
try:
    cap = datetime.date.fromisoformat(dm.get("capNhat", ""))
    if (HOM_NAY - cap).days > 30:
        canh_bao.append(f"Danh mục pháp lý cập nhật lần cuối {cap:%d/%m/%Y} (quá 30 ngày) – nên rà lại hiệu lực trên Cổng Pháp luật quốc gia")
except ValueError:
    pass
for x in vb.values():
    tt, hl = x.get("ttCong", ""), x.get("hieuLucTu") or ""
    try:
        d = datetime.date.fromisoformat(hl)
    except ValueError:
        d = None
    if not tt:
        ghi_chu.append(f"{x['soHieu']}: chưa ghi tình trạng hiệu lực")
    if d and d > HOM_NAY and tt in ("Còn hiệu lực", "Hết hiệu lực một phần"):
        canh_bao.append(f"{x['soHieu']}: ghi '{tt}' nhưng ngày hiệu lực {d:%d/%m/%Y} chưa đến")
    if d and d <= HOM_NAY and tt == "Chưa có hiệu lực":
        canh_bao.append(f"{x['soHieu']}: đã có hiệu lực từ {d:%d/%m/%Y} nhưng danh mục vẫn ghi 'Chưa có hiệu lực' – cập nhật danh mục và các bài viết liên quan")
    if d and 0 < (d - HOM_NAY).days <= 60:
        canh_bao.append(f"{x['soHieu']} ({x.get('ten','')[:60]}) sẽ có hiệu lực {d:%d/%m/%Y} – chuẩn bị cập nhật bài viết")
    if x.get("canKiemTra"):
        ghi_chu.append(f"{x['soHieu']}: đánh dấu cần kiểm tra")

# 4. Bài viết dẫn văn bản hết hiệu lực toàn bộ
sp = importlib.util.spec_from_file_location("bv", "_cong-cu/bai-viet.py")
bv = importlib.util.module_from_spec(sp)
sp.loader.exec_module(bv)
for b in bv.BAI:
    for i in set(re.findall(r"/phap-ly/([^.\"]+)\.html", json.dumps(b["body"], ensure_ascii=False))):
        x = vb.get(i)
        if x is None:
            loi.append(f"Bài {b['slug']} dẫn văn bản không có trong thư viện: {i}")
        elif x.get("ttCong") == "Hết hiệu lực toàn bộ":
            canh_bao.append(f"Bài {b['slug']} dẫn {x['soHieu']} đã HẾT HIỆU LỰC TOÀN BỘ – cần sửa bài")

# 5. Thời hạn tên miền / dịch vụ
th = "_cong-cu/thoi-han.json"
if os.path.exists(th):
    for m in json.load(open(th, encoding="utf-8")).get("muc", []):
        try:
            d = datetime.date.fromisoformat(m["het_han"])
        except (KeyError, ValueError):
            ghi_chu.append(f"Chưa có ngày hết hạn: {m.get('ten')}")
            continue
        con = (d - HOM_NAY).days
        if con < 0:
            loi.append(f"ĐÃ HẾT HẠN: {m['ten']} ({d:%d/%m/%Y})")
        elif con <= 60:
            canh_bao.append(f"Sắp hết hạn: {m['ten']} còn {con} ngày ({d:%d/%m/%Y}) – {m.get('noi_gia_han','')}")
        else:
            ghi_chu.append(f"{m['ten']}: hết hạn {d:%d/%m/%Y} (còn {con} ngày)")

print(f"KIỂM TRA WEBSITE {HOM_NAY:%d/%m/%Y} – {len(trang)} trang HTML, {len(locs)} URL sitemap, {len(vb)} văn bản")
for ten, ds in (("LỖI", loi), ("CẢNH BÁO", canh_bao), ("GHI CHÚ", ghi_chu)):
    print(f"\n== {ten} ({len(ds)})")
    for x in sorted(set(ds)):
        print(" -", x)
sys.exit(1 if loi else 0)
