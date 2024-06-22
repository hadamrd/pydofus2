from pydofus2.com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import (
    AbstractGameActionMessage,
)


class GameActionFightDispellMessage(AbstractGameActionMessage):
    targetId: int
    verboseCast: bool

    def init(self, targetId_: int, verboseCast_: bool, actionId_: int, sourceId_: int):
        self.targetId = targetId_
        self.verboseCast = verboseCast_

        super().init(actionId_, sourceId_)
