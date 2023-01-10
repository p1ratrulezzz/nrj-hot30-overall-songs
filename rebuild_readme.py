from src.parser.nrjparser import NRJParser
from src.storage.jsonstorage import JsonStorage
from constants import *
from operator import itemgetter
from src.tagger.spotifytagger import SpotifyTagger

parser = NRJParser()
tagger = SpotifyTagger(SPOTIFY.CLIENT_ID, SPOTIFY.CLIENT_SECRET)

storage = JsonStorage(filename = JSON_FILENAME)
tracks = parser.parseTracks()
storage.mergeTracks(tracks)
tagger.processTracks(storage.getTracks())
storage.save()

table = '|Position||Track||\n'
table += '|---|---|--------|---|\n'
tracks_sorted = sorted(storage.getTracks().values(), key=itemgetter('position_avg'))
for trackInfo in tracks_sorted:
    trackname = ''
    trackname += str(trackInfo.get('artist_display')) + ' - ' + trackInfo['title']

    # Add image
    image = ' '
    if trackInfo.get('spotify') and trackInfo['spotify'].get('image'):
        image = '<img src="{url}" />'.format(url = trackInfo['spotify']['image'])

    link = ' '
    if trackInfo.get('spotify') and trackInfo['spotify'].get('album'):
        trackId = trackInfo['spotify']['track'].split(':')[-1]
        link = '[{image}]({url})'.format(url = 'https://open.spotify.com/track/' + trackId, image = SPOTIFY.ICON_URL)
        
    change_icon = ''
    _positions = trackInfo['positions']
    if len(_positions) > 1:
        current_position = trackInfo['positions'][-1]['value']
        delta = _positions[-1]['value'] - _positions[-2]['value']
        if delta != 0:
            change_icon = '🔻' if delta < 0 else '⬆'
    else:
        current_position = _positions[0]['value']

    table += '|{position}({current_position}){change_icon}|{image}|{trackname}|{link}|\n'.format(
        position = int(trackInfo['position_avg']),
        current_position = current_position,
        trackname = trackname,
        image = image,
        link = link,
        change_icon = change_icon
    )

with open('template/readme_top.md') as readme_top_fp:
    with open('README.md', 'w', encoding='utf8') as fp:
        fp.write(readme_top_fp.read())
        fp.write('\n')
        fp.write(table)
        fp.close()
    readme_top_fp.close()
