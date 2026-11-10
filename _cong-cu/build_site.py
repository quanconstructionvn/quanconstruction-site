#!/usr/bin/env python3
"""Người tạo: Quang Mai Phú. Build SEO từ nội dung CMS, không sửa mã nguồn."""
import argparse
from datetime import datetime
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

SITE = 'https://quanconstruction.biz.vn'
INTERNAL = {'admin', 'hr', 'du-an', 'khach-hang'}
EXCLUDE = INTERNAL | {'_cong-cu', 'tests', 'docs', '.git', '.github', '__pycache__', '_site'}
# Internal applications are still published; they are excluded only from sitemap.
COPY_EXCLUDE = EXCLUDE - INTERNAL
esc = lambda value: html.escape(str(value or ''), quote=True)


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonical = attrs.get('href')
        if tag == 'meta' and attrs.get('name', '').lower() in ('robots', 'googlebot'):
            self.noindex |= 'noindex' in re.split(r'[\s,]+', attrs.get('content', '').lower())


def modified(root, path):
    result = subprocess.run(['git', '-C', str(root), 'log', '-1', '--format=%cs', '--', path],
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() or None


def slugify(title):
    plain = unicodedata.normalize('NFKD', title.replace('đ', 'd').replace('Đ', 'D'))
    slug = re.sub(r'[^a-z0-9]+', '-', plain.encode('ascii', 'ignore').decode().lower()).strip('-')
    return slug or 'tin-' + hashlib.sha256(title.encode()).hexdigest()[:10]


def article_path(item):
    slug = str(item.get('slug') or slugify(item['title'])).strip()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError('Slug chỉ gồm chữ thường không dấu, số và dấu gạch ngang')
    link = item.get('link') or f'/tin-tuc/{slug}.html'
    if not re.fullmatch(r'/tin-tuc/[a-z0-9]+(?:-[a-z0-9]+)*\.html', link):
        raise ValueError(f'Liên kết bài CMS không hợp lệ: {link}')
    return link


def safe_link(link):
    if not isinstance(link, str) or re.search(r'[\x00-\x20\\]', link):
        return False
    parsed = urlsplit(link)
    return ((link.startswith('/') and not link.startswith('//')) or
            (parsed.scheme == 'https' and bool(parsed.netloc)))


def jsonld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('<', '\\u003c') + '</script>'


def article(root, item, link, changed):
    title, desc = item['title'], item.get('summary', '')
    url = SITE + link
    paragraphs = ''.join('<p>' + esc(p).replace('\n', '<br>') + '</p>'
                         for p in re.split(r'\n\s*\n', item['body'].strip()) if p.strip())
    date = datetime.strptime(item['date'], '%d/%m/%Y').date().isoformat()
    data = {'@context': 'https://schema.org', '@type': 'Article', 'headline': title,
            'description': desc, 'datePublished': date, 'dateModified': max(date, changed or date),
            'inLanguage': 'vi', 'mainEntityOfPage': url,
            'author': {'@type': 'Person', 'name': 'Quang Mai Phú'},
            'publisher': {'@type': 'Organization', 'name': 'Quan Construction', 'url': SITE}}
    body = (f'<main><div class="ph"><div class="w"><p><a href="/">Trang chủ</a> › '
            f'<a href="/tin-tuc.html">Tin tức</a></p><h1>{esc(title)}</h1></div></div>'
            f'<section><article class="w seo-article"><p>Quang Mai Phú · {esc(item["date"])}</p>'
            f'<p><strong>{esc(desc)}</strong></p>{paragraphs}'
            '<p><a href="/xay-nha-tron-goi.html">Dịch vụ xây nhà trọn gói</a> · '
            '<a href="/du-toan-boc-khoi-luong.html">Dự toán và bóc khối lượng</a></p>'
            '<p><a class="btn p" href="/lien-he.html">Liên hệ tư vấn</a></p></article></section></main>')
    template = root / '_cong-cu/mau-trang-van-ban.html'
    if template.exists():
        page = template.read_text(encoding='utf-8')
        page = page.replace('trang toàn văn văn bản (tạo tự động bằng _cong-cu/tao-trang-phap-ly.py)',
                            'bài viết CMS (tạo tự động bằng _cong-cu/build_site.py)')
    else:
        page = '<html lang="vi"><head><title>{{TITLE}}</title><meta name="description" content="{{DESC}}"><link rel="canonical" href="{{URL}}">{{JSONLD}}</head><body>{{BODY}}</body></html>'
    values = {'TITLE': esc(title + ' | Quan Construction'), 'DESC': esc(desc), 'URL': esc(url),
              'JSONLD': jsonld(data), 'BODY': body}
    # One pass prevents a placeholder typed in CMS content being interpreted again.
    return re.sub(r'\{\{(TITLE|DESC|URL|JSONLD|BODY)\}\}', lambda m: values[m[1]], page)


def static_news(page, items, limit=0):
    cards = []
    for item in list(reversed(items))[:limit or None]:
        title = esc(item['title'])
        link = item.get('link', '')
        if link and safe_link(link):
            title = f'<a href="{esc(link)}">{title}</a>'
        cards.append(f'<div class="news rv in"><small>{esc(item.get("date"))}</small><h3>{title}</h3><p>{esc(item.get("summary"))}</p></div>')
    # The existing feed may have nested divs: use a depth-aware parser for its extent.
    pattern = r'<div\b[^>]*\bdata-feed="news"[^>]*>'
    match = re.search(pattern, page)
    if not match:
        return page
    depth = 1
    for tag in re.finditer(r'</?div\b[^>]*>', page[match.end():]):
        depth += -1 if tag[0].startswith('</') else 1
        if depth == 0:
            end = match.end() + tag.start()
            return page[:match.end()] + ''.join(cards) + page[end:]
    raise ValueError('Khối danh sách tin chưa đóng thẻ div')


def sitemap(root, output, changed_paths):
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    tree = ET.Element(f'{{{ns}}}urlset')
    entries = {}
    for file in sorted(output.rglob('*.html')):
        relative = file.relative_to(output)
        if relative.parts[0] in INTERNAL:
            continue
        meta = Metadata()
        meta.feed(file.read_text(encoding='utf-8'))
        if not meta.canonical or meta.noindex:
            continue
        parsed = urlsplit(meta.canonical)
        if parsed.scheme != 'https' or parsed.netloc != urlsplit(SITE).netloc or parsed.query or parsed.fragment:
            continue
        # A canonical must resolve to a published file; ignore non-canonical aliases.
        canonical_path = parsed.path.lstrip('/')
        canonical_file = output / (canonical_path + 'index.html' if parsed.path.endswith('/') else canonical_path)
        if canonical_file.resolve() != file.resolve():
            continue
        stamp = changed_paths.get(relative.as_posix()) or modified(root, relative.as_posix())
        entries[meta.canonical] = stamp
    for url, stamp in sorted(entries.items()):
        node = ET.SubElement(tree, f'{{{ns}}}url')
        ET.SubElement(node, f'{{{ns}}}loc').text = url
        if stamp:
            ET.SubElement(node, f'{{{ns}}}lastmod').text = stamp
    ET.ElementTree(tree).write(output / 'sitemap.xml', encoding='utf-8', xml_declaration=True)


def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output == root or root.is_relative_to(output):
        raise ValueError('Thư mục output không được chứa mã nguồn')
    if output.is_relative_to(root) and output.parent != root:
        raise ValueError('Output trong repo phải nằm trực tiếp ở thư mục gốc')
    if output.exists() and not (output / '.seo-build-output').exists():
        raise ValueError('Output đã tồn tại và không phải thư mục build SEO')
    data = json.loads((root / 'content/tin-tuc.json').read_text(encoding='utf-8'))
    items = data['items']
    owned, generated = set(), []
    for item in items:
        if item.get('link') and not safe_link(item['link']):
            raise ValueError(f'Liên kết tin không an toàn: {item["link"]}')
        if str(item.get('body') or '').strip():
            link = article_path(item)
            if link in owned or any(x is not item and x.get('link') == link for x in items):
                raise ValueError(f'Trùng đường dẫn bài viết: {link}')
            owned.add(link)
            datetime.strptime(item['date'], '%d/%m/%Y')
            generated.append((item, link))
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / '.seo-build-output').write_text('Người tạo: Quang Mai Phú\n')
    for path in root.iterdir():
        if path.name in COPY_EXCLUDE or path == output or path.name.startswith('.'):
            continue
        target = output / path.name
        if path.is_dir():
            shutil.copytree(path, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        else:
            shutil.copy2(path, target)
    changed = modified(root, 'content/tin-tuc.json')
    changed_paths = {}
    for item, link in generated:
        path = output / link.lstrip('/')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(article(root, item, link, changed), encoding='utf-8')
        item['link'] = link
        changed_paths[link.lstrip('/')] = max(datetime.strptime(item['date'], '%d/%m/%Y').date().isoformat(), changed or '')
    (output / 'content/tin-tuc.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for path, limit in [('tin-tuc.html', 0), ('index.html', 3)]:
        file = output / path
        if file.exists():
            file.write_text(static_news(file.read_text(encoding='utf-8'), items, limit), encoding='utf-8')
            changed_paths[path] = max(filter(None, [changed, modified(root, path)]), default=None)
    sitemap(root, output, changed_paths)
    (output / '.nojekyll').touch()
    print(f'Build hoàn tất: {len(generated)} bài CMS, {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='_site')
    args = parser.parse_args()
    build(Path(__file__).resolve().parents[1], Path(args.output))
