from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class MapChangeFailedMessage(NetworkMessage):
    TIMEOUT = 0
    UNREACHABLE_TRANSIT_CELL = 1
    TRANSIT_SKILL_NOTFOUND = 2
    mapId: int
    reason: str
    reasonId: int

    def init(self, mapId, reason="", reasonId=-1):
        self.mapId = mapId
        self.reason = reason
        self.reasonId = reasonId
        super().__init__()
