#!/usr/bin/env python3
"""Người tạo: Quang Mai Phú. Kiểm tra bản xuất bản trước khi deploy."""
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

SITE = 'https://quanconstruction.biz.vn'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals, self.descriptions, self.links, self.schemas = [], [], [], []
        self.h1 = 0
        self.ld = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a.get('href'))
        if tag == 'meta' and a.get('name') == 'description':
            self.descriptions.append(a.get('content'))
        if tag == 'h1':
            self.h1 += 1
        if tag == 'a':
            self.links.append(a.get('href', ''))
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.ld = ''

    def handle_data(self, data):
        if self.ld is not None:
            self.ld += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.ld is not None:
            self.schemas.append(json.loads(self.ld))
            self.ld = None


def check(root):
    root = Path(root)
    urls = [e.text for e in ET.parse(root / 'sitemap.xml').findall('.//{*}loc')]
    assert len(urls) == len(set(urls)), 'Sitemap trùng URL'
    for url in urls:
        parsed = urlsplit(url)
        assert parsed.scheme == 'https' and parsed.netloc == urlsplit(SITE).netloc, url
        path = unquote(parsed.path).lstrip('/')
        file = root / (path + 'index.html' if parsed.path.endswith('/') else path)
        assert file.is_file(), f'URL sitemap không có file: {url}'
        assert path.split('/')[0] not in {'admin', 'hr', 'du-an', 'khach-hang'}, url
    services = ['xay-nha-tron-goi.html', 'du-toan-boc-khoi-luong.html']
    for name in ['index.html', 'dich-vu.html', 'tin-tuc.html', 'so-do-trang.html', *services]:
        file = root / name
        text = file.read_text(encoding='utf-8')
        page = Page()
        page.feed(text)
        assert len(page.canonicals) == 1 and page.canonicals[0] in urls, name
        assert page.h1 == 1 and len(page.descriptions) == 1 and page.descriptions[0], name
        assert '{{TITLE}}' not in text and '{{BODY}}' not in text, name
        if name in services:
            assert any(x.get('@type') == 'Service' for x in page.schemas), name
        for link in page.links:
            p = urlsplit(link)
            if p.scheme or p.netloc or not p.path:
                continue
            target = root / p.path.lstrip('/') if p.path.startswith('/') else file.parent / p.path
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), f'Liên kết hỏng trong {name}: {link}'
    for name in ['index.html', 'dich-vu.html']:
        text = (root / name).read_text(encoding='utf-8')
        assert all('/' + path in text for path in services), name
    directory = Page()
    directory.feed((root / 'so-do-trang.html').read_text(encoding='utf-8'))
    linked = {SITE + link for link in directory.links if link.startswith('/')}
    assert set(urls).issubset(linked), 'Có URL sitemap chưa được liên kết từ sơ đồ HTML'
    for name in ['.git', '.github', '_cong-cu', 'tests', 'docs']:
        assert not (root / name).exists(), name
    assert (root / 'CNAME').read_text().strip() == urlsplit(SITE).netloc
    assert 'Sitemap: ' + SITE + '/sitemap.xml' in (root / 'robots.txt').read_text()
    assert (root / 'googleb558cccccb2164bf.html').exists(), 'Thiếu file xác minh Google cũ'
    print(f'SEO hợp lệ: {len(urls)} URL sitemap, 2 trang dịch vụ, liên kết và JSON-LD đúng.')


if __name__ == '__main__':
    check(sys.argv[1] if len(sys.argv) > 1 else '_site')
