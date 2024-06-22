from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GroupTeleportPlayerCloseMessage(NetworkMessage):
    mapId: int
    requesterId: int

    def init(self, mapId_: int, requesterId_: int):
        self.mapId = mapId_
        self.requesterId = requesterId_

        super().__init__()
