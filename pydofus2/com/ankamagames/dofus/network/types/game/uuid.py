from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class Uuid(NetworkMessage):
    uuidString: str

    def init(self, uuidString_: str):
        self.uuidString = uuidString_

        super().__init__()
