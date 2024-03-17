from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.ObjectItemInRolePlay import \
    ObjectItemInRolePlay

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.mount.ItemDurability import \
        ItemDurability
    

class PaddockItem(ObjectItemInRolePlay):
    durability: 'ItemDurability'
    def init(self, durability_: 'ItemDurability', cellId_: int, objectGID_: int):
        self.durability = durability_
        
        super().init(cellId_, objectGID_)
    