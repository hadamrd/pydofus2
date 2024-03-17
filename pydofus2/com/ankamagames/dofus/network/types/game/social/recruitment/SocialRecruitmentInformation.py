from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class SocialRecruitmentInformation(NetworkMessage):
    socialId: int
    recruitmentType: int
    recruitmentTitle: str
    recruitmentText: str
    selectedLanguages: list[int]
    selectedCriterion: list[int]
    minLevel: int
    lastEditPlayerName: str
    lastEditDate: int
    minLevelFacultative: bool
    invalidatedByModeration: bool
    recruitmentAutoLocked: bool
    minLevelFacultative: bool
    invalidatedByModeration: bool
    recruitmentAutoLocked: bool
    def init(self, socialId_: int, recruitmentType_: int, recruitmentTitle_: str, recruitmentText_: str, selectedLanguages_: list[int], selectedCriterion_: list[int], minLevel_: int, lastEditPlayerName_: str, lastEditDate_: int, minLevelFacultative_: bool, invalidatedByModeration_: bool, recruitmentAutoLocked_: bool):
        self.socialId = socialId_
        self.recruitmentType = recruitmentType_
        self.recruitmentTitle = recruitmentTitle_
        self.recruitmentText = recruitmentText_
        self.selectedLanguages = selectedLanguages_
        self.selectedCriterion = selectedCriterion_
        self.minLevel = minLevel_
        self.lastEditPlayerName = lastEditPlayerName_
        self.lastEditDate = lastEditDate_
        self.minLevelFacultative = minLevelFacultative_
        self.invalidatedByModeration = invalidatedByModeration_
        self.recruitmentAutoLocked = recruitmentAutoLocked_
        
        super().__init__()
    