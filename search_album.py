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
log: false
""")

client = opt.new_jm_client()

def print_albums(albums, title):
    print(f"\n{title} ({len(albums)}条):")
    if albums:
        a = albums[0]
        print(f"[DEBUG] 类型: {type(a).__name__}, len={len(a) if hasattr(a,'__len__') else 'N/A'}")
        print(f"[DEBUG] 内容: {str(a)[:500]}")
    
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<16}")
    print("-"*75)
    for a in albums[:30]:
        if isinstance(a, (list, tuple)):
            # tuple 格式: (id, name_dict, ...)
            aid = str(a[0]) if len(a) > 0 else '?'
            if len(a) > 1 and isinstance(a[1], dict):
                name = (a[1].get('name') or a[1].get('title') or str(a[1])[:30])[:38]
                author = (a[1].get('author', '') or '?')[:15]
                pages = a[1].get('page_count', a[1].get('count', '?'))
            else:
                name = str(a[1])[:38] if len(a) > 1 else '?'
                author = str(a[2])[:15] if len(a) > 2 else '?'
                pages = str(a[3]) if len(a) > 3 else '?'
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
    print(f"📥 下载漫画: {keyword}")
    opt2 = create_option_by_str("""
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
    try:
        download_album(keyword, option=opt2)
        print("✅ 下载完成!")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
