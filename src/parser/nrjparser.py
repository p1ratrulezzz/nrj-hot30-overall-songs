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
        divTexts = bs.select('ul.chart-list>li>div.chart-name')
        divTexts.reverse()
        position = 1
        for el in divTexts:
            el: element.Tag
            trackName = self.clearTrackName(el.get_text())
            trackInfo = self.parseTrackName(trackName)
            trackInfo['position'] = position
            trackInfo['datetime'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
            position += 1
            tracks.append(trackInfo)

        return tracks