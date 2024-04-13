from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class TeleportPlayerOfferMessage(NetworkMessage):
    mapId: int
    message: str
    timeLeft: int
    requesterId: int

    def init(self, mapId_: int, message_: str, timeLeft_: int, requesterId_: int):
        self.mapId = mapId_
        self.message = message_
        self.timeLeft = timeLeft_
        self.requesterId = requesterId_

        super().__init__()
