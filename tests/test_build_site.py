# Người tạo: Quang Mai Phú
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / '_cong-cu/build_site.py'


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'src'
        self.out = Path(self.tmp.name) / 'out'
        self.root.mkdir()
        (self.root / 'content').mkdir()
        (self.root / 'tin-tuc').mkdir()
        self.page('index.html', '/')
        self.page('tin-tuc.html', '/tin-tuc.html', '<div data-feed="news"><p>OLD</p></div>')
        self.page('tin-tuc/cu.html', '/tin-tuc/cu.html', 'BÀI CŨ')
        self.items = [{'title': 'Tin cũ', 'date': '10/11/2026', 'link': '/tin-tuc/cu.html', 'body': ''},
                      {'title': 'Dự toán & khối lượng', 'slug': 'du-toan', 'date': '10/11/2026',
                       'summary': 'Tóm tắt', 'body': 'Đoạn đầu.\n\n<script>alert(1)</script>'}]

    def page(self, path, canonical, body=''):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'<html><head><title>Test</title><link rel="canonical" href="https://quanconstruction.biz.vn{canonical}"></head><body>{body}</body></html>')

    def run_build(self):
        (self.root / 'content/tin-tuc.json').write_text(json.dumps({'items': self.items}))
        self.assertTrue(SCRIPT.exists(), 'Chưa có trình build SEO tự động')
        spec = importlib.util.spec_from_file_location('build_site', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.build(self.root, self.out)

    def test_cms_article_static_feed_and_legacy_preserved(self):
        self.run_build()
        article = (self.out / 'tin-tuc/du-toan.html').read_text()
        self.assertIn('Dự toán &amp; khối lượng', article)
        self.assertIn('&lt;script&gt;', article)
        self.assertNotIn('<script>alert', article)
        self.assertIn('"datePublished": "2026-11-10"', article)
        self.assertIn('BÀI CŨ', (self.out / 'tin-tuc/cu.html').read_text())
        self.assertIn('/tin-tuc/du-toan.html', (self.out / 'tin-tuc.html').read_text())
        self.assertNotIn('link', json.loads((self.root / 'content/tin-tuc.json').read_text())['items'][1])

    def test_sitemap_excludes_internal_noindex_duplicates_and_external(self):
        self.page('admin/index.html', '/admin/')
        self.page('hr/index.html', '/hr/')
        self.page('du-an/index.html', '/du-an/')
        self.page('khach-hang/index.html', '/khach-hang/')
        self.page('index-copy.html', '/')
        self.page('hidden.html', '/hidden.html', '')
        p = self.root / 'hidden.html'
        p.write_text(p.read_text().replace('</head>', '<meta name="robots" content="noindex,follow"></head>'))
        self.page('external.html', 'https://example.com')
        self.run_build()
        urls = [e.text for e in ET.parse(self.out / 'sitemap.xml').findall('.//{*}loc')]
        self.assertEqual(urls.count('https://quanconstruction.biz.vn/'), 1)
        self.assertIn('https://quanconstruction.biz.vn/tin-tuc/du-toan.html', urls)
        for path in ['/admin/', '/hr/', '/du-an/', '/khach-hang/', '/hidden.html']:
            self.assertNotIn('https://quanconstruction.biz.vn' + path, urls)

    def test_repeat_build_is_identical_and_deleted_cms_page_disappears(self):
        self.run_build()
        first = (self.out / 'sitemap.xml').read_bytes()
        self.run_build()
        self.assertEqual(first, (self.out / 'sitemap.xml').read_bytes())
        self.items.pop()
        self.run_build()
        self.assertFalse((self.out / 'tin-tuc/du-toan.html').exists())

    def test_bad_slug_link_or_duplicate_fails_before_overwriting(self):
        for patch in [{'slug': '../index'}, {'link': '/index.html'}, {'link': 'https://evil.test/a'}, {'slug': 'cu'}]:
            with self.subTest(patch=patch):
                self.items[1].update(patch)
                with self.assertRaises(ValueError):
                    self.run_build()
                self.items[1].pop('link', None)
                self.items[1]['slug'] = 'du-toan'

    def test_short_news_rejects_unsafe_links_before_client_feed(self):
        self.items[1]['body'] = ''
        for link in ['javascript:alert(1)', '//evil.test/', '/\\evil.test', 'data:text/html,test']:
            with self.subTest(link=link):
                self.items[1]['link'] = link
                with self.assertRaises(ValueError):
                    self.run_build()

    def test_noindex_tokens_with_spaces_are_excluded(self):
        self.page('secret.html', '/secret.html')
        path = self.root / 'secret.html'
        path.write_text(path.read_text().replace('</head>', '<meta name="robots" content="follow, noindex"></head>'))
        self.run_build()
        self.assertNotIn('/secret.html', (self.out / 'sitemap.xml').read_text())

    def test_nested_output_cannot_copy_itself(self):
        self.out = self.root / 'previews/site'
        with self.assertRaises(ValueError):
            self.run_build()


if __name__ == '__main__':
    unittest.main()
