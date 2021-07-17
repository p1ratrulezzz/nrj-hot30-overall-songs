from src.storage.storage import Storage
import os
import json
from datetime import datetime, timezone

class JsonStorage(Storage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "filename" not in self._options:
            raise RuntimeError("Filename option must be set")

        self.readTracks()

    def _getFilename(self):
        return self._options['filename']

    def readTracks(self):
        if os.path.exists(self._getFilename()):
            with open(self._getFilename(), 'r') as fp:
                data = json.load(fp)
                if data.get('tracks'):
                    self._tracks = data['tracks']
                fp.close()

    def save(self):
        json_data = {
            'updated': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'tracks': self._tracks,
        }

        with open(self._getFilename(), 'w') as fp:
            fp.write(json.dumps(json_data, indent=True))
            fp.close()

