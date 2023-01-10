from src.parser.parser import Parser
from bs4 import BeautifulSoup, element
import urllib3
from constants import *
from datetime import datetime, timezone

class NRJParser(Parser):
    _playlist_url = NRJ_URL

    def __init__(self):
        self._http = urllib3.PoolManager()

    def parseTracks(self):
        tracks = []
        r = self._http.request('GET', self._playlist_url)
        bs = BeautifulSoup(r.data, 'html.parser')
        divTexts = bs.select('.hot-30-content__main .hot-30__item')
        position = 1
        for el in divTexts:
            el: element.Tag
            trackName = self.clearTrackName(el.select('.player-titles.player__title')[0].get_text())
            trackInfo = {}

            artistName = el.select('.player-titles.player__subtitle')[0].get_text()
            trackInfo["artist"] = self.clearArtistName(artistName)
            trackInfo["artist_display"] = artistName.strip('\r\n\t ')
            trackInfo["title"] = trackName.strip("\r\n\t ")

            trackInfo['position'] = position
            trackInfo['datetime'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
            position += 1
            tracks.append(trackInfo)

        return tracks