# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Tạo trang tĩnh cho bài viết hướng dẫn (tin-tuc/<slug>.html) từ _cong-cu/bai-viet.py,
# thêm bài vào content/tin-tuc.json (mục Tin tức) và sitemap.xml.
# Chạy từ thư mục gốc website:  python3 _cong-cu/tao-bai-viet.py
import json, os, re, html, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://quanconstruction.biz.vn"
P = lambda *a: os.path.join(ROOT, *a)
esc = lambda s: html.escape(str(s or ""), quote=True)
fmt = lambda x: "/".join(reversed(x.split("-")))

spec = importlib.util.spec_from_file_location("bai_viet", P("_cong-cu", "bai-viet.py"))
bv = importlib.util.module_from_spec(spec); spec.loader.exec_module(bv)

CSS = """<style>
.bv-ph{padding:40px 0 44px}.bv-ph h1{font-size:clamp(24px,4vw,38px);line-height:1.25;margin-top:8px;max-width:900px}
.bv-crumb{font-size:13.5px;margin-bottom:6px}.bv-crumb a{color:inherit;opacity:.85;text-decoration:underline}
.bv-wrap{display:grid;grid-template-columns:minmax(0,760px) 300px;gap:40px;padding-top:34px;padding-bottom:60px;align-items:start}
.bv-tx{font-size:16.5px;line-height:1.8;color:#1d2a44}.bv-tx h2{font-size:22px;color:var(--navy);margin:30px 0 10px}
.bv-tx p{margin:0 0 14px}.bv-tx ul,.bv-tx ol{margin:0 0 16px;padding-left:22px}.bv-tx li{margin:0 0 8px}
.bv-tx a{color:var(--blue);font-weight:600}.bv-meta{font-size:14px;color:var(--mut);margin-bottom:18px}
.bv-note{background:#fff8e6;border:1px solid #f1dca0;border-radius:10px;padding:12px 16px;margin:24px 0;font-size:14.5px}
.bv-side{position:sticky;top:12px;display:flex;flex-direction:column;gap:14px}
.bv-box{border:1px solid var(--line);border-radius:14px;padding:16px;background:#fff}.bv-box h3{font-size:15px;color:var(--navy);margin:0 0 10px}
.bv-box a{display:block;font-size:14px;line-height:1.45;padding:6px 0;color:#26406b;text-decoration:none;border-top:1px dashed var(--line)}.bv-box a:first-of-type{border-top:0}
.bv-cta{background:var(--navy);color:#fff;border-radius:14px;padding:18px}.bv-cta p{margin:0 0 12px;font-size:14.5px;opacity:.92}
@media(max-width:900px){.bv-wrap{grid-template-columns:1fr}.bv-side{position:static}}
</style>"""


def render(blocks):
    out = []
    for k, v in blocks:
        if k == "h2": out.append(f"<h2>{esc(v)}</h2>")
        elif k == "p": out.append(f"<p>{v}</p>")
        elif k in ("ul", "ol"): out.append(f"<{k}>" + "".join(f"<li>{x}</li>" for x in v) + f"</{k}>")
        elif k == "note": out.append(f'<div class="bv-note">{v}</div>')
    return "".join(out)


