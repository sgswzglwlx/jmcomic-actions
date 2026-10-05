# -*- coding: utf-8 -*-
"""hitomi 命中确认"""
import json, re, sys
from curl_cffi import requests as creq

T = sys.argv[1] if len(sys.argv) > 1 else "3927698"
s = creq.Session(impersonate='chrome')

def probe(url, tag):
    try:
        r = s.get(url, timeout=40, headers={'Referer': 'https://hitomi.la/'})
        body = r.text
        return r.status_code, len(body), body
    except Exception as e:
        print(f"  {tag}: ERR {repr(e)[:120]}")
        return None, None, None

print("=== 1) 存在性对照（页面）===")
for gid in [T, '999999999', '1']:
    code, ln, body = probe(f'https://hitomi.la/galleries/{gid}.html', f'html/{gid}')
    if code is None: continue
    t = re.findall(r'<title>(.*?)</title>', body)
    print(f"  galleries/{gid}.html -> HTTP {code} | {ln}B | title={t[:1]}")

print("=== 2) 官方数据端点 ===")
for gid in [T, '999999999']:
    for ep in [f'https://ltn.hitomi.la/galleries/{gid}.js',
               f'https://ltn.gold-usergeneratedcontent.net/galleries/{gid}.js',
               f'https://ltn.hitomi.la/galleryblock/{gid}.html']:
        try:
            r = s.get(ep, timeout=35, headers={'Referer': 'https://hitomi.la/'})
            txt = r.text
            print(f"  {ep.replace('https://','')} -> HTTP {r.status_code} | {len(txt)}B")
            if r.status_code == 200 and len(txt) > 20:
                print("      ", re.sub(r'\s+', ' ', txt)[:500])
        except Exception as e:
            print(f"  {ep} ERR {repr(e)[:100]}")

print("=== 3) 页面内嵌数据解析 ===")
code, ln, body = probe(f'https://hitomi.la/galleries/{T}.html', 'html')
if body:
    for pat in [r'var galleryinfo\s*=\s*(\{.*?\});', r'galleryinfo\s*=\s*(\{.*?\})',
                r'"galleryid"\s*:\s*(\d+)', r'data-galleryid="(\d+)"']:
        m = re.findall(pat, body, re.S)
        if m:
            print(f"  pattern {pat[:30]} -> {str(m[:1])[:400]}")
    # 尝试从 script src 找
    srcs = re.findall(r'<script[^>]+src="([^"]+)"', body)
    print("  scripts:", srcs[:8])
