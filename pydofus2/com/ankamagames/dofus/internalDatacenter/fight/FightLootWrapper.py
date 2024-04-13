from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightLoot import FightLoot
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import ObjectEffect
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class FightLootWrapper(IDataCenter):

    objects: list

    kamas: float = 0

    def __init__(self, loot: FightLoot):
        super().__init__()
        self.objects = list()
        for reward in loot.objects:
            self.objects.append(
                ItemWrapper.create(
                    63, 0, reward.objectId, reward.quantity, list[ObjectEffect](), False, reward.priorityHint
                )
            )
        self.kamas = loot.kamas
