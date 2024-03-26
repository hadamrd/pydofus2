from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.surrender.SurrenderResponse import \
        SurrenderResponse
    from pydofus2.com.ankamagames.dofus.network.types.game.surrender.vote.SurrenderVoteResponse import \
        SurrenderVoteResponse


class SurrenderInfoResponseMessage(NetworkMessage):
    hasSanction: bool
    surrenderResponse: "SurrenderResponse"
    surrenderVoteResponse: "SurrenderVoteResponse"

    def init(
        self,
        hasSanction_: bool,
        surrenderResponse_: "SurrenderResponse",
        surrenderVoteResponse_: "SurrenderVoteResponse",
    ):
        self.hasSanction = hasSanction_
        self.surrenderResponse = surrenderResponse_
        self.surrenderVoteResponse = surrenderVoteResponse_

        super().__init__()
