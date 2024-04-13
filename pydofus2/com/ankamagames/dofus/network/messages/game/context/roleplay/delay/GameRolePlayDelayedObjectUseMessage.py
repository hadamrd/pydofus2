from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.delay.GameRolePlayDelayedActionMessage import (
    GameRolePlayDelayedActionMessage,
)


class GameRolePlayDelayedObjectUseMessage(GameRolePlayDelayedActionMessage):
    objectGID: int

    def init(self, objectGID_: int, delayedCharacterId_: int, delayTypeId_: int, delayEndTime_: int):
        self.objectGID = objectGID_

        super().init(delayedCharacterId_, delayTypeId_, delayEndTime_)
