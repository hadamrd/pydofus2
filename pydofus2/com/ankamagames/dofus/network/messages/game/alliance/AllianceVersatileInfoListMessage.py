from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.AllianceVersatileInformations import (
        AllianceVersatileInformations,
    )


class AllianceVersatileInfoListMessage(NetworkMessage):
    alliances: list["AllianceVersatileInformations"]

    def init(self, alliances_: list["AllianceVersatileInformations"]):
        self.alliances = alliances_

        super().__init__()
