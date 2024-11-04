from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import GroupItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.npcs.Npc import Npc
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import InventoryManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.enums.DialogTypeEnum import DialogTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.ExchangeTypeEnum import ExchangeTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogRequestMessage import (
    LeaveDialogRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildChestTabContributionMessage import (
    GuildChestTabContributionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildChestTabContributionsMessage import (
    GuildChestTabContributionsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildGetChestTabContributionsRequestMessage import (
    GuildGetChestTabContributionsRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildSelectChestTabRequestMessage import (
    GuildSelectChestTabRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.StartGuildChestContributionMessage import (
    StartGuildChestContributionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.StopGuildChestContributionMessage import (
    StopGuildChestContributionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeLeaveMessage import (
    ExchangeLeaveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMoveKamaMessage import (
    ExchangeObjectMoveKamaMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMoveToTabMessage import (
    ExchangeObjectMoveToTabMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectTransfertAllFromInvMessage import (
    ExchangeObjectTransfertAllFromInvMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectTransfertAllToInvMessage import (
    ExchangeObjectTransfertAllToInvMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectTransfertExistingFromInvMessage import (
    ExchangeObjectTransfertExistingFromInvMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectTransfertExistingToInvMessage import (
    ExchangeObjectTransfertExistingToInvMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectTransfertListFromInvMessage import (
    ExchangeObjectTransfertListFromInvMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectTransfertListToInvMessage import (
    ExchangeObjectTransfertListToInvMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectTransfertListWithQuantityToInvMessage import (
    ExchangeObjectTransfertListWithQuantityToInvMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangePlayerRequestMessage import (
    ExchangePlayerRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeRequestedTradeMessage import (
    ExchangeRequestedTradeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedMessage import (
    ExchangeStartedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedTaxCollectorShopMessage import (
    ExchangeStartedTaxCollectorShopMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedWithMultiTabStorageMessage import (
    ExchangeStartedWithMultiTabStorageMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedWithPodsMessage import (
    ExchangeStartedWithPodsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedWithStorageMessage import (
    ExchangeStartedWithStorageMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkNpcShopMessage import (
    ExchangeStartOkNpcShopMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkNpcTradeMessage import (
    ExchangeStartOkNpcTradeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkRecycleTradeMessage import (
    ExchangeStartOkRecycleTradeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkRunesTradeMessage import (
    ExchangeStartOkRunesTradeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.RecycleResultMessage import (
    RecycleResultMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.storage.StorageInventoryContentMessage import (
    StorageInventoryContentMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.storage.StorageObjectRemoveMessage import (
    StorageObjectRemoveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.storage.StorageObjectsRemoveMessage import (
    StorageObjectsRemoveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.storage.StorageObjectsUpdateMessage import (
    StorageObjectsUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.storage.StorageObjectUpdateMessage import (
    StorageObjectUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.ProtocolConstantsEnum import ProtocolConstantsEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayNamedActorInformations import (
    GameRolePlayNamedActorInformations,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class ExchangeManagementFrame(Frame):
    def __init__(self):
        super().__init__()
        self._sourceInformations: GameRolePlayNamedActorInformations
        self._targetInformations: GameRolePlayNamedActorInformations
        self._success: bool

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        self._success = None
        return True

    def pulled(self) -> bool:
        if Kernel().commonExchangeManagementFrame:
            Kernel().worker.removeFrameByName("CommonExchangeManagementFrame")
        if self._success is not None:
            KernelEventsManager().send(KernelEvent.ExchangeLeave, self._success)
        return True

    def initBankStock(self, objectsInfos):
        InventoryManager().bankInventory.initializeFromObjectItems(objectsInfos)
        InventoryManager().bankInventory.releaseHooks()

    def processExchangeRequestedTradeMessage(self, msg: ExchangeRequestedTradeMessage):
        if msg.exchangeType != ExchangeTypeEnum.PLAYER_TRADE:
            return
        self._source_informations: GameRolePlayNamedActorInformations = Kernel().roleplayEntitiesFrame.getEntityInfos(
            msg.source
        )
        self._target_informations: GameRolePlayNamedActorInformations = Kernel().roleplayEntitiesFrame.getEntityInfos(
            msg.target
        )
        source_name = self._source_informations.name
        target_name = self._target_informations.name
        if msg.source == PlayedCharacterManager().id:
            KernelEventsManager().send(KernelEvent.ExchangeRequestFromMe, source_name, target_name)
        else:
            KernelEventsManager().send(KernelEvent.ExchangeRequestToMe, target_name, source_name)

    def processExchangeStartOkNpcTradeMessage(msg: ExchangeStartOkNpcTradeMessage):
        source_name = PlayedCharacterManager().infos.name
        # NPCID = Kernel().entitiesFrame.getEntityInfos(msg.npcId).contextualId
        # NPC = Npc.getNpcById(NPCID)
        target_name = Npc.getNpcById(Kernel().roleplayEntitiesFrame.getEntityInfos(msg.npcId).npcId).name
        PlayedCharacterManager().isInExchange = True
        KernelEventsManager().send(KernelEvent.ExchangeStartOkNpcTrade, msg.npcId, source_name, target_name)
        KernelEventsManager().send(KernelEvent.ExchangeStartedType, ExchangeTypeEnum.NPC_TRADE)

    def processExchangeStartOkRunesTradeMessage(msg: ExchangeStartOkRunesTradeMessage):
        PlayedCharacterManager().isInExchange = True
        KernelEventsManager().send(KernelEvent.ExchangeStartOkRunesTrade)
        KernelEventsManager().send(KernelEvent.ExchangeStartedType, ExchangeTypeEnum.RUNES_TRADE)

    def processExchangeStartOkRecycleTradeMessage(msg: ExchangeStartOkRecycleTradeMessage):
        PlayedCharacterManager().isInExchange = True
        KernelEventsManager().send(
            KernelEvent.ExchangeStartOkRecycleTrade,
            msg.percentToPlayer,
            msg.percentToPrism,
            msg.adjacentSubareaPossessed,
            msg.adjacentSubareaUnpossessed,
        )
        KernelEventsManager().send(KernelEvent.ExchangeStartedType, ExchangeTypeEnum.RECYCLE_TRADE)

    def exchangeObjectMoveKama(self, kamas):
        eomkmsg = ExchangeObjectMoveKamaMessage()
        eomkmsg.init(kamas)
        ConnectionsHandler().send(eomkmsg)

    def exchangeObjectTransferListToInv(self, ids: list[int]):
        """
        Transfer a list of objects from storage to inventory.

        Args:
            ids: List of object UIDs to transfer

        Note: Handles protocol constants and splitting large transfers automatically
        """
        if len(ids) > ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT:
            Logger().info(I18n.getUiText("ui.exchange.partialTransfert"))

        if len(ids) >= ProtocolConstantsEnum.MIN_OBJ_COUNT_BY_XFERT:
            msg = ExchangeObjectTransfertListToInvMessage()
            msg.init(ids[: ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT])
            ConnectionsHandler().send(msg)

    def exchangeObjectTransfertAllToInv(self):
        eotatimsg = ExchangeObjectTransfertAllToInvMessage()
        eotatimsg.init()
        ConnectionsHandler().send(eotatimsg)

    def exchangeObjectTransfertExistingToInv(self):
        eotetimsg = ExchangeObjectTransfertExistingToInvMessage()
        eotetimsg.init()
        ConnectionsHandler().send(eotetimsg)

    def exchangeObjectTransferAllFromInv(self):
        ConnectionsHandler().send(ExchangeObjectTransfertAllFromInvMessage())

    def exchangeObjectTransferListFromInv(self, ids):
        if len(ids) > ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT:
            Logger().info(I18n.getUiText("ui.exchange.partialTransfert"))
        if len(ids) >= ProtocolConstantsEnum.MIN_OBJ_COUNT_BY_XFERT:
            eotlfimsg = ExchangeObjectTransfertListFromInvMessage()
            eotlfimsg.init(ids[: ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT])
            ConnectionsHandler().send(eotlfimsg)

    def exchangeObjectTransfertExistingFromInv(self):
        eotefimsg = ExchangeObjectTransfertExistingFromInvMessage()
        eotefimsg.init()
        ConnectionsHandler().send(eotefimsg)

    def laveDialogRequest(self):
        ConnectionsHandler().send(LeaveDialogRequestMessage())

    def guildSelectChestTabRequest(self, tabNumber):
        gcctrm = GuildSelectChestTabRequestMessage()
        gcctrm.init(tabNumber)
        ConnectionsHandler().send(gcctrm)

    def startGuildChestContribution(self):
        sgccm = StartGuildChestContributionMessage()
        sgccm.init()
        ConnectionsHandler().send(sgccm)

    def stopGuildChestContribution(self):
        spgccm = StopGuildChestContributionMessage()
        spgccm.init()
        ConnectionsHandler().send(spgccm)

    def guildGetChestTabContributionsRequestAction(self):
        ggctcrm = GuildGetChestTabContributionsRequestMessage()
        ggctcrm.init()
        ConnectionsHandler().send(ggctcrm)

    def exchangeObjectMoveToTabAction(self, objectUID, quantity, tabNumber):
        eomttm = ExchangeObjectMoveToTabMessage()
        eomttm.init(objectUID, quantity, tabNumber)
        ConnectionsHandler().send(eomttm)

    def exchangePlayerRequest(self, exchangeType, target):
        msg = ExchangePlayerRequestMessage()
        msg.init(target, exchangeType)
        ConnectionsHandler().send(msg)

    def exchangeObjectTransferListWithQuantityToInv(self, ids, qtys):
        if len(ids) > ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT / 2:
            Logger().info(I18n.getUiText("ui.exchange.partialTransfert"))
        if len(ids) >= ProtocolConstantsEnum.MIN_OBJ_COUNT_BY_XFERT and len(ids) == len(qtys):
            eotlwqtoimsg = ExchangeObjectTransfertListWithQuantityToInvMessage()
            eotlwqtoimsg.init(
                ids[: ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT // 2],
                qtys[: ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT // 2],
            )
            ConnectionsHandler().send(eotlwqtoimsg)
        else:
            raise ValueError(f"Invalid ids and qtys : {ids}, {qtys}")

    def processExchangeLeave(self, msg: ExchangeLeaveMessage):
        Logger().debug(f"Exchange closed")
        if msg.dialogType == DialogTypeEnum.DIALOG_EXCHANGE:
            PlayedCharacterManager().isInExchange = False
            self._success = msg.success
            Kernel().worker.removeFrame(self)
        KernelEventsManager().send(KernelEvent.ExchangeClose, msg.success)

    def process(self, msg: Message) -> bool:

        if isinstance(msg, ExchangeStartedWithStorageMessage):
            PlayedCharacterManager().isInExchange = True
            commonExchangeFrame = Kernel().commonExchangeManagementFrame
            if commonExchangeFrame:
                commonExchangeFrame.resetEchangeSequence()
            pods = int(msg.storageMaxSlot)
            KernelEventsManager().send(KernelEvent.ExchangeBankStartedWithStorage, msg.exchangeType, pods)
            return False

        if isinstance(msg, ExchangeStartedWithMultiTabStorageMessage):
            PlayedCharacterManager().isInExchange = True
            commonExchangeManagementFrame = Kernel().commonExchangeManagementFrame
            if commonExchangeManagementFrame:
                commonExchangeManagementFrame.resetEchangeSequence()
            KernelEventsManager().send(
                KernelEvent.ExchangeBankStartedWithMultiTabStorage, msg.exchangeType, msg.storageMaxSlot, msg.tabNumber
            )
            return False

        if isinstance(msg, ExchangeStartedMessage):
            PlayedCharacterManager().isInExchange = True
            commonExchangeFrame = Kernel().commonExchangeManagementFrame
            if commonExchangeFrame:
                commonExchangeFrame.resetEchangeSequence()
                if msg.exchangeType == ExchangeTypeEnum.PLAYER_TRADE:
                    sourceName = self._sourceInformations.name
                    targetName = self._targetInformations.name
                    sourceCurrentPods = -1
                    targetCurrentPods = -1
                    sourceMaxPods = -1
                    targetMaxPods = -1
                    if isinstance(msg, ExchangeStartedWithPodsMessage):
                        if msg.firstCharacterId == self._sourceInformations.contextualId:
                            sourceCurrentPods = int(msg.firstCharacterCurrentWeight)
                            targetCurrentPods = int(msg.secondCharacterCurrentWeight)
                            sourceMaxPods = int(msg.firstCharacterMaxWeight)
                            targetMaxPods = int(msg.secondCharacterMaxWeight)
                        else:
                            targetCurrentPods = int(msg.firstCharacterCurrentWeight)
                            sourceCurrentPods = int(msg.secondCharacterCurrentWeight)
                            targetMaxPods = int(msg.firstCharacterMaxWeight)
                            sourceMaxPods = int(msg.secondCharacterMaxWeight)
                    if PlayedCharacterManager().id == msg.firstCharacterId:
                        exchangeOtherCharacterId = msg.secondCharacterId
                    else:
                        exchangeOtherCharacterId = msg.firstCharacterId
                    KernelEventsManager().send(
                        KernelEvent.ExchangeStarted,
                        sourceName,
                        targetName,
                        sourceCurrentPods,
                        targetCurrentPods,
                        sourceMaxPods,
                        targetMaxPods,
                        exchangeOtherCharacterId,
                    )
                    KernelEventsManager().send(KernelEvent.ExchangeStartedType, msg.exchangeType)
                elif msg.exchangeType == ExchangeTypeEnum.STORAGE:
                    KernelEventsManager().send(KernelEvent.ExchangeStartedType, msg.exchangeType)
                return True

        elif isinstance(msg, ExchangeStartedTaxCollectorShopMessage):
            PlayedCharacterManager().isInExchange = True
            InventoryManager().bankInventory.kamas = msg.kamas
            KernelEventsManager().send(KernelEvent.ExchangeBankStarted, ExchangeTypeEnum.MOUNT, msg.objects, msg.kamas)
            return True

        elif isinstance(msg, StorageInventoryContentMessage):
            InventoryManager().bankInventory.kamas = msg.kamas
            InventoryManager().bankInventory.initializeFromObjectItems(msg.objects)
            KernelEventsManager().send(KernelEvent.InventoryContent, msg.objects, msg.kamas)
            return True

        elif isinstance(msg, StorageObjectUpdateMessage):
            object = msg.object
            itemChanged = ItemWrapper.create(
                object.position, object.objectUID, object.objectGID, object.quantity, object.effects
            )
            InventoryManager().bankInventory.modifyItem(itemChanged)
            InventoryManager().bankInventory.releaseHooks()
            return True

        elif isinstance(msg, StorageObjectRemoveMessage):
            InventoryManager().bankInventory.removeItem(msg.objectUID)
            InventoryManager().bankInventory.releaseHooks()
            return True

        elif isinstance(msg, StorageObjectsUpdateMessage):
            for sosuit in msg.objectList:
                sosuobj = sosuit
                sosuic = ItemWrapper.create(
                    sosuobj.position, sosuobj.objectUID, sosuobj.objectGID, sosuobj.quantity, sosuobj.effects
                )
                InventoryManager().bankInventory.modifyItem(sosuic)
            InventoryManager().bankInventory.releaseHooks()
            return True

        elif isinstance(msg, StorageObjectsRemoveMessage):
            for sosruid in msg.objectUIDList:
                InventoryManager().bankInventory.removeItem(sosruid)
            InventoryManager().bankInventory.releaseHooks()
            return True

        elif isinstance(msg, ExchangeStartOkNpcShopMessage):
            PlayedCharacterManager().isInExchange = True
            Kernel().worker.process(ChangeWorldInteractionAction.create(False, True))
            NPCShopItems = []
            for oitsins in msg.objectsInfos:
                itemwra = ItemWrapper.create(63, 0, oitsins.objectGID, 0, oitsins.effects, False)
                stockItem = TradeStockItemWrapper.create(
                    itemwra, oitsins.objectPrice, GroupItemCriterion(oitsins.buyCriterion)
                )
                NPCShopItems.append(stockItem)
            KernelEventsManager().send(KernelEvent.ExchangeStartOkNpcShop, msg.npcSellerId, NPCShopItems, msg.tokenId)
            return True

        elif isinstance(msg, ExchangeStartOkRunesTradeMessage):
            PlayedCharacterManager().isInExchange = True
            KernelEventsManager().send(KernelEvent.ExchangeStartOkRunesTrade)
            return True

        elif isinstance(msg, ExchangeStartOkRecycleTradeMessage):
            PlayedCharacterManager().isInExchange = True
            KernelEventsManager().send(
                KernelEvent.ExchangeStartOkRecycleTrade,
                msg.percentToPlayer,
                msg.percentToPrism,
                msg.adjacentSubareaPossessed,
                msg.adjacentSubareaUnpossessed,
            )
            return True

        elif isinstance(msg, RecycleResultMessage):
            KernelEventsManager().send(KernelEvent.RecycleResult, msg.nuggetsForPlayer, msg.nuggetsForPrism)
            Logger().info(
                I18n.getUiText(
                    "ui.recycle.resultDetailed",
                    [msg.nuggetsForPlayer, msg.nuggetsForPrism, f"{{item,{DataEnum.ITEM_GID_NUGGET}}}"],
                )
            )
            return True

        elif isinstance(msg, ExchangeLeaveMessage):
            self.processExchangeLeave(msg)
            return True

        elif isinstance(msg, GuildChestTabContributionMessage):
            KernelEventsManager().send(
                KernelEvent.GuildChestTabContribution,
                msg.tabNumber,
                msg.requiredAmount,
                msg.currentAmount,
                msg.chestContributionEnrollmentDelay,
                msg.chestContributionDelay,
            )
            return True

        elif isinstance(msg, GuildChestTabContributionsMessage):
            KernelEventsManager().send(KernelEvent.GuildChestContributions, msg.contributions)
            return True
