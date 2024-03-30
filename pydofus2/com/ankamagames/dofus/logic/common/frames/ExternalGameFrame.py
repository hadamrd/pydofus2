

from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import InventoryManager
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.storage.StorageKamasUpdateMessage import StorageKamasUpdateMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class ExternalGameFrame(Frame):

    def __init__(self) -> None:
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def pulled(self) -> bool:
        return True

    def process(self, msg):
        
        if isinstance(msg, StorageKamasUpdateMessage):
            InventoryManager().bankInventory.kamas = msg.kamasTotal
            KernelEventsManager().send(KernelEvent.StorageKamasUpdate, msg.kamasTotal)
            KernelEventsManager().send(KernelEvent.DofusBakKamasAmount, msg.kamasTotal + InventoryManager().inventory.kamas)
            return True
