from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import (
    CharacterMinimalInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class CharacterMinimalPlusLookInformations(CharacterMinimalInformations):
    entityLook: "EntityLook"
    breed: int

    def init(self, entityLook_: "EntityLook", breed_: int, level_: int, name_: str, id_: int):
        self.entityLook = entityLook_
        self.breed = breed_

        super().init(level_, name_, id_)
