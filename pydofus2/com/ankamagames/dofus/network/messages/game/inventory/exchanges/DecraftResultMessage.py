from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.DecraftedItemStackInfo import (
        DecraftedItemStackInfo,
    )


class DecraftResultMessage(NetworkMessage):
    results: list["DecraftedItemStackInfo"]

    def init(self, results_: list["DecraftedItemStackInfo"]):
        self.results = results_

        super().__init__()
