# -*- coding: utf-8 -*-
"""禁漫 ID 探测：先当 album，再当 photo，输出全部可得信息"""
import sys
from jmcomic import create_option_by_str

aid = sys.argv[1] if len(sys.argv) > 1 else "3927698"
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

FIELDS = ['album_id','photo_id','name','author','tags','alias_cn','alias_en','page_count',
          'pub_date','update_date','liked','views','likes','comment_count','works','actors',
          'series','description','scramble_id','is_scrambled','from_album','image_url','title']

def dump(o, label):
    print(f"--- {label} ---")
    for k in FIELDS:
        try:
            v = getattr(o, k, None)
            if v not in (None, '', [], {}):
                print(f"{k}: {str(v)[:300]}")
        except Exception as e:
            print(f"{k}: <err {e}>")
    props = {}
    try:
        props = o.get_properties_dict()
    except Exception:
        pass
    for k, v in props.items():
        if k not in FIELDS and v:
            print(f"  *{k}: {str(v)[:200]}")

print(f"=== 探测 ID: {aid} ===")
ok = False
try:
    a = client.get_album_detail(aid)
    print(">>> ALBUM 命中")
    dump(a, "ALBUM")
    eps = getattr(a, 'episode_list', [])
    print(f"episode_count: {len(eps)}")
    for ep in eps[:60]:
        print(f"  ep {getattr(ep,'photo_id','?')} | {getattr(ep,'title','')} | {getattr(ep,'page_count','?')}p")
    ok = True
except Exception as e:
    print("ALBUM FAIL:", repr(e)[:300])

try:
    p = client.get_photo_detail(aid, fetch_album=True)
    print(">>> PHOTO 命中")
    dump(p, "PHOTO")
    try:
        print(">>> 所属专辑:")
        dump(p.from_album, "FROM_ALBUM")
    except Exception as e:
        print("from_album err", e)
    ok = True
except Exception as e:
    print("PHOTO FAIL:", repr(e)[:300])

print("RESULT:", "FOUND" if ok else "NOT_FOUND")
