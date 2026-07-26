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

def get_id(a):
    if isinstance(a, dict): return a.get('id', '?')
    return getattr(a, 'id', '?')

def get_name(a):
    if isinstance(a, dict): return (a.get('name', a.get('title', '')) or '?')[:38]
    return (getattr(a, 'name', '') or '?')[:38]

def get_pages(a):
    if isinstance(a, dict): return a.get('page_count', a.get('count', '?'))
    return str(getattr(a, 'page_count', '?'))

def get_author(a):
    if isinstance(a, dict): return (a.get('author', '') or '?')[:15]
    return (getattr(a, 'author', '') or '?')[:15]

def print_albums(albums, title):
    print(f"\n{title} ({len(albums)}条):")
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<16}")
    print("-"*75)
    for a in albums[:30]:
        print(f"{get_id(a):>8} | {get_name(a):<40} | {get_pages(a):>4} | {get_author(a):<15}")

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
