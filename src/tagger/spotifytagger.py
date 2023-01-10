import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyTagger():
    def __init__(self, client_id, client_secret):
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self._sp = spotipy.Spotify(auth_manager=auth_manager)
    def processTracks(self, tracks:dict):
        for trackInfo in tracks.values():
            if not trackInfo.get('spotify'):
                trackInfo['spotify'] = {}

            # Do not process if there is already a spotify info
            if trackInfo['spotify'].get('track') is not None:
                continue

            artist = ''
            if trackInfo.get('artist'):
                artist = str(trackInfo['artist']) + ' '

            for tries in range(0, 2):
                q = artist
                q += trackInfo['title']

                try:
                    results = self._sp.search(q, limit=3, market='DE')
                except Exception:
                    continue

                if results.get('tracks') and results['tracks'].get('items'):
                    trackItem = results['tracks']['items'][0]
                    trackInfo['spotify']['track'] = trackItem['uri']
                    trackInfo['spotify']['album'] = trackItem['album']['uri']
                    trackInfo['spotify']['image'] = trackItem['album']['images'][0]['url']
                    break
                elif trackInfo.get('artist'):
                    for char in [',', ' ']:
                        artist = str(trackInfo['artist'])
                        lastSpacePos = artist.rfind(char)
                        if lastSpacePos != -1:
                            artist = artist[lastSpacePos + 1:] + ' '
                            break

            if trackInfo['spotify'].get('track') is None:
                    trackInfo['spotify']['track'] = ''