"""搜索并下载漫画 - v2"""
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
print(f"[*] 客户端: {type(client).__name__}")
print(f"[*] 方法: {[m for m in dir(client) if 'search' in m.lower() or 'album' in m.lower()]}")

if action == "search":
    # 尝试多种搜索方式
    try:
        result = client.search_album(keyword, page=1)
    except AttributeError:
        # API 客户端没有 search_album，用 search 方法
        result = client.search(keyword, page=1)
    
    print(f"\n搜索 '{keyword}' 结果:")
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<15}")
    print("-"*75)
    for album in result[:20]:
        name = album.name[:38] if album.name else "?"
        print(f"{album.id:>8} | {name:<40} | {album.page_count:>4} | {str(album.author)[:15]:<15}")

elif action == "download":
    album_id = keyword
    print(f"下载漫画: {album_id}")
    result = download_album(album_id, option=opt)
    print(f"下载完成!")
    files = glob.glob("/tmp/jm/**/*", recursive=True)
    print(f"共 {len(files)} 个文件")
    for f in files[:30]:
        print(f"  {f}")
