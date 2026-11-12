# Người tạo: Quang Mai Phú
import importlib.util
import unittest
from pathlib import Path


class ArticleFeedTests(unittest.TestCase):
    def module(self):
        path=Path(__file__).resolve().parents[1]/'_cong-cu/tao-bai-viet.py'
        spec=importlib.util.spec_from_file_location('article_generator',path)
        m=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    def test_generated_feed_preserves_cms_articles_and_external_legacy_links(self):
        m=self.module()
        self.assertTrue(hasattr(m,'merge_news_items'),'Thiếu cơ chế bảo toàn bài CMS')
        old=[{'title':'Bài CMS','body':'Nội dung thật','link':'/tin-tuc/cms.html'},
             {'title':'Bài cũ','link':'/tin-tuc/generated.html','body':''}]
        generated=[{'title':'Bài mới','link':'/tin-tuc/generated.html','body':''}]
        merged=m.merge_news_items(old,generated,{'/tin-tuc/generated.html','/tin-tuc/future.html'})
        self.assertIn(old[0],merged)
        self.assertNotIn(old[1],merged)
        self.assertIn(generated[0],merged)

    def test_cms_override_same_generated_url_is_not_overwritten(self):
        m=self.module()
        self.assertTrue(hasattr(m,'merge_news_items'))
        cms={'title':'Nội dung đã chỉnh','link':'/tin-tuc/one.html','body':'Nội dung CMS'}
        merged=m.merge_news_items([cms],[{'link':'/tin-tuc/one.html','body':''}],{'/tin-tuc/one.html'})
        self.assertEqual(merged,[cms])
