from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import \
    InventoryManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.actions.DeleteObjectAction import \
    DeleteObjectAction
from pydofus2.com.ankamagames.dofus.network.enums.CharacterInventoryPositionEnum import \
    CharacterInventoryPositionEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.InventoryContentMessage import \
    InventoryContentMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.InventoryWeightMessage import \
    InventoryWeightMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectAddedMessage import \
    ObjectAddedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectDeletedMessage import \
    ObjectDeletedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectDeleteMessage import \
    ObjectDeleteMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectDropMessage import \
    ObjectDropMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectModifiedMessage import \
    ObjectModifiedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectMovementMessage import \
    ObjectMovementMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectQuantityMessage import \
    ObjectQuantityMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectsAddedMessage import \
    ObjectsAddedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectsDeletedMessage import \
    ObjectsDeletedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectsQuantityMessage import \
    ObjectsQuantityMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectUseMessage import \
    ObjectUseMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ObjectUseMultipleMessage import \
    ObjectUseMultipleMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.WatchInventoryContentMessage import \
    WatchInventoryContentMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.KamasUpdateMessage import \
    KamasUpdateMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class InventoryManagementFrame(Frame):

    CHARACTER_BUILD_PRESET_TYPE: int = 1

    IDOLS_PRESET_TYPE: int = 2

    FORGETTABLE_PRESET_TYPE: int = 3

    POPUP_WARNING_TIPS_ID: int = 15

    _dataStoreType: DataStoreType

    popupSaveKeyClassic: str = "prevention-phishing"

    _objectUIDToDrop: int

    _objectGIDToDrop: int

    _quantityToDrop: int

    _dropPopup: str

    _currentPointUseUIDObject: int

    _movingObjectUID: int

    _movingObjectPreviousPosition: int

    _objectPositionModification: bool

    _presetTypeIdByPresetId: dict

    _chatText: str

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        InventoryManager().init()
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, WatchInventoryContentMessage):
            InventoryManager().init()
            InventoryManager().inventory.initializeFromObjectItems(msg.objects)
            InventoryManager().inventory.kamas = msg.kamas
            return True

        if type(msg) is InventoryContentMessage:
            Logger().debug("Inventory content received")
            InventoryManager().inventory.initializeFromObjectItems(msg.objects)
            InventoryManager().inventory.kamas = msg.kamas
            Logger().debug(f"Player inventgory Kamas: {msg.kamas}")
            KernelEventsManager().send(KernelEvent.KamasUpdate, msg.kamas)
            equipmentView = InventoryManager().inventory.getView("equipment")
            if equipmentView and equipmentView.content:
                if (
                    equipmentView.content[CharacterInventoryPositionEnum.ACCESSORY_POSITION_PETS]
                    and equipmentView.content[CharacterInventoryPositionEnum.ACCESSORY_POSITION_PETS].typeId
                    == DataEnum.ITEM_TYPE_PETSMOUNT
                ):
                    PlayedCharacterManager().isPetsMounting = True
                    PlayedCharacterManager().petsMount = equipmentView.content[
                        CharacterInventoryPositionEnum.ACCESSORY_POSITION_PETS
                    ]
                if equipmentView.content[CharacterInventoryPositionEnum.INVENTORY_POSITION_ENTITY]:
                    PlayedCharacterManager().hasCompanion = True
            playerCharacterManager = PlayedCharacterManager()
            playerCharacterManager.inventory = InventoryManager().realInventory
            if playerCharacterManager.characteristics:
                playerCharacterManager.characteristics.kamas = msg.kamas
            KernelEventsManager().send(KernelEvent.InventoryContent, msg.objects, msg.kamas)
            return True

        if isinstance(msg, ObjectAddedMessage):
            iw = InventoryManager().inventory.addObjectItem(msg.object)
            Logger().debug(f"Added object {iw.objectGID} x {iw.quantity}")
            KernelEventsManager().send(KernelEvent.ObjectAdded, iw)
            return True

        if isinstance(msg, ObjectsAddedMessage):
            for osait in msg.object:
                iw = InventoryManager().inventory.addObjectItem(osait)
                KernelEventsManager().send(KernelEvent.ObjectAdded, iw)
            return True

        if isinstance(msg, ObjectQuantityMessage):
            iw = InventoryManager().inventory.modifyItemQuantity(msg.objectUID, msg.quantity)
            for shortcutQty in InventoryManager().shortcutBarItems:
                if shortcutQty and shortcutQty.id == msg.objectUID:
                    shortcutQty.quantity = msg.quantity
            KernelEventsManager().send(KernelEvent.ObjectAdded, iw)
            return True

        if isinstance(msg, ObjectsQuantityMessage):
            osqm = msg
            for objoqm in osqm.objectsUIDAndQty:
                InventoryManager().inventory.modifyItemQuantity(objoqm.objectUID, objoqm.quantity)
                for shortcutsQty in InventoryManager().shortcutBarItems:
                    if shortcutsQty and shortcutsQty.id == objoqm.objectUID:
                        shortcutsQty.quantity = objoqm.quantity
            return True

        if isinstance(msg, KamasUpdateMessage):
            InventoryManager().inventory.kamas = msg.kamasTotal
            KernelEventsManager().send(KernelEvent.KamasUpdate, msg.kamasTotal)
            return True

        if isinstance(msg, InventoryWeightMessage):
            lastInventoryWeight = PlayedCharacterManager().inventoryWeight
            PlayedCharacterManager().inventoryWeight = msg.inventoryWeight
            PlayedCharacterManager().inventoryWeightMax = msg.weightMax
            if msg.inventoryWeight / msg.weightMax > 0.95:
                KernelEventsManager().send(KernelEvent.PlayerPodsFull)
            KernelEventsManager().send(
                KernelEvent.InventoryWeightUpdate, lastInventoryWeight, msg.inventoryWeight, msg.weightMax
            )
            return True

        if isinstance(msg, ObjectMovementMessage):
            ommsg = msg
            InventoryManager().inventory.modifyItemPosition(ommsg.objectUID, ommsg.position)
            return True

        if isinstance(msg, ObjectModifiedMessage):
            omdmsg = msg
            inventoryMgr = InventoryManager()
            inventoryMgr.inventory.modifyObjectItem(omdmsg.object)
            return False

        if isinstance(msg, ObjectDeletedMessage):
            odmsg = msg
            InventoryManager().inventory.removeItem(odmsg.objectUID, -1)
            return True

        if isinstance(msg, ObjectsDeletedMessage):
            osdmsg = msg
            for osdit in osdmsg.objectUID:
                InventoryManager().inventory.removeItem(osdit, -1)
            return True

        if isinstance(msg, DeleteObjectAction):
            doa = msg
            odmsg2 = ObjectDeleteMessage()
            odmsg2.init(doa.objectUID, doa.quantity)
            ConnectionsHandler().send(odmsg2)
            return True

        return False

    def pulled(self) -> bool:
        return True

    def onAcceptDrop(self) -> None:
        self._dropPopup = None
        odropmsg: ObjectDropMessage = ObjectDropMessage()
        odropmsg.init(self._objectUIDToDrop, self._quantityToDrop)
        if not PlayedCharacterManager().isFighting:
            ConnectionsHandler().send(odropmsg)

    def onRefuseDrop(self) -> None:
        self._dropPopup = None

    def useItem(self, iw: ItemWrapper, quantity=0, useOnCell=False):
        if useOnCell and iw.targetable:
            if Kernel().battleFrame:
                return
        else:
            if quantity > 1:
                oumsg = ObjectUseMultipleMessage()
                oumsg.init(iw.objectUID, quantity)
            else:
                oumsg = ObjectUseMessage()
                oumsg.init(iw.objectUID)
            playerEntity = PlayedCharacterManager().entity
            if playerEntity and playerEntity.isMoving:
                playerEntity.stop()
            else:
                ConnectionsHandler().send(oumsg)
