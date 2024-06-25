from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import InventoryManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.StorageOptionManager import StorageOptionManager
from pydofus2.com.ankamagames.dofus.network.enums.ExchangeTypeEnum import ExchangeTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogRequestMessage import (
    LeaveDialogRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeAcceptMessage import (
    ExchangeAcceptMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeIsReadyMessage import (
    ExchangeIsReadyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectAddedMessage import (
    ExchangeObjectAddedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMoveMessage import (
    ExchangeObjectMoveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectsAddedMessage import (
    ExchangeObjectsAddedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeReadyMessage import (
    ExchangeReadyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.FocusedExchangeReadyMessage import (
    FocusedExchangeReadyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ExchangeKamaModifiedMessage import (
    ExchangeKamaModifiedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ExchangeObjectModifiedMessage import (
    ExchangeObjectModifiedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ExchangeObjectRemovedMessage import (
    ExchangeObjectRemovedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ExchangeObjectsModifiedMessage import (
    ExchangeObjectsModifiedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ExchangeObjectsRemovedMessage import (
    ExchangeObjectsRemovedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.ExchangePodsModifiedMessage import (
    ExchangePodsModifiedMessage,
)
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class CommonExchangeManagementFrame(Frame):

    def __init__(self, pExchangeType):
        super().__init__()
        self._exchangeType = pExchangeType
        self._numCurrentSequence = 0

    def incrementEchangeSequence(self):
        self._numCurrentSequence += 1

    def resetEchangeSequence(self):
        self._numCurrentSequence = 0

    def leaveShopStock(self):
        ldrmsg = LeaveDialogRequestMessage()
        ldrmsg.init()
        # TODO : Implement the BidHouseManagementFrame class
        bidhouseManagementFrame = Kernel().bidHouseManagementFrame
        if bidhouseManagementFrame:
            bidhouseManagementFrame.switching = False
        ConnectionsHandler().send(ldrmsg)

    def exchangeAccept(self):
        exchangeAcceptMessage = ExchangeAcceptMessage()
        exchangeAcceptMessage.init()
        ConnectionsHandler().send(exchangeAcceptMessage)

    def exchangeRefuse(self):
        ldrmsg = LeaveDialogRequestMessage()
        ldrmsg.init()
        ConnectionsHandler().send(ldrmsg)

    def exchangeReady(self, isReady):
        ermsg = ExchangeReadyMessage()
        ermsg.init(isReady, self._numCurrentSequence)  # Assuming _numCurrentSequence is an instance variable
        if Kernel().craftFrame and (
            Kernel().craftFrame.skillId == DataEnum.SKILL_CHINQ
            or Kernel().craftFrame.skillId == DataEnum.SKILL_MINOUKI
        ):  # Assuming craftFrame and skillId are accessible attributes/variables
            Kernel().craftFrame.saveLastPlayerComponentList()
        ConnectionsHandler().send(ermsg)

    def exchangeReadyCrush(self, isReady, focusActionId):
        fermsg = FocusedExchangeReadyMessage()
        fermsg.init(
            isReady, self._numCurrentSequence, focusActionId
        )  # Assuming _numCurrentSequence and focusActionId are accessible attributes/variables
        ConnectionsHandler().send(fermsg)
        return True

    def exchangeObjectMove(self, objectUID, quantity):
        iw = InventoryManager().inventory.getItem(objectUID)
        if not iw:
            iw = InventoryManager().bankInventory.getItem(objectUID)
        if iw and iw.quantity == abs(quantity):
            pass
        eomvmsg = ExchangeObjectMoveMessage()
        eomvmsg.init(objectUID, quantity)
        ConnectionsHandler().send(eomvmsg)

    def process(self, msg):

        if isinstance(msg, ExchangeObjectModifiedMessage):
            self._numCurrentSequence += 1
            iwModified = ItemWrapper.create(
                msg.object.position,
                msg.object.objectUID,
                msg.object.objectGID,
                msg.object.quantity,
                msg.object.effects,
                False,
            )
            if self._exchangeType == ExchangeTypeEnum.CRAFT:
                Kernel().craftFrame.modifyCraftComponent(msg.remote, iwModified)
            KernelEventsManager().send(KernelEvent.ExchangeObjectModified, iwModified, msg.remote)
            return True

        elif isinstance(msg, ExchangeObjectsModifiedMessage):
            self._numCurrentSequence += 1
            itemModifiedArray = []
            for anModifiedItem in msg.object:
                iwsModified = ItemWrapper.create(
                    anModifiedItem.position,
                    anModifiedItem.objectUID,
                    anModifiedItem.objectGID,
                    anModifiedItem.quantity,
                    anModifiedItem.effects,
                    False,
                )
                if self._exchangeType == ExchangeTypeEnum.CRAFT:
                    Kernel().craftFrame.modifyCraftComponent(msg.remote, iwsModified)
                itemModifiedArray.append(iwsModified)
            KernelEventsManager().send(KernelEvent.ExchangeObjectListModified, itemModifiedArray, msg.remote)
            return True

        elif isinstance(msg, ExchangeObjectAddedMessage):
            self._numCurrentSequence += 1
            iwAdded = ItemWrapper.create(
                msg.object.position,
                msg.object.objectUID,
                msg.object.objectGID,
                msg.object.quantity,
                msg.object.effects,
                False,
            )
            if self._exchangeType == ExchangeTypeEnum.CRAFT:
                Kernel().craftFrame.addCraftComponent(msg.remote, iwAdded)
            KernelEventsManager().send(KernelEvent.ExchangeObjectAdded, iwAdded, msg.remote)
            return True

        elif isinstance(msg, ExchangeObjectsAddedMessage):
            self._numCurrentSequence += 1
            itemAddedArray = []
            for anAddedObje in msg.object:
                iwsAdded = ItemWrapper.create(
                    anAddedObje.position,
                    anAddedObje.objectUID,
                    anAddedObje.objectGID,
                    anAddedObje.quantity,
                    anAddedObje.effects,
                    False,
                )
                if self._exchangeType == ExchangeTypeEnum.CRAFT:
                    Kernel().craftFrame.addCraftComponent(msg.remote, iwsAdded)
                itemAddedArray.append(iwsAdded)
            KernelEventsManager().send(KernelEvent.ExchangeObjectListAdded, itemAddedArray, msg.remote)
            return True

        elif isinstance(msg, ExchangeObjectRemovedMessage):
            self._numCurrentSequence += 1
            if self._exchangeType == ExchangeTypeEnum.CRAFT:
                Kernel().craftFrame.removeCraftComponent(msg.remote, msg.objectUID)
            KernelEventsManager().send(KernelEvent.ExchangeObjectRemoved, msg.objectUID, msg.remote)
            return True

        elif isinstance(msg, ExchangeObjectsRemovedMessage):
            self._numCurrentSequence += 1
            itemDeleteMessage = []
            for itemUid in msg.objectUID:
                if self._exchangeType == ExchangeTypeEnum.CRAFT:
                    Kernel().craftFrame.removeCraftComponent(msg.remote, itemUid)
                itemDeleteMessage.append(itemUid)
            KernelEventsManager().send(KernelEvent.ExchangeObjectListRemoved, itemDeleteMessage, msg.remote)
            return True

        if isinstance(msg, ExchangeIsReadyMessage):
            roleplayEntitiesFrame = Kernel().roleplayEntitiesFrame
            playerName = roleplayEntitiesFrame.getEntityInfos(msg.id).name
            KernelEventsManager().send(KernelEvent.ExchangeIsReady, playerName, msg.ready)
            return True

        if isinstance(msg, ExchangeKamaModifiedMessage):
            self._numCurrentSequence += 1
            if not msg.remote:
                StorageOptionManager().updateStorageView()
            KernelEventsManager().send(KernelEvent.ExchangeKamaModified, msg.quantity, msg.remote)
            return True

        if isinstance(msg, ExchangePodsModifiedMessage):
            self._numCurrentSequence += 1
            KernelEventsManager().send(KernelEvent.ExchangePodsModified, msg.currentWeight, msg.maxWeight, msg.remote)
            return True

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def pulled(self) -> bool:
        if Kernel().worker.contains("CraftFrame"):
            Kernel().worker.removeFrameByName("CraftFrame")
        return True
