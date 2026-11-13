#!/usr/bin/env python3
"""Người tạo: Quang Mai Phú. Đọc hiệu suất Search Console, chỉ xuất báo cáo mã hóa."""
from datetime import date,datetime,timedelta
from zoneinfo import ZoneInfo
import base64
import json
import os
from pathlib import Path
from time import sleep
from urllib.parse import quote

SITE='https://quanconstruction.biz.vn/'
AAD=b'Quan Construction Search Console report v1'


def windows(end):
    return {'recent_start':str(end-timedelta(days=6)),'recent_end':str(end),
            'previous_start':str(end-timedelta(days=13)),'previous_end':str(end-timedelta(days=7))}


def compare_queries(recent,previous):
    old={r['keys'][0]:r for r in previous}
    new={r['keys'][0]:r for r in recent}
    output=[]
    for query in sorted(set(old)|set(new)):
        a,b=old.get(query,{}),new.get(query,{})
        before,after=a.get('impressions',0),b.get('impressions',0)
        output.append({'query':query,'previous':a,'recent':b,'impressions_delta':after-before,
                       'impressions_change_pct':100*(after-before)/before if before else None})
    return sorted(output,key=lambda row:(row['impressions_delta'],row['recent'].get('impressions',0)),reverse=True)


def encrypt_report(report,public_pem):
    from cryptography.hazmat.primitives import serialization,hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key=AESGCM.generate_key(bit_length=256)
    nonce=os.urandom(12)
    ciphertext=AESGCM(key).encrypt(nonce,json.dumps(report,ensure_ascii=False).encode(),AAD)
    public=serialization.load_pem_public_key(public_pem)
    wrapped=public.encrypt(key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    enc=lambda value:base64.b64encode(value).decode()
    return json.dumps({'version':1,'key':enc(wrapped),'nonce':enc(nonce),'ciphertext':enc(ciphertext)})


def main():
    from seo_audit import gsc_session
    raw=os.environ.get('GSC_CREDENTIALS_JSON','')
    if not raw:raise SystemExit('Chưa cấu hình thông tin xác thực Search Console.')
    session=gsc_session(raw)
    endpoint='https://www.googleapis.com/webmasters/v3/sites/'+quote(SITE,safe='')+'/searchAnalytics/query'
    def query(start,end,dimension):
        body={'startDate':start,'endDate':end,'dimensions':[dimension],'type':'web','dataState':'final','rowLimit':25000}
        for attempt in range(3):
            response=None
            try:response=session.post(endpoint,json=body,timeout=40)
            except Exception:pass
            if response is not None and response.status_code==200:return response.json().get('rows',[])
            if response is not None and response.status_code in (401,403,429):
                raise RuntimeError('Search Analytics không truy cập được, HTTP '+str(response.status_code))
            if attempt<2:sleep(2**(attempt+1))
        raise RuntimeError('Search Analytics chưa trả dữ liệu sau 3 lần thử.')
    try:
        yesterday=datetime.now(ZoneInfo('America/Los_Angeles')).date()-timedelta(days=1)
        daily=query(str(yesterday-timedelta(days=34)),str(yesterday),'date')
        if not daily:raise RuntimeError('Chưa có dữ liệu hiệu suất đã hoàn tất trong 35 ngày.')
        latest=date.fromisoformat(max(row['keys'][0] for row in daily))
        period=windows(latest)
        current=query(period['recent_start'],period['recent_end'],'query')
        previous=query(period['previous_start'],period['previous_end'],'query')
        pages=query(period['recent_start'],period['recent_end'],'page')
        report={'author':'Quang Mai Phú','site':SITE,'data_state':'final','report_timezone':'America/Los_Angeles',
                'period':period,'daily':daily,'queries_recent':current,'queries_previous':previous,
                'query_comparison':compare_queries(current,previous),'pages_recent':pages,
                'note':'Truy vấn ẩn danh có thể bị Google lược bỏ; không xem truy vấn vắng là chắc chắn không có tìm kiếm. Đây là xu hướng hiển thị website, không phải Google Trends.'}
        output=Path('_search_report');output.mkdir(exist_ok=True)
        (output/'performance.enc').write_text(encrypt_report(report,Path('_cong-cu/search-report-public.pem').read_bytes()))
        print('Đã đọc hiệu suất và lưu báo cáo mã hóa. Không công khai truy vấn hoặc dữ liệu hiệu suất trong nhật ký.')
    finally:session.close()


if __name__=='__main__':main()
