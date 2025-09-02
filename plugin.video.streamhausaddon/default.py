import sys
import urllib.parse
import xbmcplugin
import xbmcgui
from resources.lib import parser

handle = int(sys.argv[1])

# zpracování parametrů z Kodi
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

def list_movies():
    # seznam testovacích filmů (nahraď logikou Prehrajto)
    movies = ["Film A", "Film B", "Film C"]
    for title in movies:
        url = f"?action=play&title={urllib.parse.quote(title)}"
        li = xbmcgui.ListItem(label=title)
        xbmcplugin.addDirectoryItem(handle, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(handle)

def play_movie(title):
    # tady zavoláš parser pro Prehrajto a získáš přímý odkaz na stream
    url = parser.get_stream_url(title)
    xbmc.Player().play(url)

# rozhodnutí podle parametrů
if "action" in params:
    if params["action"] == "play":
        play_movie(params["title"])
else:
    list_movies()
