"""搜索并下载漫画"""
import sys, os
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

if action == "search":
    client = opt.new_jm_client()
    result = client.search_album(keyword, page=1)
    print(f"搜索 '{keyword}' 结果 ({len(result)}条):")
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
    # 列出下载的文件
    import glob
    files = glob.glob("/tmp/jm/**/*", recursive=True)
    print(f"共 {len(files)} 个文件")
    for f in files[:20]:
        print(f"  {f}")
