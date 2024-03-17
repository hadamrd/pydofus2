from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class AgressableStatusMessage(NetworkMessage):
    playerId: int
    enable: int
    roleAvAId: int
    pictoScore: int
    def init(self, playerId_: int, enable_: int, roleAvAId_: int, pictoScore_: int):
        self.playerId = playerId_
        self.enable = enable_
        self.roleAvAId = roleAvAId_
        self.pictoScore = pictoScore_
        
        super().__init__()
    