# Người tạo: Quang Mai Phú
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / '_cong-cu/seo_audit.py'


class AuditTests(unittest.TestCase):
    def module(self):
        self.assertTrue(SCRIPT.exists(), 'Chưa có bộ kiểm tra SEO định kỳ')
        spec = importlib.util.spec_from_file_location('seo_audit', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_only_public_same_host_sitemap_urls_are_audited(self):
        m = self.module()
        xml = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(
            '<url><loc>' + x + '</loc></url>' for x in [m.SITE+'/', m.SITE+'/', m.SITE+'/hr/', 'https://evil.test/']) + '</urlset>'
        urls, rejected = m.sitemap_urls(xml)
        self.assertEqual(urls, [m.SITE+'/'])
        self.assertEqual(len(rejected), 2)

    def test_crawlable_page_is_not_claimed_indexed_without_gsc(self):
        m = self.module()
        url = m.SITE+'/test.html'
        result = m.page_result(url, 200, '<link rel="canonical" href="'+url+'">', url)
        self.assertEqual(result['issues'], [])
        self.assertEqual(result['index_status'], 'not_checked')

    def test_noindex_and_canonical_mismatch_are_reported(self):
        m = self.module()
        r = m.page_result(m.SITE+'/a.html', 200, '<meta name="robots" content="follow, noindex"><link rel="canonical" href="'+m.SITE+'/b.html">', m.SITE+'/a.html')
        self.assertIn('noindex', r['issues'])
        self.assertIn('canonical_mismatch', r['issues'])

    def test_http_errors_are_not_gsc_indexing_verdicts(self):
        m = self.module()
        r = m.page_result(m.SITE+'/a.html', 404, '', m.SITE+'/a.html')
        self.assertIn('http_404', r['issues'])
        self.assertEqual(r['index_status'], 'not_checked')

    def test_gsc_pass_excluded_unknown_and_errors_are_distinct(self):
        m = self.module()
        for verdict, expected in [('PASS','indexed'), ('NEUTRAL','not_indexed'), ('FAIL','not_indexed'), ('VERDICT_UNSPECIFIED','unknown')]:
            self.assertEqual(m.index_result({'inspectionResult':{'indexStatusResult':{'verdict':verdict}}})['index_status'], expected)
        self.assertEqual(m.index_result({})['index_status'], 'unknown')

    def test_report_states_missing_credentials_and_escapes_table(self):
        m = self.module()
        report = m.markdown_report([{'url':m.SITE+'/a', 'http_status':200, 'issues':[], 'index_status':'not_checked', 'coverage':'x|y\nnext'}], 'not_connected', [])
        self.assertIn('chưa được kết nối', report)
        self.assertNotIn('|x|y', report)

    def test_credential_token_destination_must_be_google(self):
        m = self.module()
        with self.assertRaises(ValueError):
            m.validate_credentials({'type':'service_account','token_uri':'https://evil.test/token'})

    def test_connection_error_stops_batch_and_preserves_unknown_states(self):
        m = self.module()
        class Session:
            def __init__(self):
                self.calls = 0
                self.closed = False
            def post(self, *args, **kwargs):
                self.calls += 1
                raise TimeoutError()
            def close(self):
                self.closed = True
        session = Session()
        m.gsc_session = lambda raw: session
        rows = [{'url':m.SITE+'/a','index_status':'not_checked'},
                {'url':m.SITE+'/b','index_status':'not_checked'}]
        self.assertEqual(m.inspect_pages(rows,'configured',m.SITE+'/'), 'connection_error')
        self.assertEqual(session.calls, 1)
        self.assertTrue(session.closed)
        self.assertEqual(rows[1]['index_status'],'not_checked')


if __name__ == '__main__':
    unittest.main()
