from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.quest.QuestListMessage import \
    QuestListMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.quest.QuestActiveInformations import \
        QuestActiveInformations
    

class WatchQuestListMessage(QuestListMessage):
    playerId: int
    def init(self, playerId_: int, finishedQuestsIds_: list[int], finishedQuestsCounts_: list[int], activeQuests_: list['QuestActiveInformations'], reinitDoneQuestsIds_: list[int]):
        self.playerId = playerId_
        
        super().init(finishedQuestsIds_, finishedQuestsCounts_, activeQuests_, reinitDoneQuestsIds_)
    