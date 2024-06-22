from pydofus2.com.ankamagames.dofus.network.types.game.social.recruitment.SocialRecruitmentInformation import (
    SocialRecruitmentInformation,
)


class AllianceRecruitmentInformation(SocialRecruitmentInformation):
    def init(
        self,
        socialId_: int,
        recruitmentType_: int,
        recruitmentTitle_: str,
        recruitmentText_: str,
        selectedLanguages_: list[int],
        selectedCriterion_: list[int],
        minLevel_: int,
        lastEditPlayerName_: str,
        lastEditDate_: int,
        minLevelFacultative_: bool,
        invalidatedByModeration_: bool,
        recruitmentAutoLocked_: bool,
    ):

        super().init(
            socialId_,
            recruitmentType_,
            recruitmentTitle_,
            recruitmentText_,
            selectedLanguages_,
            selectedCriterion_,
            minLevel_,
            lastEditPlayerName_,
            lastEditDate_,
            minLevelFacultative_,
            invalidatedByModeration_,
            recruitmentAutoLocked_,
        )
