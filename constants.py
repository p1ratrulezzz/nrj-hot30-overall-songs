JSON_FILENAME = 'resources/tracks.json'
NRJ_URL = 'https://www.energyfm.ru/nrj_hot_30'

with open('spotify_token.txt', 'r') as token_fp:
    SPOTIFY_TOKEN = token_fp.readline()
    token_fp.close()