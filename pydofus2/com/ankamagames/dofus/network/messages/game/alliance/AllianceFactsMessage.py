from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalSocialPublicInformations import \
        CharacterMinimalSocialPublicInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.social.AllianceFactSheetInformation import \
        AllianceFactSheetInformation
    

class AllianceFactsMessage(NetworkMessage):
    infos: 'AllianceFactSheetInformation'
    members: list['CharacterMinimalSocialPublicInformations']
    controlledSubareaIds: list[int]
    leaderCharacterId: int
    leaderCharacterName: str
    def init(self, infos_: 'AllianceFactSheetInformation', members_: list['CharacterMinimalSocialPublicInformations'], controlledSubareaIds_: list[int], leaderCharacterId_: int, leaderCharacterName_: str):
        self.infos = infos_
        self.members = members_
        self.controlledSubareaIds = controlledSubareaIds_
        self.leaderCharacterId = leaderCharacterId_
        self.leaderCharacterName = leaderCharacterName_
        
        super().__init__()
    