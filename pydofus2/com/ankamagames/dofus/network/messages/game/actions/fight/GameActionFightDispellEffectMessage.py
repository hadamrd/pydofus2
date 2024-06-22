from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightDispellMessage import (
    GameActionFightDispellMessage,
)


class GameActionFightDispellEffectMessage(GameActionFightDispellMessage):
    boostUID: int

    def init(self, boostUID_: int, targetId_: int, verboseCast_: bool, actionId_: int, sourceId_: int):
        self.boostUID = boostUID_

        super().init(targetId_, verboseCast_, actionId_, sourceId_)
