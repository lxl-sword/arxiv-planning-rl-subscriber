import feedparser
import datetime
import os

def arxiv_search(query, max_results=5):
    base_url = 'http://export.arxiv.org/api/query?'
    search_url = f'search_query={query}&start=0&max_results={max_results}'
    response = feedparser.parse(base_url + search_url)
    return response.entries

def save_results_as_html(entries):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs("docs", exist_ok=True)  # 确保 docs 目录存在
    filename = f"docs/arxiv_{today}.html"  # 每日爬取结果以日期命名

    # 生成每日的结果页面
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>arXiv Papers - {today}</title>\n</head>\n<body>\n")
        f.write(f"<h1>📚 arXiv Papers on {today}</h1>\n")

        for entry in entries:
            f.write(f"<h2><a href='{entry.link}' target='_blank'>{entry.title}</a></h2>\n")
            authors = ', '.join(author.name for author in entry.authors)
            f.write(f"<p><strong>Authors:</strong> {authors}</p>\n")
            f.write(f"<p><strong>Summary:</strong> {entry.summary[:500]}...</p>\n")
            f.write("<hr>\n")

        f.write("</body>\n</html>")

    # 更新 index.html 页面，添加历史链接
    update_index(today)

    print(f"✅ Results saved to {filename}")

def update_index(latest_date):
    index_file = "docs/index.html"
    if not os.path.exists(index_file):
        with open(index_file, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>arXiv Archive</title>\n</head>\n<body>\n")
            f.write("<h1>📚 arXiv Paper Archive</h1>\n")
            f.write("<ul>\n")
            f.write("</ul>\n")
            f.write("</body>\n</html>")

    # 读取现有 index.html
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 防止重复添加同一天的链接
    new_entry = f'<li><a href="arxiv_{latest_date}.html">{latest_date} Papers</a></li>\n'
    if new_entry not in content:
        content = content.replace("<ul>\n", f"<ul>\n{new_entry}")

    # 保存更新后的 index.html
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    query = 'all:planning+AND+all:"reinforcement learning"'
    results = arxiv_search(query, max_results=100)
    save_results_as_html(results)
