from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class AllianceSubmitApplicationMessage(NetworkMessage):
    applyText: str
    allianceId: int
    def init(self, applyText_: str, allianceId_: int):
        self.applyText = applyText_
        self.allianceId = allianceId_
        
        super().__init__()
    