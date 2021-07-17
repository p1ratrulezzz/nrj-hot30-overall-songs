from abc import ABC, abstractmethod
import re

class Parser(ABC):
    @abstractmethod
    def parseTracks(self):
        pass

    def clearTrackName(self, trackName:str):
        trackName.strip("\r\n\t ")
        trackName = re.sub("[\u2013\u2014\u2015\u2012\u2E3B\u2E3A]+", "-", trackName, flags=re.IGNORECASE|re.UNICODE)
        trackName = re.sub("\s+", " ", trackName, flags=re.IGNORECASE|re.UNICODE)
        return trackName

    def parseTrackName(self, trackName:str):
        info = {"title": trackName}
        dashPos = trackName.rfind("-")
        if dashPos != -1:
            info["artist"] = trackName[:dashPos].strip("\r\n\t ")
            info["title"] = trackName[dashPos+1:].strip("\r\n\t ")
        return info