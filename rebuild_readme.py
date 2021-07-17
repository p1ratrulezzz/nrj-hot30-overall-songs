from src.parser.nrjparser import NRJParser
from src.storage.jsonstorage import JsonStorage
import constants

parser = NRJParser()

storage = JsonStorage(filename = constants.JSON_FILENAME)
#tracks = parser.parseTracks()
#storage.mergeTracks(tracks)
#storage.save()

table = '|Position|Track|\n'
table += '|---|--------|\n'
for trackInfo in storage.getTracks().values():
    trackname = str(trackInfo.get('artist')) + ' - ' + trackInfo['title']
    table += '|{position}|{trackname}|\n'.format(position = int(trackInfo['position_avg']), trackname = trackname)

with open('template/readme_top.md') as readme_top_fp:
    with open('README.md', 'w') as fp:
        fp.write(readme_top_fp.read())
        fp.write('\n')
        fp.write(table)
        fp.close()
    readme_top_fp.close()
