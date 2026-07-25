"""搜索并下载漫画 - v4"""
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

if action == "search":
    result = client.search_tag(keyword, page=1)
    
    print(f"搜索 '{keyword}' 结果 ({len(result)}条):")
    print(f"{'ID':>8} | {'标题':<40} | {'章节':>4} | {'作者':<15}")
    print("-"*75)
    
    # search_tag 返回的是 list of tuple: (album_id, name, page_count, author, ...)
    for album in result[:30]:
        if isinstance(album, tuple):
            aid, name = album[0], album[1]
            pages = album[2] if len(album) > 2 else "?"
            author = album[3] if len(album) > 3 else "?"
            name_str = str(name)[:38] if name else "?"
        else:
            aid = album.id
            name_str = album.name[:38] if album.name else "?"
            pages = album.page_count
            author = album.author[:15] if album.author else "?"
        print(f"{aid:>8} | {name_str:<40} | {pages:>4} | {str(author)[:15]:<15}")

elif action == "search_all":
    result = client.search("", "popular", "all", "all", "all", page=1)
    print(f"最新漫画 ({len(result)}条):")
    for item in result[:5]:
        print(f"  {item}")

elif action == "download":
    album_id = keyword
    print(f"下载漫画: {album_id}")
    try:
        result = download_album(album_id, option=opt)
        print(f"下载完成!")
        files = glob.glob("/tmp/jm/**/*", recursive=True)
        print(f"共 {len(files)} 个文件")
        for f in files[:30]:
            sz = os.path.getsize(f)
            print(f"  {f} ({sz/1024:.0f}KB)")
    except Exception as e:
        print(f"下载失败: {e}")

elif action == "debug":
    # 查看 search_tag 返回的类型
    result = client.search_tag(keyword, page=1)
    print(f"类型: {type(result)}")
    print(f"长度: {len(result)}")
    if result:
        print(f"第一个元素类型: {type(result[0])}")
        print(f"第一个元素内容: {result[0]}")
        print(f"第二个元素: {result[1] if len(result)>1 else 'N/A'}")
