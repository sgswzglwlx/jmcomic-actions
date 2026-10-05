# -*- coding: utf-8 -*-
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
for order in ['mr', 'mv_t']:
    print(f"=== 排序 {order} ===")
    try:
        page = client.categories_filter(1, JmMagicConstants.TIME_ALL, '', order)
        items = list(page)
        ids = []
        for x in items[:20]:
            try:
                ids.append(int(x[0])); print(f"   {x[0]} | {str(x[1])[:52]}")
            except Exception:
                pass
        if ids:
            print(f"   -> 该榜 id: min={min(ids)} max={max(ids)}")
    except Exception as e:
        print("   FAIL:", repr(e)[:200])
