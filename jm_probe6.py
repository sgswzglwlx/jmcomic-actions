# -*- coding: utf-8 -*-
"""跨站同号交叉验证"""
import re, sys
from curl_cffi import requests as creq

T = sys.argv[1] if len(sys.argv) > 1 else "3927698"
s = creq.Session(impersonate='chrome')

tests = [
    ('nhentai   ', f'https://nhentai.net/api/gallery/{T}'),
    ('hitomi    ', f'https://hitomi.la/galleries/{T}.html'),
    ('e-hentai  ', f'https://e-hentai.org/g/{T}/'),
    ('18comicAPI', f'https://18comic.vip/api/album?id={T}'),
    ('jmcomic.me', f'https://jmcomic.me/api/album?id={T}'),
    ('18comic.ink', f'https://18comic.ink/api/album?id={T}'),
    ('18comic.org', f'https://18comic.org/api/album?id={T}'),
]
for name, url in tests:
    try:
        host = url.split('/')[2]
        r = s.get(url, timeout=40, allow_redirects=True,
                  headers={'Referer': f'https://{host}/', 'X-Requested-With': 'XMLHttpRequest',
                           'Accept': 'application/json, text/html, */*'})
        body = r.text
        title = re.findall(r'<title>(.*?)</title>', body)
        info = ''
        if 'JSON' in r.headers.get('Content-Type', '').upper() or body.strip().startswith('{'):
            info = body[:220].replace('\n', ' ')
        else:
            info = f"title={title[:1]} " + re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body))[:160]
        print(f"  {name}: HTTP {r.status_code} | {len(body)}B | final={r.url[:110]}")
        print(f"      {info}")
    except Exception as e:
        print(f"  {name}: ERR {repr(e)[:140]}")
