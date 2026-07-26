"""漫画搜索/浏览工具"""
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
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<16}")
    print("-"*75)
    for a in albums[:30]:
        if isinstance(a, tuple):
            aid, name = str(a[0]), str(a[1])[:38]
            pages = str(a[2]) if len(a) > 2 else "?"
            author = str(a[3])[:15] if len(a) > 3 else "?"
        else:
            aid, name = str(a.id), (a.name or "?")[:38]
            pages, author = str(a.page_count), (a.author or "?")[:15]
        print(f"{aid:>8} | {name:<40} | {pages:>4} | {author:<15}")

if action == "hot":
    # 热门推荐
    result = client.search_tag("热门", page=1)
    print_albums(result, "🔥 热门推荐")

elif action == "new":
    # 最新
    result = search("", "latest", "all", "all", "all", page=1)
    print_albums(result, "✨ 最新上架")

elif action == "popular":
    # 人气最高
    result = search("", "popular", "all", "all", "all", page=1)
    print_albums(result, "⭐ 人气最高")

elif action == "tag":
    # 按标签搜索
    tags = ["纯爱", "NTR", "原神", "崩坏", "FGO", "碧蓝档案", "蔚蓝档案", "同人"]
    for tag in tags:
        try:
            result = client.search_tag(tag, page=1)
            if result:
                print_albums(result, f"🏷️ {tag}")
        except:
            pass

elif action == "search":
    result = client.search_tag(keyword, page=1)
    print_albums(result, f"🔍 搜索 '{keyword}'")

elif action == "download":
    album_id = keyword
    print(f"下载漫画: {album_id}")
    try:
        download_album(album_id, option=opt)
        print("下载完成!")
    except Exception as e:
        print(f"下载失败: {e}")
