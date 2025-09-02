import sys
import urllib.parse
import xbmcplugin
import xbmcgui
from resources.lib import parser

handle = int(sys.argv[1])
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

def search_movies():
    # input box pro zadání názvu filmu
    keyboard = xbmcgui.Dialog().input("Zadej název filmu")
    if not keyboard:
        return

    # volání parseru pro vyhledání filmů
    movies = parser.search_movies(keyboard)
    for movie in movies:
        url = f"?action=play&title={urllib.parse.quote(movie['title'])}&link={urllib.parse.quote(movie['url'])}"
        li = xbmcgui.ListItem(label=movie['title'])
        xbmcplugin.addDirectoryItem(handle, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(handle)

def play_movie(title, link):
    # volání parseru pro získání přímého odkazu na stream
    url = parser.get_stream_url_from_page(link)
    if url:
        xbmc.Player().play(url)
    else:
        xbmcgui.Dialog().notification("Chyba", "Video nelze přehrát", xbmcgui.NOTIFICATION_ERROR)

# rozhodnutí podle parametrů
if "action" in params:
    if params["action"] == "play":
        play_movie(params["title"], params["link"])
else:
    search_movies()
