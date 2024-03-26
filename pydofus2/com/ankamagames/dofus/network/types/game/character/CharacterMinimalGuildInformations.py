from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import \
    CharacterMinimalPlusLookInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicGuildInformations import \
        BasicGuildInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook


class CharacterMinimalGuildInformations(CharacterMinimalPlusLookInformations):
    guild: "BasicGuildInformations"

    def init(
        self,
        guild_: "BasicGuildInformations",
        entityLook_: "EntityLook",
        breed_: int,
        level_: int,
        name_: str,
        id_: int,
    ):
        self.guild = guild_

        super().init(entityLook_, breed_, level_, name_, id_)
