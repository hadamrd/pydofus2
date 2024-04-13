from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GroupTeleportPlayerOfferMessage(NetworkMessage):
    mapId: int
    worldX: int
    worldY: int
    timeLeft: int
    requesterId: int
    requesterName: str

    def init(self, mapId_: int, worldX_: int, worldY_: int, timeLeft_: int, requesterId_: int, requesterName_: str):
        self.mapId = mapId_
        self.worldX = worldX_
        self.worldY = worldY_
        self.timeLeft = timeLeft_
        self.requesterId = requesterId_
        self.requesterName = requesterName_

        super().__init__()
