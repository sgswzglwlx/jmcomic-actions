# -*- coding: utf-8 -*-
import sys
from jmcomic import create_option_by_str, JmMagicConstants

TARGET = sys.argv[1] if len(sys.argv) > 1 else "3927698"
opt = create_option_by_str("""
client:
  impl: api
  postman:
    type: curl_cffi
    meta_data:
      impersonate: chrome
  retry_times: 1
log: false
""")
client = opt.new_jm_client()

print("=== A) 以车号搜索 ===")
for mt in (0, 1):
    try:
        r = client.search(TARGET, 1, mt, 'mv', JmMagicConstants.TIME_ALL, '', None)
        items = list(r)
        print(f"  main_tag={mt}: {len(items)} 条")
        for x in items[:5]:
            print("    ", str(x)[:200])
    except Exception as e:
        print(f"  main_tag={mt} FAIL:", repr(e)[:200])

print("=== B) raw /album & /chapter ===")
for api, key in [('/album', 'id'), ('/chapter', 'id')]:
    try:
        resp = client.req_api(client.append_params_to_url(api, {key: TARGET}))
        d = resp.model_data
        print(f"  {api}?{key}={TARGET} -> {str(d)[:400]}")
    except Exception as e:
        print(f"  {api} FAIL:", repr(e)[:200])

print("=== C) 最新本子原始项（判断 id 上限）===")
try:
    p = client.categories_filter(1, JmMagicConstants.TIME_ALL, '', 'mv')
    items = list(p)
    print("  len:", len(items))
    for x in items[:6]:
        print("   raw:", type(x).__name__, str(x)[:260])
except Exception as e:
    print("  FAIL:", repr(e)[:250])

print("=== D) 基线复核 ===")
for tid in ['1464279', '1460220']:
    try:
        a = client.get_album_detail(tid)
        print(f"  {tid} OK: {a.name[:40]} / {a.author[:16]}")
    except Exception as e:
        print(f"  {tid} FAIL: {str(e)[:80]}")
