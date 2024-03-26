from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.zaap.TeleportDestinationsMessage import \
    TeleportDestinationsMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.interactive.zaap.TeleportDestination import \
        TeleportDestination


class ZaapDestinationsMessage(TeleportDestinationsMessage):
    spawnMapId: int

    def init(self, spawnMapId_: int, type_: int, destinations_: list["TeleportDestination"]):
        self.spawnMapId = spawnMapId_

        super().init(type_, destinations_)
