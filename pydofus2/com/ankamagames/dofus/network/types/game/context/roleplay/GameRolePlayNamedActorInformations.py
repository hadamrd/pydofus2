from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import (
    GameRolePlayActorInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
        EntityDispositionInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class GameRolePlayNamedActorInformations(GameRolePlayActorInformations):
    name: str

    def init(self, name_: str, look_: "EntityLook", contextualId_: int, disposition_: "EntityDispositionInformations"):
        self.name = name_

        super().init(look_, contextualId_, disposition_)
