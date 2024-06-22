from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class SurrenderVoteEndMessage(NetworkMessage):
    voteResult: bool

    def init(self, voteResult_: bool):
        self.voteResult = voteResult_

        super().__init__()
