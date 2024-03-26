from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import \
    AbstractGameActionMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
        GameFightFighterInformations


class GameActionFightSummonMessage(AbstractGameActionMessage):
    summons: list["GameFightFighterInformations"]

    def init(self, summons_: list["GameFightFighterInformations"], actionId_: int, sourceId_: int):
        self.summons = summons_

        super().init(actionId_, sourceId_)
