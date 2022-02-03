# SIGNATURE_KEY_DATA = Constants_SIGNATURE_KEY_DATA

import os
from pathlib import Path

from com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from com.ankamagames.jerakine.types.enums.DataStoreEnum import DataStoreEnum


LOG_UPLOAD_MODE = False

EVENT_MODE = False

EVENT_MODE_PARAM = ""

CHARACTER_CREATION_ALLOWED = True

PRE_GAME_MODULE = ["Ankama_Connection"]

COMMON_GAME_MODULE = ["Ankama_Common","Ankama_Config","Ankama_Tooltips","Ankama_Console","Ankama_ContextMenu"]

ADMIN_MODULE = ["Ankama_Admin"]

DETERMINIST_TACKLE = True

DATASTORE_MODULE_DEBUG:DataStoreType = DataStoreType("Dofus_ModuleDebug", True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_COMPUTER)

MAX_LOGIN_ATTEMPTS = 3

ROOTDIR = Path(os.path.dirname(__file__))

MAPS_PATH = "content/maps"

DOFUS_ROOTDIR = Path(r"C:\Users\majdoub\AppData\Local\Ankama\Dofus")

DOFUS_DATA_DIR = DOFUS_ROOTDIR / "data"

DOFUS_COMMON_DIR = DOFUS_DATA_DIR / "common"

DOFUS_LOCAL_DATA_STORE = Path(r"C:\Users\majdoub\AppData\Roaming\Dofus")

DOFUS_CONTENT_DIR = DOFUS_ROOTDIR / "content"

PROTOCOL_SPEC_PATH = ROOTDIR / "network/spec.json"

WORLDGRAPH_PATH = DOFUS_CONTENT_DIR / "maps" / "world-graph.binary"