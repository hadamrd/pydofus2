from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class EmotePlayAbstractMessage(NetworkMessage):
    emoteId: int
    emoteStartTime: int

    def init(self, emoteId_: int, emoteStartTime_: int):
        self.emoteId = emoteId_
        self.emoteStartTime = emoteStartTime_

        super().__init__()
