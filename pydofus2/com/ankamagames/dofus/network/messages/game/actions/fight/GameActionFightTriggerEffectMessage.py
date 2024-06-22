from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightDispellEffectMessage import (
    GameActionFightDispellEffectMessage,
)


class GameActionFightTriggerEffectMessage(GameActionFightDispellEffectMessage):
    def init(self, boostUID_: int, targetId_: int, verboseCast_: bool, actionId_: int, sourceId_: int):

        super().init(boostUID_, targetId_, verboseCast_, actionId_, sourceId_)
