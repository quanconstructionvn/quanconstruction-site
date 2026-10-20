# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Tạo trang toàn văn tĩnh cho từng văn bản pháp luật (phục vụ Google tìm kiếm – SEO),
# cập nhật danh mục tĩnh + câu hỏi thường gặp trong phap-ly.html và sitemap.xml.
# Chạy từ thư mục gốc website:  python3 _cong-cu/tao-trang-phap-ly.py
# Dữ liệu vào: phap-ly/danh-muc.json, phap-ly/van-ban/<id>.json, _cong-cu/mau-trang-van-ban.html
import json, re, os, html, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://quanconstruction.biz.vn"
P = lambda *a: os.path.join(ROOT, *a)
esc = lambda s: html.escape(str(s or ""), quote=True)

GROUPS = [["A", "Văn bản Luật nền tảng"], ["B1", "Quản lý hoạt động xây dựng"], ["B2", "Chi phí đầu tư xây dựng"],
          ["B3", "Hợp đồng xây dựng"], ["B4", "Chất lượng, thi công và bảo trì"], ["B5", "Vật liệu xây dựng"],
          ["B6", "Năng lực, hệ thống thông tin"], ["B7", "Thanh toán – quyết toán vốn đầu tư"], ["C", "Dân sự, thương mại, đấu thầu"],
          ["D", "Đất đai & sổ đỏ"], ["E", "Nhà ở & kinh doanh bất động sản"], ["G", "Công chứng, thuế & lệ phí nhà đất"],
          ["H", "Xử phạt vi phạm hành chính"], ["F", "Quy hoạch"], ["I", "Kiến trúc"], ["J", "Phòng cháy, chữa cháy & cứu nạn, cứu hộ"]]
GM = dict(GROUPS)
ORDER = {g[0]: i for i, g in enumerate(GROUPS)}

# Câu hỏi thường gặp trên trang Tra cứu pháp luật (chỉ dẫn tới điều luật, không diễn giải thay văn bản)
FAQ = [
    ("Hồ sơ xin giấy phép xây dựng nhà ở riêng lẻ gồm những gì?", "217-2026-nd-cp", "60",
     "Hồ sơ đề nghị cấp giấy phép xây dựng đối với nhà ở riêng lẻ được quy định tại Điều 60 Nghị định 217/2026/NĐ-CP; điều kiện cấp phép xem Điều 50, giấy tờ hợp pháp về đất xem Điều 55."),
    ("Ai có thẩm quyền cấp giấy phép xây dựng?", "217-2026-nd-cp", "53",
     "Thẩm quyền cấp giấy phép xây dựng được quy định tại Điều 53 Nghị định 217/2026/NĐ-CP, hướng dẫn Luật Xây dựng 135/2025/QH15 (Điều 43, 44)."),
    ("Hoàn công nhà ở cần hồ sơ gì?", "207-2026-nd-cp", "28",
     "Hồ sơ hoàn thành công trình xây dựng quy định tại Điều 28 Nghị định 207/2026/NĐ-CP; nghiệm thu hoàn thành công trình xem Điều 24, bàn giao xem Điều 30."),
    ("Thủ tục cấp sổ đỏ (Giấy chứng nhận) lần đầu như thế nào?", "101-2024-nd-cp", "36",
     "Trình tự, thủ tục cấp Giấy chứng nhận lần đầu quy định tại Điều 36 Nghị định 101/2024/NĐ-CP; hồ sơ đăng ký lần đầu xem Điều 28; nguyên tắc cấp Giấy chứng nhận xem Điều 135 Luật Đất đai 31/2024/QH15."),
    ("Mức thu lệ phí trước bạ nhà đất là bao nhiêu?", "33-vbhn-btc", "8",
     "Mức thu lệ phí trước bạ theo tỷ lệ (%) quy định tại Điều 8, giá tính lệ phí trước bạ tại Điều 7 Văn bản hợp nhất 33/VBHN-BTC về lệ phí trước bạ."),
    ("Tạm ứng hợp đồng xây dựng được quy định ở đâu?", "210-2026-nd-cp", "",
     "Tạm ứng hợp đồng xây dựng được quy định trong Nghị định 210/2026/NĐ-CP về hợp đồng xây dựng (điều về tạm ứng hợp đồng). Gõ “tạm ứng hợp đồng” vào ô tìm kiếm để đọc ngay điều luật."),
    ("Nhà ở riêng lẻ có phải đáp ứng yêu cầu phòng cháy chữa cháy không?", "55-2024-qh15", "20",
     "Yêu cầu phòng cháy đối với nhà ở quy định tại Điều 20, nhà ở kết hợp sản xuất, kinh doanh tại Điều 21 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ 55/2024/QH15."),
    ("Xây dựng sai phép, không phép bị xử phạt thế nào?", "339-2026-nd-cp", "25",
     "Vi phạm về trật tự xây dựng (xây dựng không phép, sai phép) quy định tại Điều 25 Nghị định 339/2026/NĐ-CP, có hiệu lực từ 26/08/2026."),
]


