from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicNamedAllianceInformations import (
    BasicNamedAllianceInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import SocialEmblem


class AllianceInformation(BasicNamedAllianceInformations):
    allianceEmblem: "SocialEmblem"

    def init(self, allianceEmblem_: "SocialEmblem", allianceName_: str, allianceId_: int, allianceTag_: str):
        self.allianceEmblem = allianceEmblem_

        super().init(allianceName_, allianceId_, allianceTag_)
