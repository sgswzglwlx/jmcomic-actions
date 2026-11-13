# -*- coding: utf-8 -*-
"""禁漫批量下载：专辑ID逗号分隔，逐部下载并打包 zip 到 /tmp/out"""
import os, re, shutil, sys, traceback
from jmcomic import create_option_by_str, download_album

ids = [x.strip() for x in sys.argv[1].split(',') if x.strip()]
print(f"IDS({len(ids)}): {ids}", flush=True)

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
log: false
""")

os.makedirs('/tmp/out', exist_ok=True)
ok, fail = [], []
for aid in ids:
    print(f"=== START {aid} ===", flush=True)
    try:
        download_album(aid, option=opt)
        # 找该 id 对应的目录（最新修改）
        cands = [d for d in os.listdir('/tmp/jm') if d.startswith(aid)]
        if not cands:
            subs = [os.path.join('/tmp/jm', d) for d in os.listdir('/tmp/jm')]
            subs = [s for s in subs if os.path.isdir(s)]
            cands_dirs = [s for s in subs if aid in os.path.basename(s)]
        base = '/tmp/jm'
        # 判定要打包的目录：标题含 id? 直接打包整个 /tmp/jm 下该 aid 的目录
        target = None
        for root, dirs, files in os.walk('/tmp/jm'):
            if os.path.basename(root).startswith(aid) and files:
                target = root; break
        if target is None:
            # 退而求其次：本 album 目录（含章节子目录）
            for root, dirs, files in os.walk('/tmp/jm'):
                if os.path.basename(root).startswith(aid):
                    target = root; break
        if target:
            zbase = f'/tmp/out/{aid}'
            zpath = shutil.make_archive(zbase, 'zip', target)
            sz = os.path.getsize(zpath)
            n = sum(len(f) for _, _, f in os.walk(target))
            print(f"ZIP> {aid} | {os.path.basename(target)} | {n} files | {sz/1048576:.1f} MB", flush=True)
            ok.append(aid)
        else:
            print(f"NO_DIR {aid}", flush=True); fail.append(aid)
    except Exception as e:
        print(f"=== FAIL {aid}: {repr(e)[:200]} ===", flush=True)
        traceback.print_exc()
        fail.append(aid)

print(f"SUMMARY ok={len(ok)} fail={len(fail)} fail_ids={fail}", flush=True)
tot = sum(os.path.getsize(os.path.join('/tmp/out', f)) for f in os.listdir('/tmp/out')) if os.path.isdir('/tmp/out') else 0
print(f"TOTAL_OUT {tot/1048576:.1f} MB", flush=True)
print("ALL_DONE", flush=True)
