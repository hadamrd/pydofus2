from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.rank.RankInformation import RankInformation


class AllianceRankUpdateRequestMessage(NetworkMessage):
    rank: "RankInformation"

    def init(self, rank_: "RankInformation"):
        self.rank = rank_

        super().__init__()
