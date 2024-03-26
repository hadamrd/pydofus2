from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import \
    AbstractGameActionMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.GameActionMark import \
        GameActionMark


class GameActionFightMarkCellsMessage(AbstractGameActionMessage):
    mark: "GameActionMark"

    def init(self, mark_: "GameActionMark", actionId_: int, sourceId_: int):
        self.mark = mark_

        super().init(actionId_, sourceId_)
