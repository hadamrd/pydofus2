from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.alliance.application.AlliancePlayerApplicationAbstractMessage import \
    AlliancePlayerApplicationAbstractMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import \
        AllianceInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.social.application.SocialApplicationInformation import \
        SocialApplicationInformation


class AlliancePlayerApplicationInformationMessage(AlliancePlayerApplicationAbstractMessage):
    allianceInformation: "AllianceInformation"
    apply: "SocialApplicationInformation"

    def init(self, allianceInformation_: "AllianceInformation", apply_: "SocialApplicationInformation"):
        self.allianceInformation = allianceInformation_
        self.apply = apply_

        super().init()
