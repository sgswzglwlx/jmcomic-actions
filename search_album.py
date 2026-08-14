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
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<16}")
    print("-"*75)
    for a in albums[:30]:
        if isinstance(a, (list, tuple)):
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

elif action == "info":
    aid = keyword
    print(f"📋 漫画详情: {aid}")
    try:
        album = client.get_album_detail(aid)
        print(f"标题: {album.name}")
        print(f"作者: {album.author}")
        print(f"章节数: {album.page_count}")
        print(f"别名(CN): {album.alias_cn}")
        print(f"别名(EN): {album.alias_en}")
        print(f"ID: {album.id}")
        # 尝试打印所有属性
        props = album.get_properties_dict() if hasattr(album, 'get_properties_dict') else {}
        for k, v in props.items():
            if k not in ('id',) and v:
                print(f"  {k}: {str(v)[:80]}")
    except Exception as e:
        print(f"❌ 获取失败: {e}")


elif action == "author":
    result = client.search_author(keyword, page=1)
    print(f"\n👤 作者 '{keyword}' 的作品 ({len(result)}条):")
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<16}")
    print("-"*75)
    for a in result[:30]:
        if isinstance(a, (list, tuple)):
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

elif action == "download":
    print(f"\u{4e0b}\u8f7d\u6f2b\u753b}: {keyword}")
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
        print("\u2705 \u4e0b\u8f7d\u5b8c\u6210!")
        # 打包 zip
        import subprocess, glob
        subprocess.run(['zip', '-r', '-q', f'/tmp/jm_{keyword}.zip', '/tmp/jm/'], check=True)
        print(f"\u2705 \u6253\u5305\u5b8c\u6210: /tmp/jm_{keyword}.zip")
    except Exception as e:
        print(f"\u274c \u4e0b\u8f7d\u5931\u8d25: {e}")
