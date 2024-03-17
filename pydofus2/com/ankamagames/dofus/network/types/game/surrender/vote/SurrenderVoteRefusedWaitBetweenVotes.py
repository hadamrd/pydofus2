from pydofus2.com.ankamagames.dofus.network.types.game.surrender.vote.SurrenderVoteRefused import \
    SurrenderVoteRefused


class SurrenderVoteRefusedWaitBetweenVotes(SurrenderVoteRefused):
    nextVoteTimestamp: int
    def init(self, nextVoteTimestamp_: int):
        self.nextVoteTimestamp = nextVoteTimestamp_
        
        super().init()
    