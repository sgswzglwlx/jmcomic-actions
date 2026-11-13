# -*- coding: utf-8 -*-
"""批量下载: python3 jm_batch.py "id1,id2,id3\""""
import sys
from jmcomic import create_option_by_str, download_batch

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
download_batch(ids, opt)
print('DONE', ids, flush=True)
