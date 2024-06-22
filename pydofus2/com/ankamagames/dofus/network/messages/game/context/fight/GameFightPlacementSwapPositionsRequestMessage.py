from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementPositionRequestMessage import (
    GameFightPlacementPositionRequestMessage,
)


class GameFightPlacementSwapPositionsRequestMessage(GameFightPlacementPositionRequestMessage):
    requestedId: int

    def init(self, requestedId_: int, cellId_: int):
        self.requestedId = requestedId_

        super().init(cellId_)
