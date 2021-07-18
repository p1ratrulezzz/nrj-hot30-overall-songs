import yaml

__all__ = ["JSON_FILENAME", "NRJ_URL", "SPOTIFY"]

JSON_FILENAME = 'resources/tracks.json'
NRJ_URL = 'https://www.energyfm.ru/nrj_hot_30'

with open('spotify.yml', 'r') as token_fp:
    spotify_data = yaml.safe_load(token_fp)
    token_fp.close()

intersect = spotify_data.keys() & {'client_id', 'client_secret'}
if len(intersect) != 2:
    raise RuntimeError('There must be client_id and client_secret set for spotify')

class SPOTIFY:
    CLIENT_ID = spotify_data['client_id']
    CLIENT_SECRET = spotify_data['client_secret']
    ICON_URL = 'data:image/png;base64,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'

