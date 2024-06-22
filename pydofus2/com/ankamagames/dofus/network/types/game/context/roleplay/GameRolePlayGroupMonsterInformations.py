from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import (
    GameRolePlayActorInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
        EntityDispositionInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GroupMonsterStaticInformations import (
        GroupMonsterStaticInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class GameRolePlayGroupMonsterInformations(GameRolePlayActorInformations):
    staticInfos: "GroupMonsterStaticInformations"
    lootShare: int
    alignmentSide: int
    hasHardcoreDrop: bool

    def init(
        self,
        staticInfos_: "GroupMonsterStaticInformations",
        lootShare_: int,
        alignmentSide_: int,
        hasHardcoreDrop_: bool,
        look_: "EntityLook",
        contextualId_: int,
        disposition_: "EntityDispositionInformations",
    ):
        self.staticInfos = staticInfos_
        self.lootShare = lootShare_
        self.alignmentSide = alignmentSide_
        self.hasHardcoreDrop = hasHardcoreDrop_

        super().init(look_, contextualId_, disposition_)
