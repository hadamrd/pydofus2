from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import \
    CharacterMinimalInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.guild.note.PlayerNote import \
        PlayerNote
    from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
        PlayerStatus


class GuildMember(CharacterMinimalInformations):
    breed: int
    rankId: int
    enrollmentDate: int
    givenExperience: int
    experienceGivenPercent: int
    connected: int
    alignmentSide: int
    hoursSinceLastConnection: int
    moodSmileyId: int
    accountId: int
    achievementPoints: int
    status: "PlayerStatus"
    note: "PlayerNote"
    sex: bool
    havenBagShared: bool
    sex: bool
    havenBagShared: bool

    def init(
        self,
        breed_: int,
        rankId_: int,
        enrollmentDate_: int,
        givenExperience_: int,
        experienceGivenPercent_: int,
        connected_: int,
        alignmentSide_: int,
        hoursSinceLastConnection_: int,
        moodSmileyId_: int,
        accountId_: int,
        achievementPoints_: int,
        status_: "PlayerStatus",
        note_: "PlayerNote",
        sex_: bool,
        havenBagShared_: bool,
        level_: int,
        name_: str,
        id_: int,
    ):
        self.breed = breed_
        self.rankId = rankId_
        self.enrollmentDate = enrollmentDate_
        self.givenExperience = givenExperience_
        self.experienceGivenPercent = experienceGivenPercent_
        self.connected = connected_
        self.alignmentSide = alignmentSide_
        self.hoursSinceLastConnection = hoursSinceLastConnection_
        self.moodSmileyId = moodSmileyId_
        self.accountId = accountId_
        self.achievementPoints = achievementPoints_
        self.status = status_
        self.note = note_
        self.sex = sex_
        self.havenBagShared = havenBagShared_

        super().init(level_, name_, id_)
