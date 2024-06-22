from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class StartExchangeTaxCollectorEquipmentMessage(NetworkMessage):
    uid: int

    def init(self, uid_: int):
        self.uid = uid_

        super().__init__()
