from pydofus2.com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import (
    AbstractGameActionMessage,
)


class GameActionFightExchangePositionsMessage(AbstractGameActionMessage):
    targetId: int
    casterCellId: int
    targetCellId: int

    def init(self, targetId_: int, casterCellId_: int, targetCellId_: int, actionId_: int, sourceId_: int):
        self.targetId = targetId_
        self.casterCellId = casterCellId_
        self.targetCellId = targetCellId_

        super().init(actionId_, sourceId_)
