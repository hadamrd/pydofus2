from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.mount.MountData import MountData
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.frames.MountDialogFrame import MountDialogFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import TimeManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.network.enums.ChatActivableChannelsEnum import ChatActivableChannelsEnum
from pydofus2.com.ankamagames.dofus.network.enums.MountCharacteristicEnum import MountCharacteristicEnum
from pydofus2.com.ankamagames.dofus.network.enums.MountEquipedErrorEnum import MountEquipedErrorEnum
from pydofus2.com.ankamagames.dofus.network.enums.ProtocolConstantsEnum import ProtocolConstantsEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountDataMessage import MountDataMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountEmoteIconUsedOkMessage import (
    MountEmoteIconUsedOkMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountEquipedErrorMessage import (
    MountEquipedErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountFeedRequestMessage import (
    MountFeedRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountHarnessColorsUpdateRequestMessage import (
    MountHarnessColorsUpdateRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountHarnessDissociateRequestMessage import (
    MountHarnessDissociateRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountInformationInPaddockRequestMessage import (
    MountInformationInPaddockRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountInformationRequestMessage import (
    MountInformationRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountReleasedMessage import (
    MountReleasedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountReleaseRequestMessage import (
    MountReleaseRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountRenamedMessage import MountRenamedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountRenameRequestMessage import (
    MountRenameRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountRidingMessage import MountRidingMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountSetMessage import MountSetMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountSetXpRatioRequestMessage import (
    MountSetXpRatioRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountSterilizedMessage import (
    MountSterilizedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountSterilizeRequestMessage import (
    MountSterilizeRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountToggleRidingRequestMessage import (
    MountToggleRidingRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountUnSetMessage import MountUnSetMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.mount.MountXpRatioMessage import MountXpRatioMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeHandleMountsMessage import (
    ExchangeHandleMountsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeMountsPaddockAddMessage import (
    ExchangeMountsPaddockAddMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeMountsPaddockRemoveMessage import (
    ExchangeMountsPaddockRemoveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeMountsStableAddMessage import (
    ExchangeMountsStableAddMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeMountsStableRemoveMessage import (
    ExchangeMountsStableRemoveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeMountsTakenFromPaddockMessage import (
    ExchangeMountsTakenFromPaddockMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeRequestOnMountStockMessage import (
    ExchangeRequestOnMountStockMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkMountMessage import (
    ExchangeStartOkMountMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkMountWithOutPaddockMessage import (
    ExchangeStartOkMountWithOutPaddockMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeWeightMessage import (
    ExchangeWeightMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.UpdateMountCharacteristicsMessage import (
    UpdateMountCharacteristicsMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.mount.UpdateMountIntegerCharacteristic import (
    UpdateMountIntegerCharacteristic,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class MountFrame(Frame):
    MAX_XP_RATIO = 90

    def __init__(self):
        self._mountDialogFrame = None
        self._mountXpRatio = None
        self._stableList = None
        self._paddockList: list[MountData] = None
        self._inventoryWeight = None
        self._inventoryMaxWeight = None
        self._isRiding = False

    @property
    def priority(self):
        return Priority.NORMAL

    @property
    def mountXpRatio(self):
        return self._mountXpRatio

    @property
    def stableList(self):
        return self._stableList

    @property
    def paddockList(self):
        return self._paddockList

    def pushed(self):
        self._mountDialogFrame = MountDialogFrame()
        return True

    def pulled(self):
        Logger().info("MountFrame pulled")
        return True

    def initializeMountLists(self, stables, paddocks):
        self._stableList = []
        if stables:
            for mcd in stables:
                self._stableList.append(MountData.makeMountData(mcd, True, self._mountXpRatio))

        self._paddockList = []
        if paddocks:
            for mcd in paddocks:
                self._paddockList.append(MountData.makeMountData(mcd, True, self._mountXpRatio))

    def mountInformationInPaddockRequest(self, mountId):
        miiprmsg = MountInformationInPaddockRequestMessage()
        miiprmsg.init(mountId)
        ConnectionsHandler().send(miiprmsg)

    def mountToggleRidingRequest(self):
        playerEntity = DofusEntities().getEntity(PlayedCharacterManager().id)
        if playerEntity and not playerEntity.isMoving:
            mtrrmsg = MountToggleRidingRequestMessage()
            mtrrmsg.init()
            ConnectionsHandler().send(mtrrmsg)
        else:
            Logger().warning("Player is moving, mount toggle riding request aborted")

    def mountFeedRequest(self, mountId, mountLocation, mountFoodUid, quantity):
        if Kernel().battleFrame is None:
            mfrmsg = MountFeedRequestMessage()
            mfrmsg.init(mountId, mountLocation, mountFoodUid, quantity)
            ConnectionsHandler().send(mfrmsg)

    def mountReleaseRequest(self):
        mrrmsg = MountReleaseRequestMessage()
        mrrmsg.init()
        ConnectionsHandler().send(mrrmsg)

    def mountSterilizeRequest(self):
        msrmsg = MountSterilizeRequestMessage()
        msrmsg.init()
        ConnectionsHandler().send(msrmsg)

    def mountrenameRequest(self, newName, mountId):
        mountRenameRequestMessage = MountRenameRequestMessage()
        mountRenameRequestMessage.init(newName if newName else "", mountId)
        ConnectionsHandler().send(mountRenameRequestMessage)

    def mountSetXppRatioRequest(self, xpRatio):
        msxrpmsg = MountSetXpRatioRequestMessage()
        msxrpmsg.init(min(xpRatio, self.MAX_XP_RATIO))
        ConnectionsHandler().send(msxrpmsg)

    def mountinfoRequest(self, mountId, time):
        mirmsg = MountInformationRequestMessage()
        mirmsg.init(mountId, time)
        ConnectionsHandler().send(mirmsg)

    def exchangeRequestOnMountStock(self):
        eromsmsg = ExchangeRequestOnMountStockMessage()
        eromsmsg.init()
        ConnectionsHandler().send(eromsmsg)

    def ExchangeHandleMountStable(self, ridesId, actionType):
        idsVector = list(ridesId)
        vecLength = len(idsVector)
        while vecLength > 0:
            if vecLength > ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT:
                proxVector = idsVector[: ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT]
                idsVector = idsVector[ProtocolConstantsEnum.MAX_OBJ_COUNT_BY_XFERT :]
            else:
                proxVector = idsVector
                vecLength = 0
            ehmsmsg = ExchangeHandleMountsMessage()
            ehmsmsg.init(actionType, proxVector)
            ConnectionsHandler().send(ehmsmsg)

    def MountHarnessDissociateRequest(self):
        mhdrmsg = MountHarnessDissociateRequestMessage()
        mhdrmsg.init()
        ConnectionsHandler().send(mhdrmsg)

    def MountHarnessColorsUpdateRequest(self, useHarnessColors):
        mhcurmsg = MountHarnessColorsUpdateRequestMessage()
        mhcurmsg.init(useHarnessColors)
        ConnectionsHandler().send(mhcurmsg)

    def process(self, msg: Message):

        if isinstance(msg, MountSterilizedMessage):
            mountId = msg.mountId
            mount = MountData.getMountFromCache(mountId)
            if mount:
                mount.reproductionCount = -1
            KernelEventsManager().send(KernelEvent.MountSterilized, mountId)
            return True

        if isinstance(msg, MountRenamedMessage):
            mountId = msg.mountId
            mountName = msg.name
            mount = MountData.getMountFromCache(mountId)
            if mount:
                mount.name = mountName
            if self._mountDialogFrame.inStable:
                KernelEventsManager().send(KernelEvent.MountStableUpdate, self._stableList, None, None)
            KernelEventsManager().send(KernelEvent.MountRenamed, mountId, mountName)
            return True

        if isinstance(msg, ExchangeMountsStableAddMessage):
            if self._stableList:
                for mountData in msg.mountDescription:
                    self._stableList.append(MountData.makeMountData(mountData, True, self._mountXpRatio))
            KernelEventsManager().send(KernelEvent.MountStableUpdate, self._stableList, None, None)
            return True

        if isinstance(msg, ExchangeMountsStableRemoveMessage):
            for uMountId in msg.mountsId:
                for i in range(len(self._stableList)):
                    if self._stableList[i].id == uMountId:
                        del self._stableList[i]
                        break
            KernelEventsManager().send(KernelEvent.MountStableUpdate, self._stableList, None, None)
            return True

        if isinstance(msg, ExchangeMountsPaddockAddMessage):
            for mountData in msg.mountDescription:
                self._paddockList.append(MountData.makeMountData(mountData, True, self._mountXpRatio))
            KernelEventsManager().send(KernelEvent.MountStableUpdate, None, self._paddockList, None)
            return True

        if isinstance(msg, ExchangeMountsPaddockRemoveMessage):
            for uMountId in msg.mountsId:
                for i in range(len(self._paddockList)):
                    if self._paddockList[i].id == uMountId:
                        del self._paddockList[i]
                        break
            KernelEventsManager().send(KernelEvent.MountStableUpdate, None, self._paddockList, None)
            return True

        if isinstance(msg, MountXpRatioMessage):
            self._mountXpRatio = msg.ratio
            mount = PlayedCharacterManager().mount
            if mount:
                mount.xpRatio = self._mountXpRatio
            KernelEventsManager().send(KernelEvent.MountXpRatio, self._mountXpRatio)
            return True

        if isinstance(msg, MountDataMessage):
            if self._mountDialogFrame.inStable:
                KernelEventsManager().send(
                    KernelEvent.CertificateMountData, MountData.makeMountData(msg.mountData, False, self.mountXpRatio)
                )
            else:
                KernelEventsManager().send(
                    KernelEvent.PaddockedMountData, MountData.makeMountData(msg.mountData, False, self.mountXpRatio)
                )
            return True

        if isinstance(msg, MountRidingMessage):
            self._isRiding = msg.isRiding
            PlayedCharacterManager().isRiding = msg.isRiding
            Logger().info(f"Player is {'riding' if msg.isRiding else 'not riding'} mount!")
            KernelEventsManager().send(KernelEvent.MountRiding, msg.isRiding)
            return True

        if isinstance(msg, MountEquipedErrorMessage):
            meemsg = msg
            if meemsg.errorType == MountEquipedErrorEnum.UNSET:
                typeError = "UNSET"
            elif meemsg.errorType == MountEquipedErrorEnum.SET:
                typeError = "SET"
            elif meemsg.errorType == MountEquipedErrorEnum.RIDING:
                typeError = "RIDING"
                KernelEventsManager().send(KernelEvent.MountRiding, False)
            KernelEventsManager().send(KernelEvent.MountEquipedError, typeError)
            return True

        elif isinstance(msg, ExchangeWeightMessage):
            ewmsg = msg
            self._inventoryWeight = ewmsg.currentWeight
            self._inventoryMaxWeight = ewmsg.maxWeight
            KernelEventsManager().send(KernelEvent.ExchangeWeight, ewmsg.currentWeight, ewmsg.maxWeight)
            return True

        elif isinstance(msg, ExchangeStartOkMountMessage):
            esokmmsg = msg
            # TooltipManager.hideAll()
            self.initializeMountLists(esokmmsg.stabledMountsDescription, esokmmsg.paddockedMountsDescription)
            Kernel().worker.addFrame(self._mountDialogFrame)
            return True

        elif isinstance(msg, MountSetMessage):
            if PlayedCharacterManager().mount:
                autopilotBehaviorId = 10
                behaviors = msg.mountData.behaviors
                mountIsNowAutoTripable = False
                mountWasNotAutoTripable = True
                if behaviors and autopilotBehaviorId in behaviors:
                    mountIsNowAutoTripable = True
                if PlayedCharacterManager().mount.ability:
                    for ability in PlayedCharacterManager().mount.ability:
                        if ability.id == autopilotBehaviorId:
                            mountWasNotAutoTripable = False
                if mountWasNotAutoTripable and mountIsNowAutoTripable:
                    autopilotMessage = I18n.getUiText("ui.mountTrip.autopilotActivated", [msg.mountData.name])
                    Logger().warning(autopilotMessage)
                    # commonMod = UiModuleManager().getModule("Ankama_Common").mainClass
                    # commonMod.openPopup(I18n.getUiText("ui.common.congratulation"), autopilotMessage, [I18n.getUiText("ui.common.ok")])
            PlayedCharacterManager().mount = MountData.makeMountData(msg.mountData, False, self.mountXpRatio)
            KernelEventsManager().send(KernelEvent.MountSet)
            return True

        elif isinstance(msg, MountUnSetMessage):
            PlayedCharacterManager().mount = None
            KernelEventsManager().send(KernelEvent.MountUnSet)
            return True

        elif isinstance(msg, ExchangeStartOkMountWithOutPaddockMessage):
            esomwopmsg = msg
            self.initializeMountLists(esomwopmsg.stabledMountsDescription, None)
            Kernel().worker.addFrame(self._mountDialogFrame)
            return True

        if isinstance(msg, UpdateMountCharacteristicsMessage):
            umbmsg = msg
            isInPaddock = True
            mountToUpdate = None

            for m in self._paddockList:
                if m.id == umbmsg.rideId:
                    mountToUpdate = m
                    break

            if not mountToUpdate:
                for m in self._stableList:
                    if m.id == umbmsg.rideId:
                        mountToUpdate = m
                        isInPaddock = False
                        break

            if not mountToUpdate:
                Logger().error(f"Can't find {umbmsg.rideId} ride ID for update mount boost")
                return True

            for boost in umbmsg.boostToUpdateList:
                if isinstance(boost, UpdateMountIntegerCharacteristic):
                    intBoost = boost
                    if intBoost.type == MountCharacteristicEnum.ENERGY:
                        mountToUpdate.energy = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.LOVE:
                        mountToUpdate.love = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.MATURITY:
                        mountToUpdate.maturity = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.SERENITY:
                        mountToUpdate.serenity = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.STAMINA:
                        mountToUpdate.stamina = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.TIREDNESS:
                        mountToUpdate.boostLimiter = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.CARRIER:
                        mountToUpdate.isRideable = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.PREGNANT:
                        if intBoost.value == 0:
                            mountToUpdate.fecondationTime = intBoost.value
                    elif intBoost.type == MountCharacteristicEnum.FERTILE:
                        mountToUpdate.isFecondationReady = intBoost.value

            if isInPaddock:
                KernelEventsManager().send(KernelEvent.MountStableUpdate, None, self._paddockList, None)
            else:
                KernelEventsManager().send(KernelEvent.MountStableUpdate, self._stableList, None, None)
            return True

        elif isinstance(msg, MountEmoteIconUsedOkMessage):
            meiuomsg = msg
            mountSprite = DofusEntities.getEntity(meiuomsg.mountId)

            if mountSprite:
                animationName = None
                if meiuomsg.reactionType == 1:
                    animationName = "AnimEmoteRest_Statique"
                elif meiuomsg.reactionType == 2:
                    animationName = "AnimAttaque0"
                elif meiuomsg.reactionType == 3:
                    animationName = "AnimEmoteCaresse"
                elif meiuomsg.reactionType == 4:
                    animationName = "AnimEmoteReproductionF"
                elif meiuomsg.reactionType == 5:
                    animationName = "AnimEmoteReproductionM"

                if animationName:
                    # seq = SerialSequencer()
                    # seq.addStep(PlayAnimationStep(mountSprite, animationName, False))
                    # seq.addStep(SetAnimationStep(mountSprite, AnimationEnum.ANIM_STATIQUE))
                    # seq.start()
                    pass

        elif isinstance(msg, ExchangeMountsTakenFromPaddockMessage):
            emtfpmsg = msg
            takenMessage = I18n.getUiText(
                "ui.mount.takenFromPaddock",
                [emtfpmsg.name, f"[{emtfpmsg.worldX}, {emtfpmsg.worldY}]", emtfpmsg.ownername],
            )
            Logger().info(takenMessage)
            KernelEventsManager().send(
                KernelEvent.TextInformation,
                takenMessage,
                ChatActivableChannelsEnum.PSEUDO_CHANNEL_INFO,
                TimeManager().getTimestamp(),
            )
            return True

        elif isinstance(msg, MountReleasedMessage):
            mremsg = msg
            KernelEventsManager().send(KernelEvent.MountReleased, mremsg.mountId)
            return True

        return False

    @property
    def inventoryWeight(self):
        return self._inventoryWeight

    @property
    def inventoryMaxWeight(self):
        return self._inventoryMaxWeight
