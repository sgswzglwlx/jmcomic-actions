# JMComic 漫画下载器 - GitHub Actions 版

## 使用方法

### 方式一：直接使用本仓库

1. **Fork 本仓库**
2. 进入你的仓库 → **Actions** 标签页
3. 找到 **JMComic 漫画下载** 工作流
4. 点击 **Run workflow**
5. 填写参数：
   - `album_ids`: 漫画ID（如 `123456` 或 `123456,789012`）
   - `search_keyword`: 搜索关键词（可选）
   - `output_format`: `images` 或 `pdf`
6. 运行完成后，下载 artifacts

### 方式二：本地运行

```bash
pip install jmcomic
python3 -c "from jmcomic import download_album; download_album('123456')"
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| album_ids | 要下载的漫画ID，多个用逗号分隔 | `123456,789012` |
| search_keyword | 搜索关键词，留空则按ID下载 | `火影忍者` |
| search_page | 搜索页码 | `1` |
| output_format | 输出格式：images(图片) 或 pdf | `images` |

## 工作原理

利用 GitHub Actions 的 Ubuntu 运行环境，通过 jmcomic 库连接禁漫天堂 API，
实现自动化下载。因为 GitHub 服务器的 IP 未被禁漫天堂封锁，可以正常连接。

## 注意事项

- 下载的文件在 GitHub 上保留 90 天
- 免费用户每次运行限 6 小时
- 建议下载后及时取走文件
