from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import \
    EffectInstance
from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.StorageOptionManager import \
    StorageOptionManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.BankMinoukiView import \
    BankMinoukiView


class BankMinoukiFilteredView(BankMinoukiView):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "bankMinoukiFiltered"

    def isListening(self, item: ItemWrapper) -> bool:
        return (
            super().isListening(item)
            and StorageOptionManager().hasBankFilter()
            and self.hasMinoukiEffect(item, StorageOptionManager().bankFilter)
        )

    def hasMinoukiEffect(self, item: ItemWrapper, filter: int) -> bool:
        effect: EffectInstance = None
        for effect in item.possibleEffects:
            if effect.effectId == ActionIds.ACTION_ITEM_CUSTOM_EFFECT:
                if effect.parameter2 == filter:
                    return True
        return False
