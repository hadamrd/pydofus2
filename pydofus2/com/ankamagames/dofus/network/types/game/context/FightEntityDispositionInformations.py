from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
    EntityDispositionInformations,
)


class FightEntityDispositionInformations(EntityDispositionInformations):
    carryingCharacterId: int

    def init(self, carryingCharacterId_: int, cellId_: int, direction_: int):
        self.carryingCharacterId = carryingCharacterId_

        super().init(cellId_, direction_)
