# -*- coding: utf-8 -*-
"""禁漫 ID 空间探测 v4"""
import sys
from jmcomic import create_option_by_str, JmMagicConstants

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

print("=== A) 最新本子（判断 id 量级）===")
try:
    page = client.categories_filter(1, JmMagicConstants.TIME_ALL, '', 'mv')
    ids = []
    n = 0
    for a in page:
        n += 1
        try:
            aid = int(a[0]); name = str(a[1])[:45]; au = str(a[2])[:18]
        except Exception:
            aid = int(getattr(a, 'id', 0)); name = str(getattr(a, 'name', ''))[:45]; au = str(getattr(a, 'author', ''))[:18]
        ids.append(aid)
        if n <= 12:
            print(f"   {aid} | {name} | {au}")
    print(f"   -> 共 {n} 条, id: min={min(ids)} max={max(ids)}")
except Exception as e:
    print("   FAIL:", repr(e)[:250])

print("=== B) id 空间抽样探测 ===")
for tid in [1500000, 2000000, 2500000, 3000000, 3500000, 3900000, 3927698]:
    try:
        a = client.get_album_detail(str(tid))
        print(f"   album {tid} -> OK: {a.name[:50]} / {a.author[:20]}")
    except Exception as e:
        print(f"   album {tid} -> 不存在 ({str(e)[:45]})")
