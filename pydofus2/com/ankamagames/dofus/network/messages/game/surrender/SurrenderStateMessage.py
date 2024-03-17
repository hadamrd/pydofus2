from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class SurrenderStateMessage(NetworkMessage):
    canSurrender: bool
    permitVote: bool
    canSurrender: bool
    permitVote: bool
    def init(self, canSurrender_: bool, permitVote_: bool):
        self.canSurrender = canSurrender_
        self.permitVote = permitVote_
        
        super().__init__()
    