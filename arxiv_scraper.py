import feedparser
import datetime
import os
from urllib.parse import quote  # 用于 URL 编码

def arxiv_search(query, max_results=5):
    base_url = 'http://export.arxiv.org/api/query?'
    # 对查询参数进行 URL 编码
    #encoded_query = quote(query)
    encoded_query = query
    search_url = f'search_query={encoded_query}&start=0&max_results={max_results}'
    response = feedparser.parse(base_url + search_url)
    return response.entries

def arxiv_search_today(query, max_results=20):
    base_url = 'http://export.arxiv.org/api/query?'
    today = datetime.datetime.now().strftime("%Y%m%d")
    query_with_date = f'({query})+AND+submittedDate:[{today}0000+TO+{today}2359]'
    encoded_query = query_with_date
    search_url = f'search_query={encoded_query}&start=0&max_results={max_results}'
    response = feedparser.parse(base_url + search_url)
    return response.entries

def arxiv_search_previous_day(query, max_results=20):
    base_url = 'http://export.arxiv.org/api/query?'
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    query_with_date = f'({query})+AND+submittedDate:[{yesterday_str}0000+TO+{yesterday_str}2359]'
    encoded_query = query_with_date
    search_url = f'search_query={encoded_query}&start=0&max_results={max_results}'
    response = feedparser.parse(base_url + search_url)
    print(f"🔍 Found {len(response.entries)} papers submitted on {yesterday_str}.")
    return response.entries



def save_results_as_html(entries):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs("docs", exist_ok=True)
    filename = f"docs/arxiv_{today}.html"
   
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>arXiv Papers - {today}</title>\n</head>\n<body>\n")
        f.write(f"<h1>📚 arXiv Papers on {today}</h1>\n")

        if not entries:
            f.write("<p>❌ No papers found for today.</p>\n")
        else:
            for entry in entries:
                f.write(f"<h2><a href='{entry.link}' target='_blank'>{entry.title}</a></h2>\n")
                authors = ', '.join(author.name for author in entry.authors)
                f.write(f"<p><strong>Authors:</strong> {authors}</p>\n")
                f.write(f"<p><strong>Summary:</strong> {entry.summary[:500]}...</p>\n")
                f.write("<hr>\n")
                

        f.write("</body>\n</html>")
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

    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()

    new_entry = f'<li><a href="arxiv_{latest_date}.html">{latest_date} Papers</a></li>\n'
    if new_entry not in content:
        content = content.replace("<ul>\n", f"<ul>\n{new_entry}")

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    query = 'all:planning+AND+all:"reinforcement%20learning"'
    results = arxiv_search(query, max_results=10000)
    #results = arxiv_search_today(query, max_results=100)
    #results = arxiv_search_previous_day(query, max_results=100)
    save_results_as_html(results)
