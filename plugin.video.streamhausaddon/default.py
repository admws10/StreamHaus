import sys
import urllib.parse
import xbmcplugin
import xbmcgui
from resources.lib import parser

handle = int(sys.argv[1])

def search_movies():
    # otevře dialog pro zadání názvu filmu
    keyboard = xbmcgui.Dialog().input("Zadej název filmu")
    if not keyboard:
        return

    # získá seznam filmů podle parseru
    movies = parser.search_movies(keyboard)
    for movie in movies:
        url = f"?action=play&title={urllib.parse.quote(movie['title'])}&link={urllib.parse.quote(movie['url'])}"
        li = xbmcgui.ListItem(label=movie['title'])
        xbmcplugin.addDirectoryItem(handle, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(handle)

def play_movie(title, link):
    # zavolá parser pro přímý stream
    url = parser.get_stream_url_from_page(link)
    xbmc.Player().play(url)

# zpracování parametrů
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

if "action" in params:
    if params["action"] == "play":
        play_movie(params["title"], params["link"])
else:
    search_movies()
