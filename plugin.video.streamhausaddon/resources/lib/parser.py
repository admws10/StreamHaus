# resources/lib/parser.py

import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def search_movies(query):
    query = query.replace(" ", "+")
    search_url = f"https://prehrajto.cz/hledat?q={query}"

    r = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    movies = []
    for a in soup.select("a.film-link"):
        title = a.text.strip()
        url = a['href']
        if url.startswith("/"):
            url = "https://prehrajto.cz" + url
        movies.append({"title": title, "url": url})
    return movies

def get_stream_url_from_page(page_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(page_url)
        time.sleep(3)

        try:
            video_elem = driver.find_element("tag name", "video")
            url = video_elem.get_attribute("src")
            if url:
                return url
        except:
            pass

        m = re.search(r'https?://[^\s\'"]+\.m3u8', driver.page_source)
        if m:
            return m.group(0)
        m = re.search(r'https?://[^\s\'"]+\.mp4', driver.page_source)
        if m:
            return m.group(0)

    finally:
        driver.quit()

    return None
