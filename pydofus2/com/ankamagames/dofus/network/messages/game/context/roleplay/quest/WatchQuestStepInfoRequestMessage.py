from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.quest.QuestStepInfoRequestMessage import (
    QuestStepInfoRequestMessage,
)


class WatchQuestStepInfoRequestMessage(QuestStepInfoRequestMessage):
    playerId: int

    def init(self, playerId_: int, questId_: int):
        self.playerId = playerId_

        super().init(questId_)
