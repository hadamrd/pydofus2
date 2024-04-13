from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorMovement import (
        TaxCollectorMovement,
    )


class TaxCollectorMovementsOfflineMessage(NetworkMessage):
    movements: list["TaxCollectorMovement"]

    def init(self, movements_: list["TaxCollectorMovement"]):
        self.movements = movements_

        super().__init__()
