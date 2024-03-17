import os
from pathlib import Path

from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import \
    ByteArray
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.DataStoreEnum import \
    DataStoreEnum
from pydofus2.com.hurlan.crypto.SignatureKey import SignatureKey

LOG_UPLOAD_MODE = False

EVENT_MODE = False

EVENT_MODE_PARAM = ""

CHARACTER_CREATION_ALLOWED = True

PRE_GAME_MODULE = ["Ankama_Connection"]

COMMON_GAME_MODULE = [
    "Ankama_Common",
    "Ankama_Config",
    "Ankama_Tooltips",
    "Ankama_Console",
    "Ankama_ContextMenu",
]

ADMIN_MODULE = ["Ankama_Admin"]

DETERMINIST_TACKLE = True

DATASTORE_MODULE_DEBUG = DataStoreType(
    "Dofus_ModuleDebug", True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_COMPUTER
)

DATASTORE_LANG_VERSION = DataStoreType(
    "lastLangVersion", True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_ACCOUNT
)

DATASTORE_COMPUTER_OPTIONS = DataStoreType(
    "Dofus_ComputerOptions",
    True,
    DataStoreEnum.LOCATION_LOCAL,
    DataStoreEnum.BIND_ACCOUNT,
)

MAX_LOGIN_ATTEMPTS = 3

ROOTDIR = Path(os.path.dirname(__file__))

DOFUS_ROOTDIR = Path("D:/Dofus")

LOGS_DIR = Path("D:/botdev/logs")

MAPS_PATH = Path(os.getenv("APPDATA")) / "pydofus2" / "content" / "maps"

AVERAGE_PRICES_PATH = Path(os.getenv("APPDATA")) / "pydofus2" / "content" / "average_prices.json"

PROTOCOL_SPEC_PATH = ROOTDIR.parent / "jerakine" / "network" / "parser" / "D2protocol.json"

PROTOCOL_MSG_SHUFFLE_PATH = ROOTDIR / "network" / "MsgShuffle.json"

GAME_VERSION_PATH = DOFUS_ROOTDIR / "VERSION"

BINARY_DATA_DIR = ROOTDIR.parent.parent.parent / "binaryData"

with open(
    BINARY_DATA_DIR
    / "13_com.ankamagames.dofus.Constants_SIGNATURE_KEY_DATA_com.ankamagames.dofus.Constants_SIGNATURE_KEY_DATA.bin",
    "rb",
) as fs:
    SIGNATURE_KEY_DATA = SignatureKey.import_key(ByteArray(fs.read()))
