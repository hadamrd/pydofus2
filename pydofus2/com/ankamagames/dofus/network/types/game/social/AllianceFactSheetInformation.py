from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import \
    AllianceInformation

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.alliance.recruitment.AllianceRecruitmentInformation import \
        AllianceRecruitmentInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem


class AllianceFactSheetInformation(AllianceInformation):
    creationDate: int
    nbMembers: int
    nbSubarea: int
    nbTaxCollectors: int
    recruitment: "AllianceRecruitmentInformation"

    def init(
        self,
        creationDate_: int,
        nbMembers_: int,
        nbSubarea_: int,
        nbTaxCollectors_: int,
        recruitment_: "AllianceRecruitmentInformation",
        allianceEmblem_: "SocialEmblem",
        allianceName_: str,
        allianceId_: int,
        allianceTag_: str,
    ):
        self.creationDate = creationDate_
        self.nbMembers = nbMembers_
        self.nbSubarea = nbSubarea_
        self.nbTaxCollectors = nbTaxCollectors_
        self.recruitment = recruitment_

        super().init(allianceEmblem_, allianceName_, allianceId_, allianceTag_)
