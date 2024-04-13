from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class StorageTabInformation(NetworkMessage):
    name: str
    tabNumber: int
    picto: int
    openRight: int
    dropRight: int
    takeRight: int
    dropTypeLimitation: list[int]

    def init(
        self,
        name_: str,
        tabNumber_: int,
        picto_: int,
        openRight_: int,
        dropRight_: int,
        takeRight_: int,
        dropTypeLimitation_: list[int],
    ):
        self.name = name_
        self.tabNumber = tabNumber_
        self.picto = picto_
        self.openRight = openRight_
        self.dropRight = dropRight_
        self.takeRight = takeRight_
        self.dropTypeLimitation = dropTypeLimitation_

        super().__init__()
