import json

import pydofus2.com.ankamagames.dofus.settings as settings


class Metadata:
    with open(settings.PROTOCOL_SPEC_PATH, "r") as fp:
        D2PROTOCOL = json.load(fp)
    PROTOCOL_BUILD: str = D2PROTOCOL["version"]
    PROTOCOL_DATE: str = D2PROTOCOL["date"]

    def __init__(self):
        super().__init__()
