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


def block(k, v):
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
        d = open(P("_cong-cu", "so-tay-du-lieu", v[1]), encoding="utf-8").read().replace("</", "<\\/")
        return (f'<script type="application/json" data-st="{v[0]}">{d}</script>'
                '<noscript><p>Công cụ này cần bật JavaScript.</p></noscript><script src="/js/so-tay-tuong-tac.js?v=1" defer></script>')
    raise ValueError(k)


def render(blocks):
    out, toc, n = [], [], 0
    for k, v in blocks:
        if k == "h2":
            n += 1; toc.append(v); out.append(f'<h2 id="m{n}">{esc(v)}</h2>')
        else:
            out.append(block(k, v))
    t = ('<nav class="cs-toc"><b>Nội dung trang</b><ol>' + "".join(f'<li><a href="#m{i+1}">{esc(x)}</a></li>' for i, x in enumerate(toc)) + "</ol></nav>") if len(toc) >= 4 else ""
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
            ds = [t for t in pages if t["nhom"] == nhom]
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
        ds = [t for t in pages if t["nhom"] == nhom]
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


if __name__ == "__main__":
    main()
