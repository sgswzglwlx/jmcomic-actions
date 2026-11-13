# -*- coding: utf-8 -*-
"""列出作者全部作品（含分页）"""
import sys
from jmcomic import create_option_by_str

kw = (sys.argv[1] if len(sys.argv) > 1 else 'JiongBaotai').strip()
print(f"AUTHOR_KW: {kw}", flush=True)

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

seen = {}
def add(items, src):
    for a in items:
        try:
            if isinstance(a, (list, tuple)):
                aid = str(a[0])
                if len(a) > 1 and isinstance(a[1], dict):
                    name = a[1].get('name') or a[1].get('title') or ''
                    author = a[1].get('author', '')
                else:
                    name = a[1] if len(a) > 1 else ''
                    author = a[2] if len(a) > 2 else ''
            else:
                aid = str(getattr(a, 'id', '?'))
                name = getattr(a, 'name', '') or ''
                author = getattr(a, 'author', '')
        except Exception:
            continue
        if aid not in seen:
            seen[aid] = (str(name)[:70], str(author)[:20], src)
    print(f"  [{src}] 累计 {len(seen)}", flush=True)

# 1) search_author 分页
for p in range(1, 6):
    try:
        r = list(client.search_author(kw, page=p))
        if not r: break
        add(r, f'author_p{p}')
    except Exception as e:
        print(f"  author_p{p} fail: {repr(e)[:120]}", flush=True); break

# 2) 关键词搜索分页
for p in range(1, 5):
    try:
        r = list(client.search(kw, p, '', 'mr', '', '', ''))
        if not r: break
        add(r, f'search_p{p}')
    except Exception as e:
        print(f"  search_p{p} fail: {repr(e)[:120]}", flush=True); break

print(f"TOTAL: {len(seen)}", flush=True)
for aid, (name, author, src) in sorted(seen.items(), key=lambda x: -int(x[0])):
    print(f"LIST> {aid} | {name} | {author} | {src}", flush=True)
print("ALL_DONE", flush=True)
