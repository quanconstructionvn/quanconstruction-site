# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Tạo trang tĩnh cho bài viết hướng dẫn (tin-tuc/<slug>.html) từ _cong-cu/bai-viet.py,
# thêm bài vào content/tin-tuc.json (mục Tin tức) và sitemap.xml.
# Chạy từ thư mục gốc website:  python3 _cong-cu/tao-bai-viet.py
# Đăng theo lịch (Quang Mai Phú): bài có "date" sau ngày hôm nay (giờ Việt Nam) chưa được tạo trang,
# chưa vào Tin tức và sitemap; GitHub Actions chạy lại mỗi sáng nên bài tự lên web đúng ngày.
#   XEM_TRUOC=1  -> tạo cả bài hẹn ngày (chỉ để xem trước trên máy, KHÔNG commit kết quả này)
#   NGAY_DANG=YYYY-MM-DD -> giả lập "hôm nay" để thử lịch đăng
import json, os, re, html, glob, importlib.util
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://quanconstruction.biz.vn"
P = lambda *a: os.path.join(ROOT, *a)
esc = lambda s: html.escape(str(s or ""), quote=True)
fmt = lambda x: "/".join(reversed(x.split("-")))

spec = importlib.util.spec_from_file_location("bai_viet", P("_cong-cu", "bai-viet.py"))
bv = importlib.util.module_from_spec(spec); spec.loader.exec_module(bv)
# Người tạo: Quang Mai Phú – nội dung chuyên môn bổ trợ hai dịch vụ.
with open(P("_cong-cu", "bai-viet-dich-vu.json"), encoding="utf-8") as service_content:
    bv.BAI.extend(json.load(service_content)["articles"])
HOM_NAY = os.environ.get("NGAY_DANG") or datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d")
XEM_TRUOC = os.environ.get("XEM_TRUOC") == "1"
DA_DANG = [b for b in bv.BAI if XEM_TRUOC or b["date"] <= HOM_NAY]
CHO_DANG = [b for b in bv.BAI if b not in DA_DANG]
# Bản tiếng Anh (Quang Mai Phú): _cong-cu/bai-viet-en/<slug>.json = {"title","desc","summary","body"} (body cùng định dạng khối)
EN_DIR = P("_cong-cu", "bai-viet-en")
def _en(b):
    f = os.path.join(EN_DIR, b["slug"] + ".json")
    if not os.path.exists(f): return None
    with open(f, encoding="utf-8") as stream: return json.load(stream)
EN = {b["slug"]: _en(b) for b in DA_DANG if _en(b)}

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


def merge_news_items(existing, generated, owned_links):
    """Người tạo: Quang Mai Phú – không làm mất bài CMS khi chạy lịch đăng."""
    kept = [item for item in existing if item.get('link') not in owned_links or str(item.get('body') or '').strip()]
    overrides = {item.get('link') for item in kept if item.get('link')}
    return kept + [item for item in generated if item.get('link') not in overrides]


