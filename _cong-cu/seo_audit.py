#!/usr/bin/env python3
"""Người tạo: Quang Mai Phú. Kiểm tra SEO công khai và đọc trạng thái Search Console."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from time import sleep
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener
import xml.etree.ElementTree as ET

SITE = 'https://quanconstruction.biz.vn'
API = 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect'
INTERNAL = {'hr', 'admin', 'du-an', 'khach-hang', '_cong-cu'}
PRIORITY = [SITE+'/', SITE+'/xay-nha-tron-goi.html', SITE+'/du-toan-boc-khoi-luong.html']


def allowed_url(url):
    p = urlsplit(url)
    return (p.scheme == 'https' and p.netloc == urlsplit(SITE).netloc and not p.query and
            not p.fragment and p.path.lstrip('/').split('/')[0] not in INTERNAL)


class SameSiteRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise ValueError('Redirect ra ngoài website công khai')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    if not allowed_url(url):
        raise ValueError('URL ngoài phạm vi kiểm tra')
    request = Request(url, headers={'User-Agent': 'QuanConstruction-SEO-Audit/1.0'})
    try:
        with build_opener(SameSiteRedirect()).open(request, timeout=20) as response:
            body = response.read(4_000_001)
            if len(body) > 4_000_000:
                raise ValueError('Nội dung vượt giới hạn 4 MB')
            return response.status, body.decode('utf-8', errors='replace'), response.url, response.headers
    except HTTPError as error:
        return error.code, '', error.url, error.headers


def sitemap_urls(xml):
    root = ET.fromstring(xml)
    if root.tag.split('}')[-1] != 'urlset':
        raise ValueError('Cần sitemap urlset, không phải sitemap index')
    urls, rejected = [], []
    for element in root.findall('.//{*}loc'):
        url = (element.text or '').strip()
        if not allowed_url(url):
            rejected.append(url)
        elif url not in urls:
            urls.append(url)
    return urls, rejected


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.noindex, self.canonical = False, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and a.get('name','').lower() in ('robots','googlebot'):
            self.noindex |= 'noindex' in re.split(r'[\s,]+', a.get('content','').lower())
        if tag == 'link' and 'canonical' in a.get('rel','').split():
            self.canonical = a.get('href')


def page_result(url, status, body, final_url, headers=None):
    issues = []
    result = {'url':url, 'http_status':status, 'final_url':final_url, 'issues':issues,
              'index_status':'not_checked', 'coverage':''}
    if status != 200:
        issues.append('http_' + str(status))
        return result
    if final_url != url:
        issues.append('redirected')
    meta = Metadata()
    meta.feed(body)
    if meta.noindex or 'noindex' in (headers or {}).get('X-Robots-Tag','').lower():
        issues.append('noindex')
    if not meta.canonical:
        issues.append('missing_canonical')
    elif meta.canonical != url:
        issues.append('canonical_mismatch')
    result['canonical'] = meta.canonical
    return result


def check_page(url):
    try:
        return page_result(url, *fetch(url))
    except Exception:
        # Do not leak request internals or credentials into the public report.
        return {'url':url, 'http_status':None, 'issues':['fetch_error'],
                'index_status':'not_checked', 'coverage':''}


def index_result(data):
    status = data.get('inspectionResult',{}).get('indexStatusResult',{})
    verdict = status.get('verdict','')
    return {'index_status':{'PASS':'indexed','FAIL':'not_indexed','NEUTRAL':'not_indexed'}.get(verdict,'unknown'),
            'coverage':status.get('coverageState',''), 'google_canonical':status.get('googleCanonical',''),
            'last_crawl':status.get('lastCrawlTime','')}


def validate_credentials(info):
    if info.get('type') != 'service_account' or info.get('token_uri') != 'https://oauth2.googleapis.com/token':
        raise ValueError('Chỉ nhận Google service account với token_uri chính thức')
    if not str(info.get('client_email','')).endswith('.iam.gserviceaccount.com'):
        raise ValueError('Service account email không hợp lệ')


def gsc_session(raw):
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    info = json.loads(raw)
    validate_credentials(info)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
    return AuthorizedSession(creds, refresh_timeout=30)


def inspect_pages(rows, raw, property_url):
    if not raw:
        return 'not_connected'
    try:
        session = gsc_session(raw)
    except Exception:
        return 'authentication_error'
    state = 'connected'
    try:
        for position, row in enumerate(rows, 1):
            print(f'Google URL Inspection {position}/{len(rows)}', flush=True)
            response = None
            # Người chỉnh sửa: Quang Mai Phú – thử lại lỗi mạng/5xx tạm thời.
            # URL Inspection chỉ đọc trạng thái nên thử lại không thay đổi Google index.
            for attempt in range(3):
                try:
                    response = session.post(API, json={'inspectionUrl':row['url'], 'siteUrl':property_url,
                                                     'languageCode':'vi-VN'}, timeout=30)
                except Exception:
                    response = None
                if response is not None and response.status_code < 500 and response.status_code != 408:
                    break
                if attempt < 2:
                    print(f'Google API tạm gián đoạn, thử lại {attempt + 2}/3.', flush=True)
                    sleep(2 ** (attempt + 1))
            if response is None:
                row['index_status'] = 'api_error'
                state = 'connection_error'
                break
            try:
                if response.status_code in (401,403,429):
                    state = {401:'authentication_error',403:'permission_error',429:'quota_exceeded'}[response.status_code]
                    break
                if response.status_code != 200:
                    row['index_status'] = 'api_error'
                    if response.status_code >= 500 or response.status_code == 408:
                        state = 'service_error'
                        break
                else:
                    row.update(index_result(response.json()))
            except Exception:
                row['index_status'] = 'api_error'
                state = 'connection_error'
                break
    finally:
        session.close()
    return state


def markdown_report(rows, gsc_state, rejected, total=None):
    labels = {'indexed':'Đã lập chỉ mục', 'not_indexed':'Chưa lập chỉ mục / bị loại',
              'not_checked':'Chưa kiểm tra', 'unknown':'Chưa rõ', 'api_error':'Lỗi đọc API'}
    counts = {key:sum(x['index_status']==key for x in rows) for key in labels}
    cell = lambda value: str(value or '').replace('|','\\|').replace('\n',' ')
    lines = ['# Báo cáo kiểm tra SEO', 'Người tạo: Quang Mai Phú', '',
             f'- Kiểm tra {len(rows)}/{total or len(rows)} URL trong sitemap.',
             '- Đây là kiểm tra kỹ thuật và trạng thái; không gửi yêu cầu lập chỉ mục, không đo thứ hạng.',
             '- Search Console chưa được kết nối; CHƯA xác định trang nào đã/chưa được Google lập chỉ mục.'
             if gsc_state=='not_connected' else '- Trạng thái kết nối Search Console: '+gsc_state,
             '- Thống kê: '+', '.join(f'{labels[k]}: {v}' for k,v in counts.items()),
             f'- URL bị loại khỏi phạm vi sitemap: {len(rejected)}', '',
             '| URL | HTTP | Vấn đề kỹ thuật | Trạng thái Google | Chi tiết Google |',
             '|---|---:|---|---|---|']
    for row in rows:
        lines.append('| '+ ' | '.join(map(cell,[row['url'],row.get('http_status'),
                     ', '.join(row['issues']) or 'Không phát hiện trong phạm vi kiểm tra',
                     labels[row['index_status']],row.get('coverage','')]))+' |')
    lines += ['', 'Chưa lập chỉ mục không tự động có nghĩa là lỗi; cần đọc lý do Google cung cấp.',
              'Phạm vi kỹ thuật: HTTP, chuyển hướng, canonical, noindex. Không giả lập Googlebot hay tự yêu cầu lập chỉ mục.']
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=200)
    parser.add_argument('--output',default='_seo_reports')
    args = parser.parse_args()
    if not 1 <= args.limit <= 200:
        parser.error('limit phải từ 1 đến 200')
    status, xml, _, _ = fetch(SITE+'/sitemap.xml')
    if status != 200:
        raise RuntimeError('Không đọc được sitemap công khai')
    urls, rejected = sitemap_urls(xml)
    # Keep both business pages in every limited inspection batch.
    urls.sort(key=lambda u:(PRIORITY.index(u) if u in PRIORITY else len(PRIORITY),u))
    with ThreadPoolExecutor(max_workers=4) as executor:
        rows = list(executor.map(check_page, urls[:args.limit]))
    gsc = inspect_pages(rows,os.environ.get('GSC_CREDENTIALS_JSON',''),os.environ.get('GSC_PROPERTY',SITE+'/'))
    report = markdown_report(rows,gsc,rejected,len(urls))
    output = Path(args.output)
    output.mkdir(parents=True,exist_ok=True)
    (output/'seo-report.md').write_text(report,encoding='utf-8')
    (output/'seo-report.json').write_text(json.dumps({'author':'Quang Mai Phú',
        'checked_at':datetime.now(timezone.utc).isoformat(),'gsc_connection':gsc,'total_urls':len(urls),
        'rejected_urls':rejected,'pages':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as stream:
            stream.write(report)
    print(f'Đã kiểm tra {len(rows)}/{len(urls)} URL. Search Console: {gsc}. Báo cáo: {output}', flush=True)
    for status in ('indexed', 'not_indexed', 'unknown', 'not_checked', 'api_error'):
        print(f'Index status {status}: {sum(row["index_status"] == status for row in rows)}', flush=True)
    if gsc not in ('connected','not_connected'):
        raise SystemExit('Không đọc đủ trạng thái Google; xem phần kết nối trong báo cáo.')
    if rejected or any(row['issues'] for row in rows):
        raise SystemExit('Có vấn đề kỹ thuật cần xem trong báo cáo.')


if __name__ == '__main__':
    main()
