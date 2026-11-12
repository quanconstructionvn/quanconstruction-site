# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Tạo nhánh "Sổ tay xây dựng" cho dân xây dựng & văn phòng (QA/QC, QS, CCM, Giám sát):
#   /so-tay-xay-dung.html (trang chủ nhánh) và /so-tay-xay-dung/<slug>.html từ dữ liệu _cong-cu/so-tay-xay-dung.py.
# Chạy từ thư mục gốc website:  python3 _cong-cu/tao-so-tay-xay-dung.py
# Khối nội dung: ("st", [kiểu, file.json]) = công cụ tương tác (js/so-tay-tuong-tac.js) | ("h2", chữ) | ("h3", chữ) | ("p", html) | ("ul"/"ol", [html,...]) | ("note", html)
#                | ("table", {"cot": [...], "dong": [[html,...], ...]}) | ("faq", [(câu hỏi, trả lời html), ...]) | ("html", html thô)
import json, os, re, html, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://quanconstruction.biz.vn"
P = lambda *a: os.path.join(ROOT, *a)
esc = lambda s: html.escape(str(s or ""), quote=True)

spec = importlib.util.spec_from_file_location("so_tay_xay_dung", P("_cong-cu", "so-tay-xay-dung.py"))
cs = importlib.util.module_from_spec(spec); spec.loader.exec_module(cs)

CSS = """<style>
.cs-ph{padding:40px 0 44px}.cs-ph h1{font-size:clamp(24px,4vw,38px);line-height:1.25;margin-top:8px;max-width:900px}.cs-ph p{max-width:820px;opacity:.92}
.cs-crumb{font-size:13.5px;margin-bottom:6px}.cs-crumb a{color:inherit;opacity:.85;text-decoration:underline}
.cs-wrap{display:grid;grid-template-columns:270px minmax(0,1fr);gap:36px;padding-top:30px;padding-bottom:60px;align-items:start}
.cs-nav{position:sticky;top:12px;border:1px solid var(--line);border-radius:14px;padding:14px;background:#fff;font-size:14px;max-height:calc(100vh - 24px);overflow:auto}
.cs-nav b{display:block;color:var(--navy);font-size:12.5px;letter-spacing:.06em;text-transform:uppercase;margin:12px 0 4px}.cs-nav b:first-child{margin-top:0}
.cs-nav a{display:block;padding:5px 8px;border-radius:8px;color:#26406b;text-decoration:none;line-height:1.4}.cs-nav a:hover{background:#eef3fb}.cs-nav a.on{background:var(--navy);color:#fff}
.cs-tx{font-size:16px;line-height:1.75;color:#1d2a44;max-width:860px}.cs-tx h2{font-size:22px;color:var(--navy);margin:30px 0 10px;scroll-margin-top:12px}
.cs-tx h3{font-size:18px;color:var(--navy);margin:22px 0 8px}.cs-tx p{margin:0 0 14px}.cs-tx ul,.cs-tx ol{margin:0 0 16px;padding-left:22px}.cs-tx li{margin:0 0 7px}
.cs-tx a{color:var(--blue);font-weight:600}.cs-meta{font-size:14px;color:var(--mut);margin-bottom:16px}
.cs-note{background:#fff8e6;border:1px solid #f1dca0;border-radius:10px;padding:12px 16px;margin:22px 0;font-size:14.5px}
.cs-tbl{overflow-x:auto;margin:0 0 18px}.cs-tbl table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:560px}
.cs-tbl th{background:var(--navy);color:#fff;text-align:left;padding:9px 10px;font-weight:700}.cs-tbl td{border-bottom:1px solid var(--line);padding:9px 10px;vertical-align:top}
.cs-tbl tr:nth-child(even) td{background:#f7f9fd}
.cs-faq details{border:1px solid var(--line);border-radius:10px;margin:0 0 10px;background:#fff}.cs-faq summary{cursor:pointer;padding:12px 14px;font-weight:700;color:var(--navy)}
.cs-faq details>div{padding:0 14px 12px}
.cs-toc{background:#f4f7fc;border-radius:12px;padding:12px 16px;margin:0 0 18px;font-size:14.5px}.cs-toc ol{margin:6px 0 0}
.cs-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;margin:10px 0 26px}
.cs-card{display:block;border:1px solid var(--line);border-radius:14px;padding:16px;background:#fff;text-decoration:none!important;color:#1d2a44!important;font-weight:400!important;transition:.2s}
.cs-card:hover{border-color:var(--blue);transform:translateY(-2px);box-shadow:0 8px 22px rgba(10,29,63,.08)}.cs-card b{display:block;color:var(--navy);font-size:16.5px;margin-bottom:6px}
.cs-card span{font-size:14px;color:var(--mut);line-height:1.5}.cs-tag{display:inline-block;font-size:12px;font-weight:700;color:var(--blue);background:#eef3fb;border-radius:6px;padding:2px 8px;margin-bottom:8px}
.cs-roles{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px;margin:10px 0 24px}
.cs-roles a{border-radius:12px;padding:14px;background:var(--navy);color:#fff!important;text-decoration:none!important}.cs-roles a b{display:block;font-size:17px}.cs-roles a span{font-size:13.5px;opacity:.85;font-weight:400}
@media(max-width:900px){.cs-wrap{grid-template-columns:1fr}.cs-nav{position:static;max-height:none}}
</style>"""


