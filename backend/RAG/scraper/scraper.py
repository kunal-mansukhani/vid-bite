from bs4 import BeautifulSoup
import requests
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urljoin, urlparse, urldefrag

def get_all_links(url, base_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        if full_url.startswith(base_url) and full_url != url:
            yield full_url

def crawl_site(start_url, base_url, debug=False):
    visited = set()
    to_visit = [start_url]
    
    while to_visit:
        current_url = to_visit.pop(0)
        current_url, _ = urldefrag(current_url)
        if current_url not in visited and current_url.startswith(base_url):
            if debug:
                print(f"Crawling: {current_url}")
            visited.add(current_url)
            to_visit.extend(link for link in get_all_links(current_url, base_url) if link not in visited)
    
    return list(visited)

def extract_content_with_sections(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('article')
    if not article:
        return None
    
    main_content = article.get_text(strip=True)

    sections = []
    for h in article.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        sections.append({'id': h.get('id', ''), 'title': h.get_text(strip=True)})
    
    return {'url': url, 'content': main_content, 'sections': ' '.join(s['title'] for s in sections)}

def get_page_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return None
    return extract_content_with_sections(response.text, url)


def scrape_docs(start_url, base_url=None, verbose=False):
    if base_url is None:
        base_url = f"{urlparse(start_url).scheme}://{urlparse(start_url).netloc}"
    if verbose:
        print(f"Base URL: {base_url}")
    all_urls = crawl_site(start_url, start_url, debug=verbose)

    documents = []
    for url in all_urls:
        content = get_page_content(url)
        if content:
            doc = Document(
                page_content=content['content'],
                metadata={'url': content['url'], 'sections': content['sections']}
            )

            documents.append(doc)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    split_docs = text_splitter.split_documents(documents)
    if verbose:
        print(f"Scraped {len(documents)} documents")
        print(f"Split into {len(split_docs)} chunks")
        for doc in documents:
            print(doc.metadata['url'])
            print(doc.page_content[:100])
    return split_docs



if __name__ == '__main__':
    print("Scraping Manim Community Docs")
    docs = scrape_docs("https://docs.manim.community/en/stable/", verbose=True)