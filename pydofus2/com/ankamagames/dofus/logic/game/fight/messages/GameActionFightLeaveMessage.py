from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightDeathMessage import (
    GameActionFightDeathMessage,
)
from pydofus2.com.ankamagames.jerakine.messages.Message import Message


class GameActionFightLeaveMessage(GameActionFightDeathMessage, Message):
    def __init__(self):
        super().__init__()

    def init(self, actionId: int = 0, sourceId: float = 0, targetId: float = 0) -> "GameActionFightLeaveMessage":
        super().init(actionId, sourceId, targetId)
        return self
