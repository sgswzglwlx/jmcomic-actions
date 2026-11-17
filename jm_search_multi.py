# -*- coding: utf-8 -*-
"""多关键词搜索: python3 jm_search_multi.py "kw1,kw2" [每词页数]"""
import sys
from concurrent.futures import ThreadPoolExecutor
from jmcomic import create_option_by_str, JmMagicConstants

kws = [k.strip() for k in sys.argv[1].split(',') if k.strip()]
pages = int(sys.argv[2]) if len(sys.argv) > 2 else 2
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

allrows = {}   # id -> title
hits = {}      # id -> [kws]

for kw in kws:
    n = 0
    for page in range(1, pages + 1):
        try:
            res = list(client.search(kw, page, 0, 'mr', JmMagicConstants.TIME_ALL, '', None))
        except Exception as e:
            print(f'ERR {kw} p{page}: {e!r}'[:150], flush=True); break
        if not res:
            break
        for x in res:
            try:
                aid, title = str(x[0]), str(x[1])
            except Exception:
                aid, title = str(getattr(x, 'id', '')), getattr(x, 'name', '')
            if not aid: continue
            allrows[aid] = title
            hits.setdefault(aid, []).append(kw)
            n += 1
        if len(res) < 20: break
    print(f'KW {kw}: {n} 条', flush=True)

print(f'UNIQUE={len(allrows)}', flush=True)

def det(item):
    aid, title = item
    try:
        a = client.get_album_detail(aid)
        return (aid, a.name, a.page_count, str(a.pub_date), a.author, ' '.join(a.tags[:6]), a.views, a.likes, ','.join(hits.get(aid, [])))
    except Exception as e:
        return (aid, title, '?', '?', '?', '', 0, 0, ','.join(hits.get(aid, [])))

with ThreadPoolExecutor(max_workers=6) as ex:
    data = list(ex.map(det, allrows.items()))
print('=== TABLE ===')
for d in sorted(data, key=lambda x: str(x[3]), reverse=True):
    print('ROW|' + '|'.join(str(v).replace('|', '/') for v in d), flush=True)
