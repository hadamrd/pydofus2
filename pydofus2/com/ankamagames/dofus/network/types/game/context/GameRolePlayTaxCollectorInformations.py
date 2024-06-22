from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import (
    GameRolePlayActorInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
        EntityDispositionInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.TaxCollectorStaticInformations import (
        TaxCollectorStaticInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class GameRolePlayTaxCollectorInformations(GameRolePlayActorInformations):
    identification: "TaxCollectorStaticInformations"
    taxCollectorAttack: int

    def init(
        self,
        identification_: "TaxCollectorStaticInformations",
        taxCollectorAttack_: int,
        look_: "EntityLook",
        contextualId_: int,
        disposition_: "EntityDispositionInformations",
    ):
        self.identification = identification_
        self.taxCollectorAttack = taxCollectorAttack_

        super().init(look_, contextualId_, disposition_)
