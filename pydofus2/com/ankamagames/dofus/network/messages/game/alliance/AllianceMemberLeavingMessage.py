from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class AllianceMemberLeavingMessage(NetworkMessage):
    kicked: bool
    memberId: int
    def init(self, kicked_: bool, memberId_: int):
        self.kicked = kicked_
        self.memberId = memberId_
        
        super().__init__()
    