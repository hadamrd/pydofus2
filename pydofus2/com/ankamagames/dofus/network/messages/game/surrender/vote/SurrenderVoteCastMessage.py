from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class SurrenderVoteCastMessage(NetworkMessage):
    vote: bool
    def init(self, vote_: bool):
        self.vote = vote_
        
        super().__init__()
    