def main():
    tpl = open(P("_cong-cu", "mau-trang-van-ban.html"), encoding="utf-8").read()
    tpl = re.sub(r"<style>\n\.vb-ph.*?</style>", lambda m: CSS, tpl, flags=re.S)
    tpl = tpl.replace("trang toàn văn văn bản (tạo tự động bằng _cong-cu/tao-trang-phap-ly.py)", "bài viết hướng dẫn (tạo tự động bằng _cong-cu/tao-bai-viet.py)")
    tpl = tpl.replace('<a href="/phap-ly.html" class=on>Pháp lý</a>', '<a href="/phap-ly.html">Pháp lý</a>').replace('<a href="/tin-tuc.html">Tin tức</a>', '<a href="/tin-tuc.html" class=on>Tin tức</a>', 1)
    os.makedirs(P("tin-tuc"), exist_ok=True)
    for b in CHO_DANG:  # bài chưa tới ngày: xóa trang nếu lỡ có
        f = P("tin-tuc", b["slug"] + ".html")
        if os.path.exists(f): os.remove(f)
    for b in DA_DANG:
        url = f'{SITE}/tin-tuc/{b["slug"]}.html'
        others = "".join(f'<a href="/tin-tuc/{x["slug"]}.html">{esc(x["title"])}</a>' for x in [y for y in reversed(DA_DANG) if y["slug"] != b["slug"]][:12])  # 12 bài mới nhất
        category = esc(b.get('category', 'Hướng dẫn pháp lý'))
        body = (f'<div class="ph bv-ph"><div class="w"><div class="bv-crumb"><a href="/index.html">Trang chủ</a> › <a href="/tin-tuc.html">Tin tức</a> › {category}</div>'
                f'<span class="eyebrow">{category}</span><h1>{esc(b["title"])}</h1></div></div>\n'
                f'<div class="w bv-wrap"><article class="bv-tx"><div class="bv-meta">Quan Construction · {fmt(b["date"])}</div>{render(b["body"])}'
                f'<p style="margin-top:26px"><a class="btn p" href="/phap-ly.html" style="color:#fff">Tra cứu toàn văn pháp luật miễn phí →</a></p></article>'
                f'<aside class="bv-side"><div class="bv-cta"><b style="font-size:17px">Cần hỗ trợ thủ tục, thiết kế, thi công?</b><p>Quan Construction đồng hành từ xin phép đến khi vào ở.</p><a class="btn p" href="/lien-he.html">Liên hệ tư vấn</a></div>'
                f'<div class="bv-box"><h3>Bài viết khác</h3>{others}</div>'
                f'<div class="bv-box"><h3>Tra cứu nhanh</h3><a href="/phap-ly/135-2025-qh15.html">Luật Xây dựng 2025</a><a href="/phap-ly/217-2026-nd-cp.html">Nghị định 217/2026 (giấy phép xây dựng)</a><a href="/phap-ly/31-2024-qh15.html">Luật Đất đai 2024</a><a href="/phap-ly.html">Tất cả văn bản</a></div></aside></div>')
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": b["title"], "description": b["desc"], "datePublished": b["date"], "dateModified": b["date"],
               "inLanguage": "vi", "mainEntityOfPage": url, "image": SITE + "/favicon-512x512.png",
               "author": ({"@type": "Person", "name": b["author"]} if b.get("author") else {"@type": "Organization", "name": "Quan Construction", "url": SITE}),
               "publisher": {"@type": "Organization", "name": "Công ty TNHH Đầu tư và Phát triển Quan Construction", "logo": {"@type": "ImageObject", "url": SITE + "/favicon-512x512.png"}}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": "Tin tức", "item": SITE + "/tin-tuc.html"},
                  {"@type": "ListItem", "position": 3, "name": b["title"], "item": url}]}]
        jl = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
        title = b["title"] if len(b["title"]) <= 70 else b["title"][:68].rsplit(" ", 1)[0] + "…"
        page = (tpl.replace("{{TITLE}}", esc(title + " | Quan Construction")).replace("{{DESC}}", esc(b["desc"])).replace("{{URL}}", url)
                .replace("{{JSONLD}}", jl).replace("{{BODY}}", body).replace('<meta property="og:type" content="article">', '<meta property="og:type" content="article">'))
        if b["slug"] in EN:
            eu = f'{SITE}/en/tin-tuc/{b["slug"]}.html'
            page = (page.replace(f'<link rel="alternate" hreflang="x-default"', f'<link rel="alternate" hreflang="en" href="{eu}"><link rel="alternate" hreflang="x-default"', 1)
                    .replace('<a class="lg" href="/en/index.html">English</a>', f'<a class="lg" href="/en/tin-tuc/{b["slug"]}.html">English</a>')
                    .replace('<a class="" href="/en/index.html" title="English"', f'<a class="" href="/en/tin-tuc/{b["slug"]}.html" title="English"'))
        open(P("tin-tuc", b["slug"] + ".html"), "w", encoding="utf-8").write(page)
    tao_en()
    # Tin tức (content/tin-tuc.json): thêm/cập nhật bài theo link
    tt = json.load(open(P("content", "tin-tuc.json"), encoding="utf-8"))
    items = []
    for b in sorted(DA_DANG, key=lambda x: x["date"]):
        it = {"date": fmt(b["date"]), "title": b["title"], "summary": b["summary"], "body": "", "image": "", "link": f'/tin-tuc/{b["slug"]}.html'}
        if b["slug"] in EN:
            it.update(title_en=EN[b["slug"]]["title"], summary_en=EN[b["slug"]]["summary"], link_en=f'/en/tin-tuc/{b["slug"]}.html')
        items.append(it)
    tt["items"] = merge_news_items(tt.get("items", []), items, {f'/tin-tuc/{b["slug"]}.html' for b in bv.BAI})
    json.dump(tt, open(P("content", "tin-tuc.json"), "w", encoding="utf-8"), ensure_ascii=False)
    # sitemap
    sm = open(P("sitemap.xml"), encoding="utf-8").read()
    sm = re.sub(r"<url><loc>https://quanconstruction\.biz\.vn/(en/)?tin-tuc/[^<]+</loc>.*?</url>", "", sm)
    sm = sm.replace("</urlset>", "".join(f'<url><loc>{SITE}/tin-tuc/{b["slug"]}.html</loc><lastmod>{b["date"]}</lastmod></url>' for b in DA_DANG)
                    + "".join(f'<url><loc>{SITE}/en/tin-tuc/{b["slug"]}.html</loc><lastmod>{b["date"]}</lastmod></url>' for b in DA_DANG if b["slug"] in EN) + "</urlset>")
    open(P("sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"Đã tạo {len(DA_DANG)} bài viết (hôm nay {HOM_NAY}); {len(CHO_DANG)} bài hẹn ngày đăng; {len(EN)} bài tiếng Anh")


def _en_tpl():
    """Khung trang tiếng Anh lấy header/footer từ en/tin-tuc.html, đổi đường dẫn tương đối thành tuyệt đối."""
    s = open(P("en", "tin-tuc.html"), encoding="utf-8").read()
    def absol(x):
        x = re.sub(r'(href|src)="\.\./', r'\1="/', x)
        return re.sub(r'(href|src)="(?!/|https?:|tel:|mailto:|#)([^"]+)"', r'\1="/en/\2"', x)
    hdr = absol(s[s.index("<header"):s.index("</header>") + 9])
    foot = absol(s[s.index('<div class="fab"'):]).replace('<script src="/js/content.js?v=71"></script>', '')
    return hdr, foot


def _en_links(h, slugs):
    """Liên kết nội bộ trong bài tiếng Anh: trỏ sang bản tiếng Anh nếu có."""
    def f(m):
        u = m.group(1)
        if u.startswith("/tin-tuc/"):
            sl = u[9:-5]
            return f'href="/en{u}"' if sl in slugs else m.group(0)
        if not u.startswith("/phap-ly") and os.path.exists(P("en", u.lstrip("/"))):
            return f'href="/en{u}"'
        return m.group(0)
    return re.sub(r'href="(/[a-z0-9/-]+\.html)"', f, h)


def tao_en():
    hdr, foot = _en_tpl()
    os.makedirs(P("en", "tin-tuc"), exist_ok=True)
    for f in glob.glob(P("en", "tin-tuc", "*.html")):
        if os.path.basename(f)[:-5] not in EN: os.remove(f)
    ds = [b for b in DA_DANG if b["slug"] in EN]
    for b in ds:
        e = EN[b["slug"]]
        url, vi = f'{SITE}/en/tin-tuc/{b["slug"]}.html', f'{SITE}/tin-tuc/{b["slug"]}.html'
        others = "".join(f'<a href="/en/tin-tuc/{x["slug"]}.html">{esc(EN[x["slug"]]["title"])}</a>' for x in [y for y in reversed(ds) if y["slug"] != b["slug"]][:12])
        h = (hdr.replace('<a class="lg" href="/tin-tuc.html">', f'<a class="lg" href="/tin-tuc/{b["slug"]}.html">')
             .replace('<a class="" href="/tin-tuc.html" title="Tiếng Việt"', f'<a class="" href="/tin-tuc/{b["slug"]}.html" title="Tiếng Việt"')
             .replace('<a class="on" href="/en/tin-tuc.html" title="English"', f'<a class="on" href="/en/tin-tuc/{b["slug"]}.html" title="English"'))
        body = (f'<div class="ph bv-ph"><div class="w"><div class="bv-crumb"><a href="/en/index.html">Home</a> › <a href="/en/tin-tuc.html">News</a> › Legal guide</div>'
                f'<span class="eyebrow">Legal guide</span><h1>{esc(e["title"])}</h1></div></div>\n'
                f'<div class="w bv-wrap"><article class="bv-tx"><div class="bv-meta">Quan Construction · {fmt(b["date"])}</div>{_en_links(render(e["body"]), EN)}'
                f'<p style="font-size:14px;color:var(--mut)">Linked legal documents open in their original Vietnamese text. <a href="/tin-tuc/{b["slug"]}.html" hreflang="vi">Read this article in Vietnamese</a>.</p></article>'
                f'<aside class="bv-side"><div class="bv-cta"><b style="font-size:17px">Need help with permits, design or construction?</b><p>Quan Construction supports you from the building permit to handover.</p><a class="btn p" href="/en/lien-he.html">Contact us</a></div>'
                + (f'<div class="bv-box"><h3>More articles</h3>{others}</div>' if others else "") +
                f'<div class="bv-box"><h3>Quick reference (Vietnamese)</h3><a href="/phap-ly/135-2025-qh15.html">Construction Law 2025</a><a href="/phap-ly/217-2026-nd-cp.html">Decree 217/2026 (building permits)</a><a href="/phap-ly/31-2024-qh15.html">Land Law 2024</a></div></aside></div>')
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": e["title"], "description": e["desc"], "datePublished": b["date"], "dateModified": b["date"],
               "inLanguage": "en", "mainEntityOfPage": url, "image": SITE + "/favicon-512x512.png",
               "author": ({"@type": "Person", "name": b["author"]} if b.get("author") else {"@type": "Organization", "name": "Quan Construction", "url": SITE}),
               "publisher": {"@type": "Organization", "name": "Quan Construction Investment and Development Company Limited", "logo": {"@type": "ImageObject", "url": SITE + "/favicon-512x512.png"}}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/en/index.html"},
                  {"@type": "ListItem", "position": 2, "name": "News", "item": SITE + "/en/tin-tuc.html"},
                  {"@type": "ListItem", "position": 3, "name": e["title"], "item": url}]}]
        jl = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
        t = esc((e["title"] if len(e["title"]) <= 70 else e["title"][:68].rsplit(" ", 1)[0] + "…") + " | Quan Construction")
        d = esc(e["desc"])
        page = ('<!doctype html><!-- Created by: Quang Mai Phú – English article (generated by _cong-cu/tao-bai-viet.py) -->\n'
                '<html lang="en"><head><meta charset="utf-8"><script src="/js/thong-ke.js?v=2"></script><meta name="viewport" content="width=device-width,initial-scale=1">\n'
                f'<title>{t}</title><meta name="description" content="{d}">'
                f'<link rel="alternate" hreflang="vi" href="{vi}"><link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="x-default" href="{vi}"><link rel="canonical" href="{url}">\n'
                f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:type" content="article"><meta property="og:locale" content="en_US"><meta property="og:url" content="{url}"><meta property="og:image" content="https://quanconstruction.biz.vn/img/logo.png">\n'
                '<meta name="theme-color" content="#0a1d3f"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
                f'<link rel="stylesheet" href="/css/style.css?v=74">{CSS}{jl}</head><body>\n{h}\n{body}\n{foot}')
        open(P("en", "tin-tuc", b["slug"] + ".html"), "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    main()
