# -*- coding: utf-8 -*-
"""禁漫多关键词批量搜索（在 GitHub Actions 中运行）"""
import sys, json
from jmcomic import create_option_by_str

kws = [k.strip() for k in sys.argv[1].split('|') if k.strip()]
print("KWS:", kws, flush=True)

opt = create_option_by_str("""
client:
  impl: api
  postman:
    type: curl_cffi
    meta_data:
      impersonate: chrome
  retry_times: 3
log: false
""")
client = opt.new_jm_client()

def dump(items, label):
    n = 0
    for a in items:
        if isinstance(a, (list, tuple)):
            aid = a[0] if len(a) > 0 else '?'
            if len(a) > 1 and isinstance(a[1], dict):
                name = a[1].get('name') or a[1].get('title') or ''
                author = a[1].get('author', '')
            else:
                name = a[1] if len(a) > 1 else ''
                author = a[2] if len(a) > 2 else ''
        else:
            aid = getattr(a, 'id', '?')
            name = getattr(a, 'name', '') or getattr(a, 'title', '')
            author = getattr(a, 'author', '')
        print(f"  HIT> {aid} | {str(name)[:50]} | {str(author)[:16]}", flush=True)
        n += 1
        if n >= 12:
            break
    if n == 0:
        print("  (无结果)", flush=True)

for kw in kws:
    print(f"=== Q[{kw}] ===", flush=True)
    got = False
    for fn in ('search', 'search_tag', 'search_album'):
        if not hasattr(client, fn):
            print(f"  [no method {fn}]", flush=True)
            continue
        try:
            items = list(getattr(client, fn)(kw, page=1))
            print(f"  via {fn}: {len(items)} 条", flush=True)
            dump(items, kw)
            got = True
            break
        except Exception as e:
            print(f"  {fn} fail: {repr(e)[:150]}", flush=True)
    if not got:
        print("  FAILED", flush=True)
print("ALL_DONE", flush=True)
