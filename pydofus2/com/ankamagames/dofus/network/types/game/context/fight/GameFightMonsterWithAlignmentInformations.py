from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.alignment.ActorAlignmentInformations import (
        ActorAlignmentInformations,
    )
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


class GameFightMonsterWithAlignmentInformations(GameFightMonsterInformations):
    alignmentInfos: "ActorAlignmentInformations"

    def init(
        self,
        alignmentInfos_: "ActorAlignmentInformations",
        creatureGenericId_: int,
        creatureGrade_: int,
        creatureLevel_: int,
        spawnInfo_: "GameContextBasicSpawnInformation",
        wave_: int,
        stats_: "GameFightCharacteristics",
        previousPositions_: list[int],
        look_: "EntityLook",
        contextualId_: int,
        disposition_: "EntityDispositionInformations",
    ):
        self.alignmentInfos = alignmentInfos_

        super().init(
            creatureGenericId_,
            creatureGrade_,
            creatureLevel_,
            spawnInfo_,
            wave_,
            stats_,
            previousPositions_,
            look_,
            contextualId_,
            disposition_,
        )
