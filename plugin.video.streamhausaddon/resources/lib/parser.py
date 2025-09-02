import requests
from bs4 import BeautifulSoup

def search_movies(query):
    """
    Vyhledá filmy podle názvu na Prehrajto a vrátí seznam s názvem a odkazem na stránku.
    """
    query = query.replace(" ", "+")
    search_url = f"https://prehrajto.cz/hledat?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    movies = []
    for item in soup.select("a.film-link"):  # uprav podle skutečného HTML
        movies.append({
            "title": item.text.strip(),
            "url": item['href']
        })
    return movies

def get_stream_url_from_page(page_url):
    """
    Získá přímý odkaz na MP4/M3U8 ze stránky s videem.
    Pro testování vrací veřejný video odkaz.
    """
    # zde musí přijít logika pro Prehrajto
    return "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
