# -*- coding: utf-8 -*-
import re, sys, json
from curl_cffi import requests as creq
pid = sys.argv[1]
s = creq.Session(impersonate='chrome')
hdrs = {'Referer': 'https://www.pixiv.net/', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,'}
for url in [f'https://www.pixiv.net/artworks/{pid}',
            f'https://www.pixiv.net/ajax/illust/{pid}']:
    try:
        r = s.get(url, headers=hdrs, timeout=40)
        print(f'--- {url} HTTP {r.status_code} {len(r.text)}B')
        t = r.text
        for pat in [r'<meta property="og:title" content="([^"]*)"',
                    r'<meta name="description" content="([^"]*)"',
                    r'<title>([^<]*)</title>',
                    r'"illustTitle":"([^"]*)"',
                    r'"userName":"([^"]*)"',
                    r'"userAccount":"([^"]*)"',
                    r'"pageCount":(\d+)',
                    r'"tags":\[([^\]]{0,300})\]']:
            m = re.findall(pat, t)
            if m:
                print('   ', pat[:32], '->', str(m[:3])[:300])
    except Exception as e:
        print(f'--- {url} ERR {repr(e)[:120]}')
