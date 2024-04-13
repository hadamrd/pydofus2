from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.alliance.AllianceListMessage import AllianceListMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.AllianceFactSheetInformation import (
        AllianceFactSheetInformation,
    )


class AlliancePartialListMessage(AllianceListMessage):
    def init(self, alliances_: list["AllianceFactSheetInformation"]):

        super().init(alliances_)
