from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialMember import \
    SocialMember

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.guild.note.PlayerNote import \
        PlayerNote
    from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
        PlayerStatus
    

class GuildMemberInfo(SocialMember):
    givenExperience: int
    experienceGivenPercent: int
    alignmentSide: int
    moodSmileyId: int
    achievementPoints: int
    havenBagShared: bool
    note: 'PlayerNote'
    def init(self, givenExperience_: int, experienceGivenPercent_: int, alignmentSide_: int, moodSmileyId_: int, achievementPoints_: int, havenBagShared_: bool, note_: 'PlayerNote', breed_: int, sex_: bool, connected_: int, hoursSinceLastConnection_: int, accountId_: int, status_: 'PlayerStatus', rankId_: int, enrollmentDate_: int, level_: int, name_: str, id_: int):
        self.givenExperience = givenExperience_
        self.experienceGivenPercent = experienceGivenPercent_
        self.alignmentSide = alignmentSide_
        self.moodSmileyId = moodSmileyId_
        self.achievementPoints = achievementPoints_
        self.havenBagShared = havenBagShared_
        self.note = note_
        
        super().init(breed_, sex_, connected_, hoursSinceLastConnection_, accountId_, status_, rankId_, enrollmentDate_, level_, name_, id_)
    