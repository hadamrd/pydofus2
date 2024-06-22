from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.choice.CharacterBaseInformations import (
    CharacterBaseInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.entity.PartyEntityBaseInformation import (
        PartyEntityBaseInformation,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class PartyInvitationMemberInformations(CharacterBaseInformations):
    worldX: int
    worldY: int
    mapId: int
    subAreaId: int
    entities: list["PartyEntityBaseInformation"]

    def init(
        self,
        worldX_: int,
        worldY_: int,
        mapId_: int,
        subAreaId_: int,
        entities_: list["PartyEntityBaseInformation"],
        sex_: bool,
        entityLook_: "EntityLook",
        breed_: int,
        level_: int,
        name_: str,
        id_: int,
    ):
        self.worldX = worldX_
        self.worldY = worldY_
        self.mapId = mapId_
        self.subAreaId = subAreaId_
        self.entities = entities_

        super().init(sex_, entityLook_, breed_, level_, name_, id_)
