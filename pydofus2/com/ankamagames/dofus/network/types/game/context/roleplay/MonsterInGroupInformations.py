from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupLightInformations import (
    MonsterInGroupLightInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class MonsterInGroupInformations(MonsterInGroupLightInformations):
    look: "EntityLook"

    def init(self, look_: "EntityLook", genericId_: int, grade_: int, level_: int):
        self.look = look_

        super().init(genericId_, grade_, level_)
