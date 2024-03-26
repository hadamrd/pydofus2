from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import \
    CharacterMinimalPlusLookInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook


class CharacterBaseInformations(CharacterMinimalPlusLookInformations):
    sex: bool

    def init(self, sex_: bool, entityLook_: "EntityLook", breed_: int, level_: int, name_: str, id_: int):
        self.sex = sex_

        super().init(entityLook_, breed_, level_, name_, id_)
