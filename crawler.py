import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

# Take root url
target_url = "https://books.toscrape.com/catalogue/page-4.html"

# Request HTML

# Find all <a> objects and extract urls
to_be_crawled = set([target_url])

crawled = set()

session = requests.Session()

logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def fetch(url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return ""


def extract_links(url):
    html = fetch(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        urls = soup.find_all("a")
        for link in urls:
            href = link.get("href")
            if href:
                absolute_url = urljoin(target_url, href)
                if absolute_url not in crawled and absolute_url not in to_be_crawled:
                    to_be_crawled.add(absolute_url)
                if "page" in absolute_url:
                    print(absolute_url)


def save_to_file():
    with open("crawled_urls.txt", "w") as f:
        for url in crawled:
            f.write(url + "\n")


def crawl():
    while to_be_crawled:
        url = to_be_crawled.pop()
        crawled.add(url)
        extract_links(url)
        # print("\033[H\033[J", end="")  # Clears the terminal
        # print(f"Crawled URLS: {len(crawled)}, To Be Crawled: {len(to_be_crawled)}")

    save_to_file()
    print(f"Total Crawled URLs: {len(crawled)}")


crawl()
