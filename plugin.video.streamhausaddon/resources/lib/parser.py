import requests
from bs4 import BeautifulSoup

def get_stream_url(title):
    """
    Vyhledá film na Prehrajto a vrátí přímý odkaz na video.
    Pro testování vrací veřejný MP4 odkaz, ale logika pro Prehrajto je tu.
    """
    # 1️⃣ Připrav vyhledávací URL (Pro Prehrajto)
    query = title.replace(" ", "+")
    search_url = f"https://prehrajto.cz/hledat?q={query}"

    # 2️⃣ Pošli GET request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    r = requests.get(search_url, headers=headers)
    html = r.text

    # 3️⃣ Parse HTML pomocí BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # 4️⃣ Najdi první odkaz na video (zde placeholder, nahraď reálným selektorem)
    video_page = soup.find("a", class_="film-link")
    if video_page:
        video_url = video_page['href']  # stránka s videem

        # 5️⃣ Získej přímý stream link (.mp4 nebo .m3u8) z video_page
        # zde je potřeba nahradit logikou podle F12 Network
        # např. requests.get(video_url) + parse script tag nebo m3u8
        # Pro testování použijeme veřejný video soubor:
        return "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

    return None
