from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOption import \
    HumanOption

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.look.IndexedEntityLook import \
        IndexedEntityLook


class HumanOptionFollowers(HumanOption):
    followingCharactersLook: list["IndexedEntityLook"]

    def init(self, followingCharactersLook_: list["IndexedEntityLook"]):
        self.followingCharactersLook = followingCharactersLook_

        super().init()
