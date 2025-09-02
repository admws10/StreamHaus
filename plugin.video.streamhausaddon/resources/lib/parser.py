# resources/lib/parser.py

import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def search_movies(query):
    """
    Vyhledá filmy podle názvu na webu a vrátí seznam s názvem a odkazem.
    Pro testování vrací statické položky.
    """
    # ❗ Zde později doplnit logiku pro Prehrajto
    return [
        {"title": "Big Buck Bunny", "url": "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"},
        {"title": "Spider-Man", "url": "https://storage4-1.premiumcdn.net/29851184/oZktQ9Iy8CAJIN7FQYT6WIJ5iL9i1MfzBuKvHGmcMntjDhLWiYGfw1se2TOATzgHBos20U9vhRGHlBFnKsy8U32iz9FvOHMWHA4IojHnlSRofJOH68fNl.mp4?token=A1206ZyNVCax&expires=1756922310&sparams=token%2Cpath%2Cexpires&signature=d979babe556226416f7db51867a586996aa2c05e"}
    ]

def get_stream_url_from_page(page_url):
    """
    Získá přímý odkaz na MP4/M3U8.
    Pro test vrací přímo odkaz z search_movies.
    """
    if page_url.endswith(".mp4") or page_url.endswith(".m3u8"):
        return page_url

    # Pokud by byla stránka HTML, lze použít Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(page_url)
    time.sleep(3)  # čekání na JS

    # Hledání video tagu
    try:
        video_elem = driver.find_element_by_tag_name("video")
        url = video_elem.get_attribute("src")
        if url:
            driver.quit()
            return url
    except:
        pass

    # Regex pro M3U8 v page_source
    m = re.search(r"https?://.*?\.m3u8", driver.page_source)
    if m:
        driver.quit()
        return m.group(0)

    driver.quit()
    return None
