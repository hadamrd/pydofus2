from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class SocialFightInfo(NetworkMessage):
    fightId: int
    fightType: int
    mapId: int

    def init(self, fightId_: int, fightType_: int, mapId_: int):
        self.fightId = fightId_
        self.fightType = fightType_
        self.mapId = mapId_

        super().__init__()
