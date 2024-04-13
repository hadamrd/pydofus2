from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightAIInformations import (
    GameFightAIInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
        EntityDispositionInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameContextBasicSpawnInformation import (
        GameContextBasicSpawnInformation,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacteristics import (
        GameFightCharacteristics,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class GameFightTaxCollectorInformations(GameFightAIInformations):
    firstNameId: int
    lastNameId: int

    def init(
        self,
        firstNameId_: int,
        lastNameId_: int,
        spawnInfo_: "GameContextBasicSpawnInformation",
        wave_: int,
        stats_: "GameFightCharacteristics",
        previousPositions_: list[int],
        look_: "EntityLook",
        contextualId_: int,
        disposition_: "EntityDispositionInformations",
    ):
        self.firstNameId = firstNameId_
        self.lastNameId = lastNameId_

        super().init(spawnInfo_, wave_, stats_, previousPositions_, look_, contextualId_, disposition_)
