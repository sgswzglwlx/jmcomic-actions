# -*- coding: utf-8 -*-
"""禁漫 raw API 探测 v3"""
import json, sys
from curl_cffi import requests as creq
from jmcomic import create_option_by_str

TARGET = sys.argv[1] if len(sys.argv) > 1 else "3927698"
opt = create_option_by_str("""
client:
  impl: api
  postman:
    type: curl_cffi
    meta_data:
      impersonate: chrome
  retry_times: 2
log: false
""")
client = opt.new_jm_client()

print("=== A) 最新本子（categories_filter）===")
try:
    res = client.categories_filter(page=1)
    ids = []
    for x in res[:40]:
        print("  ", str(x)[:120])
        try: ids.append(int(x[0]))
        except Exception: pass
    if ids:
        print(f"  -> 最新 id 范围: min={min(ids)} max={max(ids)}")
except Exception as e:
    print("  FAIL:", repr(e)[:200])

print("=== B) 域名/设置 ===")
try:
    opts = client.get_domain_list() if hasattr(client, 'get_domain_list') else None
    print("  domains:", opts)
except Exception as e:
    print("  domain err:", repr(e)[:120])

print("=== C) raw API 探测 ===")
domains = ['https://18comic.vip', 'https://18comic.org']
s = creq.Session(impersonate='chrome')
hdrs = {'Referer': 'https://18comic.vip/', 'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/plain, */*'}
for d in domains:
    for path, tag in [(f'/api/album?id={TARGET}', 'album'),
                      (f'/api/chapter?id={TARGET}', 'chapter'),
                      (f'/api/album?id={TARGET}&page=1', 'album-page')]:
        try:
            r = s.get(d + path, headers=hdrs, timeout=30)
            body = r.text[:300].replace('\n', ' ')
            print(f"  {d}{path} [HTTP {r.status_code}] {body}")
        except Exception as e:
            print(f"  {d}{path} err: {repr(e)[:120]}")

print("=== D) 搜索该数字 ===")
try:
    res = client.search_album(TARGET, page=1)
    print("  hits:", len(res))
    for a in res[:5]:
        print("   ", getattr(a, 'id', '?'), getattr(a, 'name', '?'), getattr(a, 'author', ''))
except Exception as e:
    print("  FAIL:", repr(e)[:200])
