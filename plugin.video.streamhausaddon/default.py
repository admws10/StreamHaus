import sys
import os
import urllib.parse
import xbmcplugin
import xbmcgui
from resources.lib import parser

handle = int(sys.argv[1])
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

# cesta k historii
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "resources", "lib", "history.txt")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_history(query):
    history = load_history()
    if query in history:
        history.remove(query)
    history.insert(0, query)
    history = history[:10]  # maximálně 10 položek
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(history))

def search_movies():
    # nabídka historie
    history = load_history()
    if history:
        choice = xbmcgui.Dialog().select("Vyber z historie nebo napiš nový název", history + ["Napsat nový název"])
        if choice == -1:
            return
        elif choice < len(history):
            keyboard = history[choice]
        else:
            keyboard = xbmcgui.Dialog().input("Zadej název filmu")
            if not keyboard:
                return
    else:
        keyboard = xbmcgui.Dialog().input("Zadej název filmu")
        if not keyboard:
            return

    save_history(keyboard)

    movies = parser.search_movies(keyboard)
    if not movies:
        xbmcgui.Dialog().notification("Info", "Žádné filmy nenalezeny", xbmcgui.NOTIFICATION_INFO)
        return

    for movie in movies:
        li = xbmcgui.ListItem(label=movie['title'])
        # mini náhled z Prehrajto (pokud existuje)
        thumb = parser.get_thumbnail(movie['url'])
        if thumb:
            li.setArt({"thumb": thumb, "icon": thumb, "fanart": thumb})
        url = f"?action=play&title={urllib.parse.quote(movie['title'])}&link={urllib.parse.quote(movie['url'])}"
        xbmcplugin.addDirectoryItem(handle, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(handle)

def play_movie(title, link):
    xbmcgui.Dialog().notification("Info", f"Načítání {title}", xbmcgui.NOTIFICATION_INFO)
    url = parser.get_stream_url_from_page(link)
    if url:
        xbmc.Player().play(url)
    else:
        xbmcgui.Dialog().notification("Chyba", "Video nelze přehrát", xbmcgui.NOTIFICATION_ERROR)

if "action" in params:
    if params["action"] == "play":
        play_movie(params["title"], params["link"])
else:
    search_movies()