def main():
    tpl = open(P("_cong-cu", "mau-trang-van-ban.html"), encoding="utf-8").read()
    tpl = re.sub(r"<style>\n\.vb-ph.*?</style>", lambda m: CSS, tpl, flags=re.S)
    tpl = tpl.replace("trang toàn văn văn bản (tạo tự động bằng _cong-cu/tao-trang-phap-ly.py)", "bài viết hướng dẫn (tạo tự động bằng _cong-cu/tao-bai-viet.py)")
    tpl = tpl.replace('<a href="/phap-ly.html" class=on>Pháp lý</a>', '<a href="/phap-ly.html">Pháp lý</a>').replace('<a href="/tin-tuc.html">Tin tức</a>', '<a href="/tin-tuc.html" class=on>Tin tức</a>', 1)
    os.makedirs(P("tin-tuc"), exist_ok=True)
    for b in bv.BAI:
        url = f'{SITE}/tin-tuc/{b["slug"]}.html'
        others = "".join(f'<a href="/tin-tuc/{x["slug"]}.html">{esc(x["title"])}</a>' for x in bv.BAI if x["slug"] != b["slug"])
        body = (f'<div class="ph bv-ph"><div class="w"><div class="bv-crumb"><a href="/index.html">Trang chủ</a> › <a href="/tin-tuc.html">Tin tức</a> › Hướng dẫn pháp lý</div>'
                f'<span class="eyebrow">Hướng dẫn pháp lý</span><h1>{esc(b["title"])}</h1></div></div>\n'
                f'<div class="w bv-wrap"><article class="bv-tx"><div class="bv-meta">Quan Construction · {fmt(b["date"])}</div>{render(b["body"])}'
                f'<p style="margin-top:26px"><a class="btn p" href="/phap-ly.html" style="color:#fff">Tra cứu toàn văn pháp luật miễn phí →</a></p></article>'
                f'<aside class="bv-side"><div class="bv-cta"><b style="font-size:17px">Cần hỗ trợ thủ tục, thiết kế, thi công?</b><p>Quan Construction đồng hành từ xin phép đến khi vào ở.</p><a class="btn p" href="/lien-he.html">Liên hệ tư vấn</a></div>'
                f'<div class="bv-box"><h3>Bài viết khác</h3>{others}</div>'
                f'<div class="bv-box"><h3>Tra cứu nhanh</h3><a href="/phap-ly/135-2025-qh15.html">Luật Xây dựng 2025</a><a href="/phap-ly/217-2026-nd-cp.html">Nghị định 217/2026 (giấy phép xây dựng)</a><a href="/phap-ly/31-2024-qh15.html">Luật Đất đai 2024</a><a href="/phap-ly.html">Tất cả văn bản</a></div></aside></div>')
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": b["title"], "description": b["desc"], "datePublished": b["date"], "dateModified": b["date"],
               "inLanguage": "vi", "mainEntityOfPage": url, "image": SITE + "/favicon-512x512.png",
               "author": {"@type": "Organization", "name": "Quan Construction", "url": SITE},
               "publisher": {"@type": "Organization", "name": "Công ty TNHH Đầu tư và Phát triển Quan Construction", "logo": {"@type": "ImageObject", "url": SITE + "/favicon-512x512.png"}}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": "Tin tức", "item": SITE + "/tin-tuc.html"},
                  {"@type": "ListItem", "position": 3, "name": b["title"], "item": url}]}]
        jl = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
        title = b["title"] if len(b["title"]) <= 70 else b["title"][:68].rsplit(" ", 1)[0] + "…"
        page = (tpl.replace("{{TITLE}}", esc(title + " | Quan Construction")).replace("{{DESC}}", esc(b["desc"])).replace("{{URL}}", url)
                .replace("{{JSONLD}}", jl).replace("{{BODY}}", body).replace('<meta property="og:type" content="article">', '<meta property="og:type" content="article">'))
        open(P("tin-tuc", b["slug"] + ".html"), "w", encoding="utf-8").write(page)
    # Tin tức (content/tin-tuc.json): thêm/cập nhật bài theo link
    tt = json.load(open(P("content", "tin-tuc.json"), encoding="utf-8"))
    items = [x for x in tt.get("items", []) if not str(x.get("link", "")).startswith("/tin-tuc/")]
    for b in sorted(bv.BAI, key=lambda x: x["date"]):
        items.append({"date": fmt(b["date"]), "title": b["title"], "summary": b["summary"], "body": "", "image": "", "link": f'/tin-tuc/{b["slug"]}.html'})
    tt["items"] = items
    json.dump(tt, open(P("content", "tin-tuc.json"), "w", encoding="utf-8"), ensure_ascii=False)
    # sitemap
    sm = open(P("sitemap.xml"), encoding="utf-8").read()
    sm = re.sub(r"<url><loc>https://quanconstruction\.biz\.vn/tin-tuc/[^<]+</loc>.*?</url>", "", sm)
    sm = sm.replace("</urlset>", "".join(f'<url><loc>{SITE}/tin-tuc/{b["slug"]}.html</loc><lastmod>{b["date"]}</lastmod></url>' for b in bv.BAI) + "</urlset>")
    open(P("sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"Đã tạo {len(bv.BAI)} bài viết")


if __name__ == "__main__":
    main()
