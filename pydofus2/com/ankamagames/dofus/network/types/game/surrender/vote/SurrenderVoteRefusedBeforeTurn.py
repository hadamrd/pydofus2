from pydofus2.com.ankamagames.dofus.network.types.game.surrender.vote.SurrenderVoteRefused import SurrenderVoteRefused


class SurrenderVoteRefusedBeforeTurn(SurrenderVoteRefused):
    minTurnForSurrenderVote: int

    def init(self, minTurnForSurrenderVote_: int):
        self.minTurnForSurrenderVote = minTurnForSurrenderVote_

        super().init()
