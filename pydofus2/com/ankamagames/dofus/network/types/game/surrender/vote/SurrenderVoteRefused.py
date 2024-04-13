from pydofus2.com.ankamagames.dofus.network.types.game.surrender.vote.SurrenderVoteResponse import (
    SurrenderVoteResponse,
)


class SurrenderVoteRefused(SurrenderVoteResponse):
    def init(self):

        super().init()
