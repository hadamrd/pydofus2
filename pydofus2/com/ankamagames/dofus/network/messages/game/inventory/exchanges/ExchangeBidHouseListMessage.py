from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ExchangeBidHouseListMessage(NetworkMessage):
    objectGID: int
    follow: bool

    def init(self, objectGID_: int, follow_: bool):
        self.objectGID = objectGID_
        self.follow = follow_

        super().__init__()
