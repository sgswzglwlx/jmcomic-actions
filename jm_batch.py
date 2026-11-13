# -*- coding: utf-8 -*-
"""批量下载 jm 本子：python3 jm_batch.py "id1,id2,id3" """
import sys
from jmcomic import create_option_by_str, download_album

ids = [x.strip() for x in sys.argv[1].split(',') if x.strip()]
print('IDS:', ids, flush=True)

opt = create_option_by_str("""
client:
  impl: api
  postman:
    type: curl_cffi
    meta_data:
      impersonate: chrome
  retry_times: 5
dir_rule:
  base_dir: /tmp/jm
  rule: Bd_Aauthor_Atitle_Pindex
download:
  cache: true
  image:
    decode: true
  threading:
    image: 20
    photo: 4
log: true
""")

for aid in ids:
    print(f'=== START {aid} ===', flush=True)
    try:
        download_album(aid, option=opt)
        print(f'=== OK {aid} ===', flush=True)
    except Exception as e:
        print(f'=== FAIL {aid}: {e!r} ===', flush=True)

import os
n = sum(len(fs) for _, _, fs in os.walk('/tmp/jm'))
print(f'TOTAL_FILES={n}', flush=True)
