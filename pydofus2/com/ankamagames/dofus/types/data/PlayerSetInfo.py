from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import \
    EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemSet import ItemSet
from pydofus2.com.ankamagames.dofus.misc.ObjectEffectAdapter import \
    ObjectEffectAdapter
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import \
    ObjectEffect


class PlayerSetInfo:

    setId: int = 0

    setName: str

    allItems: list[int]

    setObjects: list[int]

    setEffects: list[EffectInstance]

    def __init__(self, id: int, items: list[int], effects: list[ObjectEffect]):
        self.setObjects = list[int]()
        super().__init__()
        itemSet: ItemSet = ItemSet.getItemSetById(id)
        self.setName = itemSet.name
        self.allItems = itemSet.items
        self.setId = id
        self.setObjects = items
        nEffect: int = len(effects)
        self.setEffects = list[EffectInstance]([None] * nEffect)
        for i in range(nEffect):
            self.setEffects[i] = ObjectEffectAdapter.fromNetwork(effects[i])
