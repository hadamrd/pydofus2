from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.communication.InfoMessage import InfoMessage
from pydofus2.com.ankamagames.dofus.misc.utils.ParamsDecoder import ParamsDecoder
from pydofus2.com.ankamagames.dofus.network.enums.TextInformationTypeEnum import TextInformationTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.basic.TextInformationMessage import TextInformationMessage
from pydofus2.com.ankamagames.dofus.network.messages.server.basic.SystemMessageDisplayMessage import (
    SystemMessageDisplayMessage,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class ChatFrame(Frame):
    CHAT_FAIL_TEXTS_IDS = [5259, 5359, 5338, 5373]

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

        if isinstance(msg, SystemMessageDisplayMessage):
            self.systemMessageDisplay(msg)
            return True

        if isinstance(msg, TextInformationMessage):
            timsg = msg
            param = []
            for iTimsg in timsg.parameters:
                param.append(iTimsg)
            params = []
            msgInfo = InfoMessage.getInfoMessageById(timsg.msgType * 10000 + timsg.msgId)
            if msgInfo:
                textId = msgInfo.textId
                if timsg.msgId == 28 or timsg.msgId == 29:
                    Logger().debug("Player is lagging")
                if param:
                    if param[0] and "~" in param[0]:
                        params = param[0].split("~")
                    else:
                        params = param
            else:
                Logger().error(f"Information message {timsg.msgType * 10000 + timsg.msgId} cannot be found.")
                if timsg.msgType == TextInformationTypeEnum.TEXT_INFORMATION_ERROR:
                    textId = InfoMessage.getInfoMessageById(10231).textId
                else:
                    textId = InfoMessage.getInfoMessageById(207).textId
                params.append(timsg.msgId)
            msgContent = I18n.getText(textId)
            if msgContent:
                msgContent = ParamsDecoder.applyParams(msgContent, params)
                Logger().info(f"text info for id {textId}, params {params}: {msgContent}")
            else:
                Logger().error(f"There's no message for id {timsg.msgType * 10000 + timsg.msgId}")
            if textId == 325840:
                KernelEventsManager().send(KernelEvent.KamasGained, int(params[0]))
            KernelEventsManager().send(KernelEvent.ServerTextInfo, msg.msgId, msg.msgType, textId, msgContent, params)
            return True

    def systemMessageDisplay(self, msg: SystemMessageDisplayMessage):
        a = msg.parameters
        if (
            InfoMessage.getInfoMessageById(40000 + msg.msgId)
            and InfoMessage.getInfoMessageById(40000 + msg.msgId).textId
        ):
            textId = InfoMessage.getInfoMessageById(40000 + msg.msgId).textId
        else:
            Logger().error("Information message " + str(40000 + msg.msgId) + " cannot be found.")
            textId = InfoMessage.getInfoMessageById(207).textId
            a = [msg.msgId]
        msgContent = I18n.getText(textId)
        if msgContent:
            msgContent = ParamsDecoder.applyParams(msgContent, a)
            Logger().warn(f"[textId {textId}] [{I18n.getUiText('ui.popup.warning')}] | {msgContent}")
        if textId == 5123:
            KernelEventsManager().send(KernelEvent.InactivityWarning)