def block(k, v, en=False):
    if k == "h2":
        a = re.sub(r"[^a-z0-9]+", "-", v.lower().encode("ascii", "ignore").decode()).strip("-")
        return f"<h2>{esc(v)}</h2>"
    if k == "h3": return f"<h3>{esc(v)}</h3>"
    if k == "p": return f"<p>{v}</p>"
    if k in ("ul", "ol"): return f"<{k}>" + "".join(f"<li>{x}</li>" for x in v) + f"</{k}>"
    if k == "note": return f'<div class="cs-note">{v}</div>'
    if k == "table":
        return ('<div class="cs-tbl"><table><thead><tr>' + "".join(f"<th>{esc(c)}</th>" for c in v["cot"]) + "</tr></thead><tbody>"
                + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in v["dong"]) + "</tbody></table></div>")
    if k == "faq": return '<div class="cs-faq">' + "".join(f"<details><summary>{esc(q)}</summary><div>{a}</div></details>" for q, a in v) + "</div>"
    if k == "html": return v
    if k == "st":  # công cụ tương tác: [kiểu, file JSON trong _cong-cu/so-tay-du-lieu/]
        fn = v[1].replace(".json", ".en.json") if en and os.path.exists(P("_cong-cu", "so-tay-du-lieu", v[1].replace(".json", ".en.json"))) else v[1]
        d = open(P("_cong-cu", "so-tay-du-lieu", fn), encoding="utf-8").read().replace("</", "<\\/")
        return (f'<script type="application/json" data-st="{v[0]}">{d}</script>'
                + ('<noscript><p>This tool requires JavaScript.</p></noscript>' if en else '<noscript><p>Công cụ này cần bật JavaScript.</p></noscript>')
                + '<script src="/js/so-tay-tuong-tac.js?v=2" defer></script>')
    raise ValueError(k)


def render(blocks, en=False):
    out, toc, n = [], [], 0
    for k, v in blocks:
        if k == "h2":
            n += 1; toc.append(v); out.append(f'<h2 id="m{n}">{esc(v)}</h2>')
        else:
            out.append(block(k, v, en))
    t = (f'<nav class="cs-toc"><b>{"On this page" if en else "Nội dung trang"}</b><ol>' + "".join(f'<li><a href="#m{i+1}">{esc(x)}</a></li>' for i, x in enumerate(toc)) + "</ol></nav>") if len(toc) >= 4 else ""
    return t + "".join(out)


def faq_ld(t):
    q = [(a, b) for k, v in t["body"] if k == "faq" for a, b in v]
    if not q: return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", b)}} for a, b in q]}


