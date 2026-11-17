# -*- coding: utf-8 -*-
"""站内搜索: python3 jm_search.py "关键词" [页数]"""
import sys
from concurrent.futures import ThreadPoolExecutor
from jmcomic import create_option_by_str, JmMagicConstants

kw = sys.argv[1]
pages = int(sys.argv[2]) if len(sys.argv) > 2 else 3
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

rows, seen = [], set()
for page in range(1, pages + 1):
    res = None
    try:
        res = list(client.search(kw, page, 0, 'mr', JmMagicConstants.TIME_ALL, '', None))
    except Exception as e:
        print(f'SEARCH_ERR {page}: {e!r}'[:180], flush=True)
        try:
            res = list(client.search_tag(kw, page=page))
        except Exception as e2:
            print(f'TAG_ERR {page}: {e2!r}'[:180], flush=True)
            break
    print(f'PAGE {page}: {len(res)}', flush=True)
    if not res:
        break
    for x in res:
        try:
            aid, title = str(x[0]), str(x[1])
        except Exception:
            aid, title = str(getattr(x, 'id', '')), getattr(x, 'name', '')
        if aid and aid not in seen:
            seen.add(aid); rows.append((aid, title))
    if len(res) < 20:
        break

print(f'TOTAL={len(rows)}', flush=True)

def det(r):
    aid, title = r
    try:
        a = client.get_album_detail(aid)
        return (aid, a.name, a.page_count, str(a.pub_date), a.author, ' '.join(a.tags[:5]), a.views, a.likes)
    except Exception as e:
        return (aid, title, '?', '?', '?', '', 0, 0)

with ThreadPoolExecutor(max_workers=6) as ex:
    data = list(ex.map(det, rows))
print('=== TABLE ===')
for d in sorted(data, key=lambda x: str(x[3]), reverse=True):
    print('ROW|' + '|'.join(str(v).replace('|', '/') for v in d), flush=True)
