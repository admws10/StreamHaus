from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def search_movies(query):
    """
    Vyhledá filmy podle názvu na Prehrajto a vrátí seznam s názvem a odkazem.
    """
    query = query.replace(" ", "+")
    search_url = f"https://prehrajto.cz/hledat?q={query}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(search_url)
    time.sleep(3)  # počkáme, než se načtou výsledky

    movies = []
    elems = driver.find_elements_by_css_selector("a.film-link")  # uprav podle skutečného HTML
    for e in elems:
        title = e.text
        url = e.get_attribute("href")
        movies.append({"title": title, "url": url})

    driver.quit()
    return movies

def get_stream_url_from_page(page_url):
    """
    Otevře stránku filmu a získá přímý MP4/M3U8 odkaz.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(page_url)
    time.sleep(3)  # počkáme, až se načte player

    # Hledáme video tag nebo JS proměnnou s odkazem na stream
    try:
        video_elem = driver.find_element_by_tag_name("video")
        url = video_elem.get_attribute("src")
        if url:
            driver.quit()
            return url
    except:
        pass

    # Pokud video tag nenajdeš, může být odkaz v JS
    # driver.page_source → parsovat regexem pro .mp4/.m3u8
    import re
    m = re.search(r"https?://.*?\.m3u8", driver.page_source)
    if m:
        driver.quit()
        return m.group(0)

    driver.quit()
    return None
