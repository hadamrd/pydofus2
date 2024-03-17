from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayNpcInformations import \
    GameRolePlayNpcInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import \
        EntityDispositionInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.quest.GameRolePlayNpcQuestFlag import \
        GameRolePlayNpcQuestFlag
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    

class GameRolePlayNpcWithQuestInformations(GameRolePlayNpcInformations):
    questFlag: 'GameRolePlayNpcQuestFlag'
    def init(self, questFlag_: 'GameRolePlayNpcQuestFlag', npcId_: int, sex_: bool, specialArtworkId_: int, look_: 'EntityLook', contextualId_: int, disposition_: 'EntityDispositionInformations'):
        self.questFlag = questFlag_
        
        super().init(npcId_, sex_, specialArtworkId_, look_, contextualId_, disposition_)
    