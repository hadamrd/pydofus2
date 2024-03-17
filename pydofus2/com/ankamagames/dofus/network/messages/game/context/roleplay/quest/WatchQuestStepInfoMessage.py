from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.quest.QuestStepInfoMessage import \
    QuestStepInfoMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.quest.QuestActiveInformations import \
        QuestActiveInformations
    

class WatchQuestStepInfoMessage(QuestStepInfoMessage):
    playerId: int
    def init(self, playerId_: int, infos_: 'QuestActiveInformations'):
        self.playerId = playerId_
        
        super().init(infos_)
    