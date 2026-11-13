# Người tạo: Quang Mai Phú
import importlib.util
from pathlib import Path
from datetime import date
import unittest


class PerformanceTests(unittest.TestCase):
    def module(self):
        p=Path(__file__).resolve().parents[1]/'_cong-cu/search_performance.py'
        self.assertTrue(p.exists())
        spec=importlib.util.spec_from_file_location('performance',p)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        return m

    def test_windows_have_seven_days_without_overlap(self):
        m=self.module()
        self.assertEqual(m.windows(date(2026,11,10)), {'recent_start':'2026-11-04','recent_end':'2026-11-10','previous_start':'2026-10-28','previous_end':'2026-11-03'})

    def test_keyword_comparison_retains_small_counts_without_invented_percentages(self):
        m=self.module()
        recent=[{'keys':['xây nhà'],'impressions':3,'clicks':1,'position':12}]
        previous=[]
        result=m.compare_queries(recent,previous)[0]
        self.assertEqual(result['impressions_delta'],3)
        self.assertIsNone(result['impressions_change_pct'])

    def test_report_is_authenticated_encrypted_bytes_not_plaintext(self):
        m=self.module()
        from cryptography.hazmat.primitives.asymmetric import rsa,padding
        from cryptography.hazmat.primitives import serialization,hashes
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        import base64,json
        key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        pub=key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
        payload=m.encrypt_report({'query':'private query'},pub)
        self.assertNotIn('private query',payload)
        envelope=json.loads(payload)
        secret=key.decrypt(base64.b64decode(envelope['key']),padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        plaintext=AESGCM(secret).decrypt(base64.b64decode(envelope['nonce']),base64.b64decode(envelope['ciphertext']),m.AAD)
        self.assertEqual(json.loads(plaintext),{'query':'private query'})
