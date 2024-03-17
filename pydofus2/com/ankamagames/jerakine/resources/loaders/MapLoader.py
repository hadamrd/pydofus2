import threading
from functools import lru_cache
from pathlib import Path

from pydofus2.com.ankamagames.dofus import Constants
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.dataAdapter.dlm import DLM

lock = threading.Lock()


class MapLoader:
    DLM_KEY = XmlConfig().getEntry("config.maps.encryptionKey")
    reader = DLM(DLM_KEY)

    @classmethod
    @lru_cache(maxsize=5)
    def load(cls, mapId, key=None):
        with lock:
            if key is not None:
                cls.reader.setKey(key)
            map_p = Path(Constants.MAPS_PATH) / MapLoader.getMapURI(mapId)
            if not map_p.exists():
                raise Exception(f"Map {mapId} not found in path {map_p}")
            with open(map_p, "rb") as f:
                compressedMapBinary = f.read()
                return cls.reader.read(compressedMapBinary)

    @classmethod
    def getMapURI(cls, mapId):
        return f"{int(mapId) % 10}/{int(mapId)}.dlm"
