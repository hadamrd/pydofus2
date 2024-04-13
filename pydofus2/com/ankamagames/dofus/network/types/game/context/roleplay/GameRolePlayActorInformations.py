from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import (
    GameContextActorInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
        EntityDispositionInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class GameRolePlayActorInformations(GameContextActorInformations):
    def init(self, look_: "EntityLook", contextualId_: int, disposition_: "EntityDispositionInformations"):

        super().init(look_, contextualId_, disposition_)
