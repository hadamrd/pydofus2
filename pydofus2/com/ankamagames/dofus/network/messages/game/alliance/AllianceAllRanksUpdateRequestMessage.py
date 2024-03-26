from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.rank.RankInformation import \
        RankInformation


class AllianceAllRanksUpdateRequestMessage(NetworkMessage):
    ranks: list["RankInformation"]

    def init(self, ranks_: list["RankInformation"]):
        self.ranks = ranks_

        super().__init__()
