"""漫画搜索/浏览/下载工具"""
import sys, os, glob
from jmcomic import create_option_by_str, download_album

action = sys.argv[1] if len(sys.argv) > 1 else "search"
keyword = sys.argv[2] if len(sys.argv) > 2 else ""

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
    image: 10
    photo: 3
log: false
""")

client = opt.new_jm_client()

def print_albums(albums, title):
    print(f"\n{title} ({len(albums)}条):")
    # 先看看第一个元素的结构
    if albums:
        a = albums[0]
        print(f"[DEBUG] 类型: {type(a).__name__}")
        if isinstance(a, dict):
            print(f"[DEBUG] dict keys: {list(a.keys())}")
            print(f"[DEBUG] 样例: {str(a)[:300]}")
        else:
            print(f"[DEBUG] 属性: {[x for x in dir(a) if not x.startswith('_')][:20]}")
    
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<16}")
    print("-"*75)
    for a in albums[:30]:
        if isinstance(a, dict):
            aid = a.get('id', '?')
            name = (a.get('name') or a.get('title') or '?')[:38]
            pages = a.get('page_count', a.get('count', '?'))
            author = (a.get('author') or '?')[:15]
        else:
            aid = getattr(a, 'id', '?')
            name = (getattr(a, 'name', '') or '?')[:38]
            pages = getattr(a, 'page_count', '?')
            author = (getattr(a, 'author', '') or '?')[:15]
        print(f"{str(aid):>8} | {str(name):<40} | {str(pages):>4} | {str(author):<15}")

if action == "search":
    result = client.search_tag(keyword, page=1)
    print_albums(result, f"🔍 搜索 '{keyword}'")

elif action == "download":
    album_id = keyword
    print(f"📥 下载漫画: {album_id}")
    try:
        download_album(album_id, option=opt)
        print("✅ 下载完成!")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