def main():
    tpl = open(P("_cong-cu", "mau-trang-van-ban.html"), encoding="utf-8").read()
    tpl = re.sub(r"<style>\n\.vb-ph.*?</style>", lambda m: CSS, tpl, flags=re.S)
    tpl = tpl.replace("trang toàn văn văn bản (tạo tự động bằng _cong-cu/tao-trang-phap-ly.py)", "trang sổ tay xây dựng (tạo tự động bằng _cong-cu/tao-so-tay-xay-dung.py)")
    tpl = tpl.replace('<a href="/phap-ly.html" class=on>Pháp lý</a>', '<a href="/phap-ly.html">Pháp lý</a>').replace('<a href="/so-tay-xay-dung.html">Sổ tay xây dựng</a>', '<a href="/so-tay-xay-dung.html" class=on>Sổ tay xây dựng</a>', 1)
    os.makedirs(P("so-tay-xay-dung"), exist_ok=True)
    pages = cs.TRANG
    slugs = {t["slug"] for t in pages}
    for f in os.listdir(P("so-tay-xay-dung")):  # xóa trang cũ không còn trong dữ liệu
        if f.endswith(".html") and f[:-5] not in slugs: os.remove(P("so-tay-xay-dung", f))

    def side(cur):
        o = []
        for nhom, ten in cs.NHOM:
            ds = [t for t in pages if t["nhom"] == nhom and not t.get("an_menu")]
            if ds:
                o.append(f"<b>{esc(ten)}</b>" + "".join(f'<a href="/so-tay-xay-dung/{t["slug"]}.html"{" class=on" if t["slug"] == cur else ""}>{esc(t["ngan"])}</a>' for t in ds))
        return '<aside class="cs-nav"><a href="/so-tay-xay-dung.html"' + (' class=on' if cur is None else '') + '>« Sổ tay xây dựng</a>' + "".join(o) + "</aside>"

    def page(url, title, desc, crumb, h1, lead, inner, cur, extra_ld=None, upd=None):
        body = (f'<div class="ph cs-ph"><div class="w"><div class="cs-crumb"><a href="/index.html">Trang chủ</a> › {crumb}</div>'
                f'<span class="eyebrow">Sổ tay xây dựng · QA/QC · QS · CCM · Giám sát</span><h1>{esc(h1)}</h1>{"<p>" + lead + "</p>" if lead else ""}</div></div>\n'
                f'<div class="w cs-wrap">{side(cur)}<article class="cs-tx">{f"<div class=cs-meta>Quan Construction · cập nhật {upd}</div>" if upd else ""}{inner}'
                f'<p style="margin-top:26px"><a class="btn p" href="/lien-he.html" style="color:#fff">Cần tư vấn quản lý dự án, dự toán, giám sát? Liên hệ Quan Construction →</a></p></article></div>')
        ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Sổ tay xây dựng", "item": SITE + "/so-tay-xay-dung.html"}] +
            ([{"@type": "ListItem", "position": 3, "name": h1, "item": url}] if cur else [])}]
        if extra_ld: ld.append(extra_ld)
        jl = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
        t = title if len(title) <= 70 else title[:68].rsplit(" ", 1)[0] + "…"
        return (tpl.replace("{{TITLE}}", esc(t + " | Quan Construction")).replace("{{DESC}}", esc(desc)).replace("{{URL}}", url)
                .replace("{{JSONLD}}", jl).replace("{{BODY}}", body))

    for t in pages:
        url = f'{SITE}/so-tay-xay-dung/{t["slug"]}.html'
        art = {"@context": "https://schema.org", "@type": "Article", "headline": t["title"], "description": t["desc"], "dateModified": t["ngay"],
               "inLanguage": "vi", "mainEntityOfPage": url, "author": {"@type": "Organization", "name": "Quan Construction", "url": SITE}}
        h = page(url, t["title"], t["desc"], f'<a href="/so-tay-xay-dung.html">Sổ tay xây dựng</a> › {esc(t["ngan"])}', t["title"], t.get("lead", ""),
                 render(t["body"]), t["slug"], faq_ld(t) or art, "/".join(reversed(t["ngay"].split("-"))))
        open(P("so-tay-xay-dung", t["slug"] + ".html"), "w", encoding="utf-8").write(h)

    # Trang chủ nhánh
    roles = "".join(f'<a href="/so-tay-xay-dung/{s}.html"><b>{esc(a)}</b><span>{esc(b)}</span></a>' for a, b, s in cs.VAI_TRO if s in slugs)
    cards = []
    for nhom, ten in cs.NHOM:
        ds = [t for t in pages if t["nhom"] == nhom and not t.get("an_menu")]
        if ds:
            cards.append(f"<h2>{esc(ten)}</h2><div class=cs-grid>" + "".join(
                f'<a class="cs-card" href="/so-tay-xay-dung/{t["slug"]}.html"><span class="cs-tag">{esc(ten)}</span><b>{esc(t["title"])}</b><span>{esc(t["summary"])}</span></a>' for t in ds) + "</div>")
    inner = (f'<p>{cs.GIOI_THIEU}</p><h2>Theo vai trò</h2><div class="cs-roles">{roles}</div>' + "".join(cards) +
             '<div class="cs-note">Nội dung tóm tắt để tham khảo, dẫn tới toàn văn điều luật trong <a href="/phap-ly.html">thư viện pháp luật</a> của Quan Construction. Không thay thế văn bản pháp luật hay ý kiến của cơ quan có thẩm quyền.</div>')
    h = page(SITE + "/so-tay-xay-dung.html", cs.TIEU_DE, cs.MO_TA, "Sổ tay xây dựng", cs.TIEU_DE, cs.LEAD, inner, None)
    h = h.replace('href="/so-tay-xay-dung.html">« Trang chủ', 'href="/so-tay-xay-dung.html" class=on>« Trang chủ', 1) if 'class=on>« Trang' not in h else h
    open(P("so-tay-xay-dung.html"), "w", encoding="utf-8").write(h)

    # sitemap
    sm = open(P("sitemap.xml"), encoding="utf-8").read()
    sm = re.sub(r"<url><loc>https://quanconstruction\.biz\.vn/so-tay-xay-dung(?:\.html|/[^<]+)</loc>.*?</url>", "", sm)
    moi = max([t["ngay"] for t in pages] or ["2026-11-11"])
    sm = sm.replace("</urlset>", f'<url><loc>{SITE}/so-tay-xay-dung.html</loc><lastmod>{moi}</lastmod></url>' +
                    "".join(f'<url><loc>{SITE}/so-tay-xay-dung/{t["slug"]}.html</loc><lastmod>{t["ngay"]}</lastmod></url>' for t in pages) + "</urlset>")
    open(P("sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"Đã tạo trang Sổ tay xây dựng + {len(pages)} trang con")


# ---- Bản tiếng Anh (Quang Mai Phú, 12/11/2026): dữ liệu dịch trong _cong-cu/so-tay-en/ ----
#   chung.json (tiêu đề, giới thiệu, nhóm, vai trò); trang/<slug>.json (title, ngan, desc, summary, lead, body);
#   bieu-mau.json (tên, công dụng, nguồn từng biểu mẫu – bản mẫu tải về giữ tiếng Việt); so-tay-du-lieu/*.en.json (công cụ tương tác).
#   Tạo /en/so-tay-xay-dung.html và /en/so-tay-xay-dung/<slug>.html; trang Việt được thêm hreflang en và nút đổi ngôn ngữ.
def _en_tpl():
    s = open(P("en", "tin-tuc.html"), encoding="utf-8").read()
    def absol(x):
        x = re.sub(r'(href|src)="\.\./', r'\1="/', x)
        return re.sub(r'(href|src)="(?!/|https?:|tel:|mailto:|#)([^"]+)"', r'\1="/en/\2"', x)
    hdr = absol(s[s.index("<header"):s.index("</header>") + 9])
    hdr = hdr.replace('<a href="/en/tin-tuc.html" class=on>News</a>', '<a href="/en/tin-tuc.html">News</a>').replace('<a href="/en/so-tay-xay-dung.html">Handbook</a>', '<a href="/en/so-tay-xay-dung.html" class=on>Handbook</a>', 1)
    foot = re.sub(r'<script src="/js/content\.js[^"]*"></script>', '', absol(s[s.index('<div class="fab"'):]))
    return hdr, foot


def _en_links(h):
    def f(m):
        u = m.group(1)
        if u.startswith("/phap-ly") or u.startswith("/en/"): return m.group(0)
        return f'href="/en{u}"' if os.path.exists(P("en", u.lstrip("/"))) else m.group(0)
    return re.sub(r'href="(/[a-z0-9/-]+\.html)"', f, h)


def tao_en():
    d = P("_cong-cu", "so-tay-en")
    if not os.path.exists(os.path.join(d, "chung.json")): return
    ch = json.load(open(os.path.join(d, "chung.json"), encoding="utf-8"))
    nhom_en = dict(ch["NHOM"])
    pages = []
    for t in cs.TRANG:
        f = os.path.join(d, "trang", t["slug"] + ".json")
        if os.path.exists(f):
            e = json.load(open(f, encoding="utf-8")); e.update(slug=t["slug"], nhom=t["nhom"], ngay=t["ngay"], an_menu=t.get("an_menu")); pages.append(e)
    slugs = {t["slug"] for t in pages}
    os.makedirs(P("en", "so-tay-xay-dung"), exist_ok=True)
    for f in os.listdir(P("en", "so-tay-xay-dung")):
        if f.endswith(".html") and f[:-5] not in slugs: os.remove(P("en", "so-tay-xay-dung", f))
    # Trang con tiếng Anh tồn tại trước khi đổi liên kết
    for t in pages: open(P("en", "so-tay-xay-dung", t["slug"] + ".html"), "a").close()
    open(P("en", "so-tay-xay-dung.html"), "a").close()
    hdr0, foot = _en_tpl()
    bm = json.load(open(os.path.join(d, "bieu-mau.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "bieu-mau.json")) else {"forms": {}, "nhom": {}}

    def bieu_mau_groups():
        ds = json.load(open(P("_cong-cu", "bieu-mau-danh-sach.json"), encoding="utf-8"))
        thu_tu = ["Thẩm định", "Tổng mức", "Thi công", "Chi phí bảo trì", "Thanh toán", "Quyết toán", "Dự toán, quyết toán thu chi"]
        nhom = sorted({m["nhom"] for m in ds}, key=lambda n: next((i for i, k in enumerate(thu_tu) if n.startswith(k)), 9))
        tai = lambda m: " · ".join(f'<a href="/so-tay-xay-dung/bieu-mau/{m["ma"]}.{x}" download>{y}</a>' for x, y in (("pdf", "PDF"), ("docx", "Word"), ("xlsx", "Excel")))
        out = []
        for n in nhom:
            ms = [m for m in ds if m["nhom"] == n]
            out.append(("h2", bm["nhom"].get(n, n)))
            rows = []
            for m in ms:
                e = bm["forms"].get(m["ma"], {})
                lab = e.get("can_cu") or [x[2] for x in m["can_cu"]]
                rows.append([f'<b>{e.get("ten", m["ten"])}</b>' + (" <i>(mandatory content per the law)</i>" if m["loai"] == "noi-dung" else ""), e.get("dung_khi", m["dung_khi"]),
                             e.get("nguon", m["nguon"]) + "<br>" + "; ".join(cs.L(i, dd, lab[k] if k < len(lab) else tt) for k, (i, dd, tt) in enumerate(m["can_cu"])), tai(m)])
            out.append(("table", {"cot": ["Form", "When used", "Source – legal basis", "Download (Vietnamese)"], "dong": rows}))
        return out, len(ds)

    def side(cur):
        o = []
        for nh, _ in cs.NHOM:
            ds = [t for t in pages if t["nhom"] == nh and not t.get("an_menu")]
            if ds:
                o.append(f"<b>{esc(nhom_en.get(nh, nh))}</b>" + "".join(f'<a href="/en/so-tay-xay-dung/{t["slug"]}.html"{" class=on" if t["slug"] == cur else ""}>{esc(t["ngan"])}</a>' for t in ds))
        return '<aside class="cs-nav"><a href="/en/so-tay-xay-dung.html"' + (' class=on' if cur is None else '') + '>« Construction Handbook</a>' + "".join(o) + "</aside>"

    def page(path_vi, path_en, title, desc, crumb, h1, lead, inner, cur, extra_ld=None, upd=None):
        url, vi = SITE + path_en, SITE + path_vi
        h = (hdr0.replace('<a class="lg" href="/tin-tuc.html">', f'<a class="lg" href="{path_vi}">')
             .replace('<a class="" href="/tin-tuc.html" title="Tiếng Việt"', f'<a class="" href="{path_vi}" title="Tiếng Việt"')
             .replace('<a class="on" href="/en/tin-tuc.html" title="English"', f'<a class="on" href="{path_en}" title="English"'))
        body = (f'<div class="ph cs-ph"><div class="w"><div class="cs-crumb"><a href="/en/index.html">Home</a> › {crumb}</div>'
                f'<span class="eyebrow">Construction Handbook · QA/QC · QS · CCM · Supervision</span><h1>{esc(h1)}</h1>{"<p>" + _en_links(lead) + "</p>" if lead else ""}</div></div>\n'
                f'<div class="w cs-wrap">{side(cur)}<article class="cs-tx">{f"<div class=cs-meta>Quan Construction · updated {upd}</div>" if upd else ""}{_en_links(inner)}'
                f'<p style="font-size:14px;color:var(--mut)">Linked legal documents and downloadable forms are in Vietnamese. <a href="{path_vi}" hreflang="vi">View this page in Vietnamese</a>.</p>'
                f'<p style="margin-top:26px"><a class="btn p" href="/en/lien-he.html" style="color:#fff">Need project management, cost estimating or supervision support? Contact Quan Construction →</a></p></article></div>')
        ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/en/index.html"},
            {"@type": "ListItem", "position": 2, "name": "Construction Handbook", "item": SITE + "/en/so-tay-xay-dung.html"}] +
            ([{"@type": "ListItem", "position": 3, "name": h1, "item": url}] if cur else [])}]
        if extra_ld: ld.append(extra_ld)
        jl = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
        t = esc((title if len(title) <= 70 else title[:68].rsplit(" ", 1)[0] + "…") + " | Quan Construction")
        de = esc(desc)
        return ('<!doctype html><!-- Created by: Quang Mai Phú – Construction Handbook, English (generated by _cong-cu/tao-so-tay-xay-dung.py) -->\n'
                '<html lang="en"><head><meta charset="utf-8"><script src="/js/thong-ke.js?v=2"></script><meta name="viewport" content="width=device-width,initial-scale=1">\n'
                f'<title>{t}</title><meta name="description" content="{de}">'
                f'<link rel="alternate" hreflang="vi" href="{vi}"><link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="x-default" href="{vi}"><link rel="canonical" href="{url}">\n'
                f'<meta property="og:title" content="{t}"><meta property="og:description" content="{de}"><meta property="og:type" content="article"><meta property="og:locale" content="en_US"><meta property="og:url" content="{url}"><meta property="og:image" content="https://quanconstruction.biz.vn/img/logo.png">\n'
                '<meta name="theme-color" content="#0a1d3f"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
                f'<link rel="stylesheet" href="/css/style.css?v=74">{CSS}{jl}</head><body>\n{h}\n{body}\n{foot}')

    for t in pages:
        body = []
        for k, v in t["body"]:
            if k == "bieu-mau":
                g, n = bieu_mau_groups(); body += g
            else:
                body.append((k, v))
        if t["slug"] == "bieu-mau":
            n = len(json.load(open(P("_cong-cu", "bieu-mau-danh-sach.json"), encoding="utf-8")))
            body = [(k, v.replace("{N}", str(n)) if isinstance(v, str) else v) for k, v in body]
            t = dict(t, summary=t["summary"].replace("{N}", str(n)), desc=t["desc"].replace("{N}", str(n)))
        pv, pe = f'/so-tay-xay-dung/{t["slug"]}.html', f'/en/so-tay-xay-dung/{t["slug"]}.html'
        faq = [(a, b) for k, v in body if k == "faq" for a, b in v]
        ld = ({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "en", "mainEntity": [
                {"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", b)}} for a, b in faq]} if faq else
              {"@context": "https://schema.org", "@type": "Article", "headline": t["title"], "description": t["desc"], "dateModified": t["ngay"],
               "inLanguage": "en", "mainEntityOfPage": SITE + pe, "author": {"@type": "Organization", "name": "Quan Construction", "url": SITE}})
        h = page(pv, pe, t["title"], t["desc"], f'<a href="/en/so-tay-xay-dung.html">Construction Handbook</a> › {esc(t["ngan"])}', t["title"], t.get("lead", ""),
                 render(body, True), t["slug"], ld, "/".join(reversed(t["ngay"].split("-"))))
        open(P("en", "so-tay-xay-dung", t["slug"] + ".html"), "w", encoding="utf-8").write(h)
    # Trang chủ nhánh tiếng Anh
    roles = "".join(f'<a href="/en/so-tay-xay-dung/{sl}.html"><b>{esc(a)}</b><span>{esc(b)}</span></a>' for a, b, sl in ch["VAI_TRO"] if sl in slugs)
    cards = []
    for nh, _ in cs.NHOM:
        ds = [t for t in pages if t["nhom"] == nh and not t.get("an_menu")]
        if ds:
            ten = nhom_en.get(nh, nh)
            n = len(json.load(open(P("_cong-cu", "bieu-mau-danh-sach.json"), encoding="utf-8")))
            cards.append(f"<h2>{esc(ten)}</h2><div class=cs-grid>" + "".join(
                f'<a class="cs-card" href="/en/so-tay-xay-dung/{t["slug"]}.html"><span class="cs-tag">{esc(ten)}</span><b>{esc(t["title"])}</b><span>{esc(t["summary"].replace("{N}", str(n)))}</span></a>' for t in ds) + "</div>")
    inner = (f'<p>{ch["GIOI_THIEU"]}</p><h2>By role</h2><div class="cs-roles">{roles}</div>' + "".join(cards) +
             '<div class="cs-note">This handbook summarizes Vietnamese regulations for reference and links to the full legal texts (in Vietnamese) in the Quan Construction <a href="/phap-ly.html">legal library</a>. It does not replace the legal documents or the opinion of competent authorities.</div>')
    open(P("en", "so-tay-xay-dung.html"), "w", encoding="utf-8").write(
        page("/so-tay-xay-dung.html", "/en/so-tay-xay-dung.html", ch["TIEU_DE"], ch["MO_TA"], "Construction Handbook", ch["TIEU_DE"], ch["LEAD"], inner, None))
    # Trang tiếng Việt: thêm hreflang en + nút đổi ngôn ngữ
    for pv, pe in [("/so-tay-xay-dung.html", "/en/so-tay-xay-dung.html")] + [(f'/so-tay-xay-dung/{sl}.html', f'/en/so-tay-xay-dung/{sl}.html') for sl in slugs]:
        f = P(pv.lstrip("/"))
        h = open(f, encoding="utf-8").read()
        if 'hreflang="en"' not in h.split("</head>")[0]:
            h = h.replace('<link rel="alternate" hreflang="x-default"', f'<link rel="alternate" hreflang="en" href="{SITE}{pe}"><link rel="alternate" hreflang="x-default"', 1)
        h = (h.replace('<a class="lg" href="/en/index.html">English</a>', f'<a class="lg" href="{pe}">English</a>')
             .replace('<a class="" href="/en/index.html" title="English"', f'<a class="" href="{pe}" title="English"'))
        open(f, "w", encoding="utf-8").write(h)
    # sitemap
    sm = open(P("sitemap.xml"), encoding="utf-8").read()
    sm = re.sub(r"<url><loc>https://quanconstruction\.biz\.vn/en/so-tay-xay-dung(?:\.html|/[^<]+)</loc>.*?</url>", "", sm)
    sm = sm.replace("</urlset>", f'<url><loc>{SITE}/en/so-tay-xay-dung.html</loc><lastmod>{max(t["ngay"] for t in pages)}</lastmod></url>' +
                    "".join(f'<url><loc>{SITE}/en/so-tay-xay-dung/{t["slug"]}.html</loc><lastmod>{t["ngay"]}</lastmod></url>' for t in pages) + "</urlset>")
    open(P("sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"Đã tạo bản tiếng Anh: trang chủ Sổ tay + {len(pages)} trang con")


if __name__ == "__main__":
    main()
    tao_en()
