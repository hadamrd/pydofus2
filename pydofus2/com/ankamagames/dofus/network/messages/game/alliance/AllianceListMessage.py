from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.AllianceFactSheetInformation import (
        AllianceFactSheetInformation,
    )


class AllianceListMessage(NetworkMessage):
    alliances: list["AllianceFactSheetInformation"]

    def init(self, alliances_: list["AllianceFactSheetInformation"]):
        self.alliances = alliances_

        super().__init__()
