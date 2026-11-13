# -*- coding: utf-8 -*-
"""抓取多个专辑详情：id1,id2,... 输出标题/页数/标签/简介"""
import sys
from jmcomic import create_option_by_str

ids = [x.strip() for x in sys.argv[1].split(',') if x.strip()]
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
for aid in ids:
    print(f"=== ALBUM {aid} ===", flush=True)
    try:
        a = client.get_album_detail(aid)
        d = a.get_properties_dict() if hasattr(a, 'get_properties_dict') else {}
        print(f"NAME> {a.name}", flush=True)
        print(f"PAGES> {a.page_count} 章", flush=True)
        print(f"AUTHOR> {a.author}", flush=True)
        tags = d.get('tags') or getattr(a, 'tags', None)
        if isinstance(tags, list):
            tt = []
            for t in tags:
                tt.append(str(t.get('tag_name', t)) if isinstance(t, dict) else str(t))
            print(f"TAGS> {', '.join(tt)}", flush=True)
        desc = d.get('description') or getattr(a, 'description', '') or ''
        desc = ' '.join(str(desc).split())
        print(f"DESC> {desc[:400]}", flush=True)
    except Exception as e:
        print(f"FAIL> {aid}: {repr(e)[:160]}", flush=True)
print("ALL_DONE", flush=True)
