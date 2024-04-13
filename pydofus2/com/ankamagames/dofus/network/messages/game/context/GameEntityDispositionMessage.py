from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.IdentifiedEntityDispositionInformations import (
        IdentifiedEntityDispositionInformations,
    )


class GameEntityDispositionMessage(NetworkMessage):
    disposition: "IdentifiedEntityDispositionInformations"

    def init(self, disposition_: "IdentifiedEntityDispositionInformations"):
        self.disposition = disposition_

        super().__init__()
