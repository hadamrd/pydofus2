import json
import os
from pathlib import Path

from pydofus2.Zaap.ZaapDecoy import ZaapDecoy
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
APPDATA_DIR = Path(os.getenv("APPDATA"))
PYDOFUS2_APPDIR = APPDATA_DIR / "pydofus2"

# If the directory does not exist, create it
if not PYDOFUS2_APPDIR.exists():
    PYDOFUS2_APPDIR.mkdir()

SETTINGS_DIR = PYDOFUS2_APPDIR / "settings.json"

# check if settings file exists
if not SETTINGS_DIR.exists():
    with open(SETTINGS_DIR, "w") as fs:
        json.dump({}, fs)

with open(SETTINGS_DIR, "r") as fs:
    USER_SETTINGS = json.load(fs)

DOFUS_HOME = ZaapDecoy.get_dofus_location()
if not DOFUS_HOME:
    DOFUS_HOME = Path(USER_SETTINGS.get("DOFUS_HOME")) if USER_SETTINGS.get("DOFUS_HOME") else None
    if not DOFUS_HOME:
        DOFUS_HOME = Path(os.getenv("DOFUS_HOME")) if os.getenv("DOFUS_HOME") else None
        if not DOFUS_HOME:
            raise Exception("DOFUS_HOME not found in ZAAP settings, PYDOFUS2 USER settings and not found in environment variables!")
    
    
LOGS_DIR = USER_SETTINGS.get("LOGS_DIR")    
if not LOGS_DIR:
    LOGS_DIR = Path(os.getenv("LOGS_DIR")) if os.getenv("LOGS_DIR") else None
    if not LOGS_DIR:
        LOGS_DIR = PYDOFUS2_APPDIR / "Logs"

MAPS_PATH = PYDOFUS2_APPDIR / "content" / "maps"

AVERAGE_PRICES_PATH = PYDOFUS2_APPDIR / "content" / "average_prices.json"

PROTOCOL_SPEC_PATH = ROOTDIR.parent / "jerakine" / "network" / "parser" / "D2protocol.json"

PROTOCOL_MSG_SHUFFLE_PATH = ROOTDIR / "network" / "MsgShuffle.json"

GAME_VERSION_PATH = DOFUS_HOME / "VERSION"

BINARY_DATA_DIR = ROOTDIR.parent.parent.parent / "binaryData"

with open(
    BINARY_DATA_DIR
    / "13_com.ankamagames.dofus.Constants_SIGNATURE_KEY_DATA_com.ankamagames.dofus.Constants_SIGNATURE_KEY_DATA.bin",
    "rb",
) as fs:
    SIGNATURE_KEY_DATA = SignatureKey.import_key(ByteArray(fs.read()))
