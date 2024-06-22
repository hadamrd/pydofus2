from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class UpdatedStorageTabInformation(NetworkMessage):
    name: str
    tabNumber: int
    picto: int
    dropTypeLimitation: list[int]

    def init(self, name_: str, tabNumber_: int, picto_: int, dropTypeLimitation_: list[int]):
        self.name = name_
        self.tabNumber = tabNumber_
        self.picto = picto_
        self.dropTypeLimitation = dropTypeLimitation_

        super().__init__()