def status(l, today):
    if l.get("hieuLucTu") and today < l["hieuLucTu"]: return "chua"
    if l.get("hieuLucDen") and today >= l["hieuLucDen"]: return "het"
    return "con"


STL = {"con": "Còn hiệu lực", "het": "Hết hiệu lực", "chua": "Chưa có hiệu lực"}
fmt = lambda x: "/".join(reversed(x.split("-"))) if x else "—"
name = lambda l: f'{l.get("loai","")} {l.get("soHieu","")}'.strip()


def dl(d):
    d = str(d)
    if re.fullmatch(r"\d+[a-zđ]?", d, re.I): return "Điều " + d
    if d.startswith("PL "): return "Phụ lục " + d[3:]
    if re.fullmatch(r"P\d+", d): return "Phần " + d[1:]
    return "Mục " + d


aid = lambda d: "d" + re.sub(r"\s+", "-", str(d))


def cut(s, n):
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n: return s
    s = s[:n].rsplit(" ", 1)[0]
    return s.rstrip(",;:–-") + "…"


def main():
    dm = json.load(open(P("phap-ly", "danh-muc.json"), encoding="utf-8"))
    cap = dm.get("capNhat") or datetime.date.today().isoformat()
    today = datetime.date.today().isoformat()
    tpl = open(P("_cong-cu", "mau-trang-van-ban.html"), encoding="utf-8").read()
    laws = dm["vanBan"]
    by = {l["id"]: l for l in laws}
    made = []
    for l in laws:
        f = P("phap-ly", "van-ban", l["id"] + ".json")
        if not (l.get("soDieu", 0) > 0 and os.path.exists(f)):
            continue
        arts = json.load(open(f, encoding="utf-8"))
        st = status(l, today)
        url = f'{SITE}/phap-ly/{l["id"]}.html'
        nm = name(l)
        title = cut(f'{nm}: {l["ten"]}', 78) + " | Quan Construction"
        tieu = "; ".join(f"{dl(a[0])}: {a[1]}" for a in arts[:4])
        desc = cut(f'Toàn văn {nm} – {l["ten"]}. Ban hành {fmt(l.get("ngayBanHanh"))}, hiệu lực từ {fmt(l.get("hieuLucTu"))}, {STL[st].lower()}. {len(arts)} điều/mục, tra cứu miễn phí.', 300)
        grp = GM.get(l.get("nhom"), "Văn bản pháp luật")
        # mục lục + toàn văn
        toc, tx, ch = [], [], ""
        for a in arts:
            d, td, nd, cc = a[0], a[1], a[2], (a[3] if len(a) > 3 else "")
            if cc and cc != ch:
                ch = cc
                toc.append(f'<div class="ch">{esc(cc.split(" – ")[0])}</div>')
                tx.append(f'<div class="chp">{esc(cc)}</div>')
            toc.append(f'<a href="#{aid(d)}">{esc(dl(d))}. {esc(td)}</a>')
            tx.append(f'<article id="{aid(d)}"><h3>{esc(dl(d))}. {esc(td)}</h3><div class="bd">{esc(nd)}</div></article>')
        warn = ""
        if st == "het":
            warn = f'<div class="vb-warn"><b>Văn bản đã hết hiệu lực</b>{" – thay thế bởi " + esc(l["biThayThe"]) if l.get("biThayThe") else ""}. Chỉ dùng để tham khảo, đối chiếu.</div>'
        elif st == "chua":
            warn = f'<div class="vb-warn"><b>Văn bản chưa có hiệu lực</b> – có hiệu lực từ {fmt(l.get("hieuLucTu"))}.</div>'
        elif "một phần" in (l.get("ttCong") or ""):
            warn = '<div class="vb-warn">Văn bản <b>đã hết hiệu lực một phần</b> theo Cổng Pháp luật quốc gia – vui lòng kiểm tra điều khoản đã được sửa đổi trước khi áp dụng.</div>'
        if l.get("ghiChu"):
            warn += f'<div class="vb-warn">{esc(l["ghiChu"])}</div>'
        rows = [("Số hiệu", esc(l.get("soHieu"))), ("Loại văn bản", esc(l.get("loai"))), ("Cơ quan ban hành", esc(l.get("coQuan"))),
                ("Ngày ban hành", fmt(l.get("ngayBanHanh"))), ("Hiệu lực từ", fmt(l.get("hieuLucTu")))]
        if l.get("hieuLucDen"): rows.append(("Hết hiệu lực", fmt(l["hieuLucDen"])))
        if l.get("thayThe"): rows.append(("Thay thế", esc(l["thayThe"])))
        if l.get("biThayThe"): rows.append(("Bị thay thế bởi", esc(l["biThayThe"])))
        rows.append(("Lĩnh vực", esc(grp)))
        rows.append(("Tình trạng", f'<span class="vb-st {st}">{STL[st]}</span>'))
        if l.get("linkCong"): rows.append(("Bản gốc", f'<a href="{esc(l["linkCong"])}" target="_blank" rel="noopener nofollow">Xem trên Cổng Pháp luật quốc gia ↗</a>'))
        info = '<table class="vb-info">' + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</table>"
        rel = sorted([x for x in laws if x.get("nhom") == l.get("nhom") and x["id"] != l["id"] and x.get("soDieu", 0) > 0 and os.path.exists(P("phap-ly", "van-ban", x["id"] + ".json"))], key=lambda x: x.get("thuTu", 99))
        relh = ""
        if rel:
            relh = f'<div class="vb-rel"><h2>Văn bản liên quan – {esc(grp)}</h2><ul>' + "".join(
                f'<li><a href="/phap-ly/{x["id"]}.html"><b>{esc(name(x))}</b> – {esc(x["ten"])}</a></li>' for x in rel) + "</ul></div>"
        intro = cut(f'Toàn văn {len(arts)} điều/mục, ban hành {fmt(l.get("ngayBanHanh"))} bởi {l.get("coQuan","")}. Nội dung chính: {tieu}', 520)
        body = (f'<div class="ph vb-ph"><div class="w"><div class="vb-crumb"><a href="/index.html">Trang chủ</a> › <a href="/phap-ly.html">Tra cứu pháp luật</a> › {esc(nm)}</div>'
                f'<span class="eyebrow">{esc(grp)}</span><h1>{esc(nm)} – {esc(l["ten"])}</h1><p>{esc(intro)}</p></div></div>\n'
                f'<div class="w vb-wrap"><aside class="vb-side" aria-label="Mục lục"><h2>Mục lục ({len(arts)})</h2>{"".join(toc)}</aside>\n'
                f'<main class="vb-tx"><h2>Thông tin văn bản</h2>{warn}{info}<h2>Toàn văn</h2>{"".join(tx)}\n'
                f'<p class="vb-src">Nguồn toàn văn: Cổng Pháp luật quốc gia (phapluat.gov.vn). Văn bản trình bày theo từng Điều (quy chuẩn theo từng mục), có thể chưa gồm phụ lục, biểu mẫu, bản vẽ. Nội dung chỉ để tham khảo, không thay thế văn bản chính thức hay tư vấn pháp lý; khi sử dụng chính thức, vui lòng đối chiếu bản gốc. Cập nhật: {fmt(cap)}.</p>{relh}\n'
                f'<p style="margin-top:22px"><a class="btn p" href="/phap-ly.html">← Về trang Tra cứu pháp luật</a></p></main></div>')
        ld = {"@context": "https://schema.org", "@type": "Legislation", "name": f'{nm} {l["ten"]}', "legislationIdentifier": l.get("soHieu"),
              "legislationType": l.get("loai"), "legislationPassedBy": {"@type": "GovernmentOrganization", "name": l.get("coQuan")},
              "datePublished": l.get("ngayBanHanh") or None, "legislationDate": l.get("hieuLucTu") or None, "dateModified": cap, "inLanguage": "vi", "url": url,
              "isBasedOn": l.get("linkCong") or None,
              "legislationLegalForce": {"con": "https://schema.org/InForce", "het": "https://schema.org/NotInForce", "chua": "https://schema.org/NotInForce"}[st],
              "publisher": {"@type": "Organization", "name": "Công ty TNHH Đầu tư và Phát triển Quan Construction", "url": SITE}}
        ld = {k: v for k, v in ld.items() if v}
        bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Tra cứu pháp luật", "item": SITE + "/phap-ly.html"},
            {"@type": "ListItem", "position": 3, "name": nm, "item": url}]}
        jl = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld, bc))
        page = tpl.replace("{{TITLE}}", esc(title)).replace("{{DESC}}", esc(desc)).replace("{{URL}}", url).replace("{{JSONLD}}", jl).replace("{{BODY}}", body)
        open(P("phap-ly", l["id"] + ".html"), "w", encoding="utf-8").write(page)
        made.append(l)
    # xóa trang tĩnh của văn bản không còn trong danh mục
    keep = {l["id"] for l in made}
    for f in glob.glob(P("phap-ly", "*.html")):
        if os.path.basename(f)[:-5] not in keep: os.remove(f)
    made.sort(key=lambda x: (ORDER.get(x.get("nhom"), 99), x.get("thuTu", 99)))
    # danh mục tĩnh + FAQ trong phap-ly.html
    hub = open(P("phap-ly.html"), encoding="utf-8").read()
    lst, g0 = [], None
    for x in made:
        if x.get("nhom") != g0:
            if g0 is not None: lst.append("</ul>")
            g0 = x.get("nhom"); lst.append(f'<h3>{esc(GM.get(g0, "Khác"))}</h3><ul>')
        st = status(x, today)
        lst.append(f'<li><a href="phap-ly/{x["id"]}.html">{esc(name(x))}</a> – {esc(x["ten"])}{" <em>(" + STL[st].lower() + ")</em>" if st != "con" else ""}</li>')
    lst.append("</ul>")
    faq = "".join(f'<details class="pl-faq-i"><summary>{esc(q)}</summary><p>{esc(a)} <a href="phap-ly/{i}.html{"#" + aid(d) if d else ""}">Đọc điều luật →</a></p></details>'
                  for q, i, d, a in FAQ if i in keep)
    seo = (f'<!--SEO-LIST--><section class="w pl-seo"><h2>Câu hỏi thường gặp về thủ tục xây dựng, nhà đất</h2>{faq}'
           f'<details class="pl-all"><summary>Danh mục toàn văn {len(made)} văn bản pháp luật</summary>{"".join(lst)}</details></section><!--/SEO-LIST-->')
    hub = re.sub(r"<!--SEO-LIST-->.*?(<!--/SEO-LIST-->|</section>)", lambda m: seo, hub, count=1, flags=re.S)
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, i, d, a in FAQ if i in keep]}
    hub = re.sub(r'<script type="application/ld\+json" id="ld-faq">.*?</script>', "", hub, flags=re.S)
    hub = hub.replace("</head>", f'<script type="application/ld+json" id="ld-faq">{json.dumps(faqld, ensure_ascii=False)}</script></head>', 1)
    open(P("phap-ly.html"), "w", encoding="utf-8").write(hub)
    # sitemap
    sm = open(P("sitemap.xml"), encoding="utf-8").read()
    sm = re.sub(r"<url><loc>https://quanconstruction\.biz\.vn/phap-ly/[^<]+</loc>.*?</url>", "", sm)
    sm = re.sub(r"(<url><loc>https://quanconstruction\.biz\.vn/phap-ly\.html</loc>).*?</url>", r"\1<lastmod>" + cap + "</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>", sm)
    add = "".join(f'<url><loc>{SITE}/phap-ly/{x["id"]}.html</loc><lastmod>{cap}</lastmod><changefreq>monthly</changefreq></url>' for x in made)
    sm = sm.replace("</urlset>", add + "</urlset>")
    open(P("sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"Đã tạo {len(made)} trang văn bản, cập nhật phap-ly.html và sitemap.xml")


if __name__ == "__main__":
    main()
