import pydofus2.com.ankamagames.dofus.logic.game.common.managers.StorageOptionManager as storageoptmgr
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.Inventory import Inventory


class PlayerInventory(Inventory):
    def __init__(self):
        super().__init__()

    @property
    def kamas(self):
        return self._kamas

    @kamas.setter
    def kamas(self, value: float) -> None:
        if PlayedCharacterManager().characteristics:
            PlayedCharacterManager().characteristics.kamas = value
        self._kamas = value
        storageoptmgr.StorageOptionManager().updateStorageView()
