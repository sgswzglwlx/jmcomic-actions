# -*- coding: utf-8 -*-
"""作者作品全列表: python3 jm_author.py <作者名>"""
import sys
from concurrent.futures import ThreadPoolExecutor
from jmcomic import create_option_by_str

name = sys.argv[1] if len(sys.argv) > 1 else 'Hessen_52hz'
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

rows = []
for page in range(1, 6):
    try:
        res = client.search_author(name, page=page)
    except Exception as e:
        print(f'PAGE {page} ERR {e!r}'[:200]); break
    res = list(res)
    print(f'PAGE {page}: {len(res)} 条', flush=True)
    if not res: break
    for x in res:
        try:
            aid = str(x[0]); title = str(x[1])
        except Exception:
            aid = str(getattr(x, 'id', '')); title = getattr(x, 'name', '')
        rows.append((aid, title))
    if len(res) < 30: break

print(f'TOTAL_ROWS={len(rows)}', flush=True)

def detail(r):
    aid, title = r
    try:
        a = client.get_album_detail(aid)
        return (aid, a.name, a.page_count, str(a.pub_date), ' '.join(a.tags[:5]))
    except Exception as e:
        return (aid, title, '?', '?', f'ERR {e!r}'[:40])

with ThreadPoolExecutor(max_workers=6) as ex:
    data = list(ex.map(detail, rows))

print('=== TABLE ===')
for d in sorted(data, key=lambda x: str(x[3]), reverse=True):
    print('ROW|' + '|'.join(str(v).replace('|', '/') for v in d))
