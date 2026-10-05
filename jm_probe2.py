# -*- coding: utf-8 -*-
"""禁漫 ID 交叉探测 v2：基线校验 + 站点 ID 量级 + 目标页直抓"""
import re, sys
from curl_cffi import requests as creq
from jmcomic import create_option_by_str

TARGET = sys.argv[1] if len(sys.argv) > 1 else "3927698"

opt = create_option_by_str("""
client:
  impl: api
  postman:
    type: curl_cffi
    meta_data:
      impersonate: chrome
  retry_times: 2
log: false
""")
client = opt.new_jm_client()

print("=== 1) 基线校验（已知存在的本子）===")
for tid in ['1464279', '1240338']:
    try:
        a = client.get_album_detail(tid)
        print(f"  BASE OK {tid}: {a.name} / {a.author} / {len(getattr(a,'episode_list',[]))}话")
    except Exception as e:
        print(f"  BASE FAIL {tid}: {repr(e)[:120]}")

print("=== 2) 站点 ID 量级（首页最新本子）===")
s = creq.Session(impersonate='chrome')
for url in ['https://18comic.vip/albums', 'https://18comic.vip/']:
    try:
        r = s.get(url, timeout=40)
        ids = re.findall(r'/album/(\d+)/', r.text)
        ids = [i for i in ids if len(i) >= 5]
        print(f"  {url} -> HTTP {r.status_code}, {len(r.text)}B, 抓到 {len(ids)} 个album id")
        if ids:
            nums = sorted(set(int(i) for i in ids))
            print(f"     min={nums[0]} max={nums[-1]} 样本={nums[:8]} ... {nums[-8:]}")
        print(f"     标题: {re.findall(r'<title>(.*?)</title>', r.text)[:1]}")
    except Exception as e:
        print(f"  {url} err: {repr(e)[:150]}")

print("=== 3) 直抓目标页 ===")
for u in [f'https://18comic.vip/album/{TARGET}/', f'https://18comic.vip/photo/{TARGET}/']:
    try:
        r = s.get(u, timeout=40, allow_redirects=True)
        t = re.findall(r'<title>(.*?)</title>', r.text)
        print(f"  {u} -> HTTP {r.status_code}, {len(r.text)}B, title={t[:1]}, final={r.url}")
        body = re.sub(r'<[^>]+>', ' ', r.text)
        body = re.sub(r'\s+', ' ', body)
        print(f"     摘要: {body[:400]}")
    except Exception as e:
        print(f"  {u} err: {repr(e)[:150]}")
