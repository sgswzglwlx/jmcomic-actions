# -*- coding: utf-8 -*-
"""批量下载 + 扁平化 + 单包压缩：python3 jm_grab.py "id1,id2,...\""""
import os, re, shutil, sys, zipfile, time
from jmcomic import create_option_by_str, download_album

ids = [x.strip() for x in sys.argv[1].split(',') if x.strip()]
print('IDS:', len(ids), ids, flush=True)

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
    image: 24
    photo: 4
log: false
""")

failed = []
for i, aid in enumerate(ids, 1):
    t = time.time()
    try:
        download_album(aid, option=opt)
        print(f'OK {i}/{len(ids)} {aid} {int(time.time()-t)}s', flush=True)
    except Exception as e:
        failed.append(aid)
        print(f'FAIL {i}/{len(ids)} {aid}: {e!r}'[:200], flush=True)

print('FAILED:', failed, flush=True)

# ---- 扁平化：每部作品一个文件夹（仅一层），图片直接放里面 ----
root, out = '/tmp/jm', '/tmp/out'
shutil.rmtree(out, ignore_errors=True)
os.makedirs(out, exist_ok=True)

def clean(s):
    s = re.sub(r'[\\/:*?"<>|\r\n\t]', '_', s)
    return re.sub(r'\s+', ' ', s).strip()[:90]

idx = 0
manifest = []
for author in sorted(os.listdir(root)):
    ap = os.path.join(root, author)
    if not os.path.isdir(ap): continue
    for title in sorted(os.listdir(ap)):
        tp = os.path.join(ap, title)
        if not os.path.isdir(tp): continue
        imgs = []
        for dp, _, fs in os.walk(tp):
            for f in fs:
                if f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')):
                    imgs.append(os.path.join(dp, f))
        if not imgs: continue
        imgs.sort()
        idx += 1
        folder = os.path.join(out, f'{idx:02d}_{clean(title)}')
        os.makedirs(folder, exist_ok=True)
        for n, f in enumerate(imgs, 1):
            shutil.copy(f, os.path.join(folder, f'{n:05d}{os.path.splitext(f)[1]}'))
        manifest.append(f'{idx:02d}\t{len(imgs)}\t{title}')
        print(f'FLAT {idx:02d} {len(imgs)}p {title[:60]}', flush=True)

print('FOLDERS:', idx, 'TOTAL_IMGS:', sum(int(m.split("\t")[1]) for m in manifest), flush=True)
open('/tmp/manifest.txt','w').write('\n'.join(manifest))

# ---- 打单包 ----
zp = '/tmp/out.zip'
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_STORED, allowZip64=True) as z:
    for dp, _, fs in os.walk(out):
        for f in fs:
            full = os.path.join(dp, f)
            z.write(full, os.path.relpath(full, out))
sz = os.path.getsize(zp)
print(f'ZIP {zp} {sz} bytes ({sz/1048576:.1f} MB)', flush=True)
