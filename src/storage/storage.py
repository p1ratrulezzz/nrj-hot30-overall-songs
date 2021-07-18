from abc import ABC, abstractmethod
import json
import zlib

class Storage(ABC):
    _tracks = {}
    _options = {}
    def __init__(self, **kwargs):
        for k in kwargs.keys():
            self._options[k] = kwargs[k]

    @abstractmethod
    def readTracks(self):
        pass

    def getTracks(self):
        return self._tracks

    def mergeTracks(self, newtracks):
        for trackInfo in newtracks:
            hash = self.hashTrack(trackInfo)
            newinfo = {}
            if self._tracks.get(hash):
                newinfo = self._tracks[hash]
            else:
                if trackInfo.get("artist"):
                    newinfo["artist"] = trackInfo["artist"]
                    newinfo['artist_display'] = trackInfo["artist_display"]
                newinfo['title'] = trackInfo['title']

            if not newinfo.get("positions"):
                newinfo['positions'] = []

            if len(newinfo['positions']) == 0 or newinfo['positions'][-1]['value'] != trackInfo['position']:
                newinfo['positions'].append({'value': trackInfo['position'], 'datetime': trackInfo['datetime']})

            positions = []
            for posInfo in newinfo['positions']:
                positions.append(posInfo['value'])

            newinfo['position_avg'] = sum(positions) / len(positions)
            self._tracks[hash] = newinfo

    @abstractmethod
    def save(self):
        pass

    def hashTrack(self, trackInfo:dict):
        data = []
        if trackInfo.get("artist"):
            data.append(trackInfo['artist'].lower())
        data.append(trackInfo["title"].lower())

        hash = zlib.adler32(json.dumps(data).encode('utf8'))
        return hex(hash).lstrip("0x").rstrip("L")