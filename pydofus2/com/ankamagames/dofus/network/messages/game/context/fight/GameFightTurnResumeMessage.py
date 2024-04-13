from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnStartMessage import (
    GameFightTurnStartMessage,
)


class GameFightTurnResumeMessage(GameFightTurnStartMessage):
    remainingTime: int

    def init(self, remainingTime_: int, id_: int, waitTime_: int):
        self.remainingTime = remainingTime_

        super().init(id_, waitTime_)
