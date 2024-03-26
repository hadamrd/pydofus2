from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.network.enums.AlignmentSideEnum import \
    AlignmentSideEnum
from pydofus2.com.ankamagames.dofus.network.enums.AlignmentWarEffortDonationResultEnum import \
    AlignmentWarEffortDonationResultEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.character.alignment.war.effort.AlignmentWarEffortDonateRequestMessage import \
    AlignmentWarEffortDonateRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.alignment.war.effort.AlignmentWarEffortDonationResultMessage import \
    AlignmentWarEffortDonationResultMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.alignment.war.effort.CharacterAlignmentWarEffortProgressionMessage import \
    CharacterAlignmentWarEffortProgressionMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.alignment.war.effort.CharacterAlignmentWarEffortProgressionRequestMessage import \
    CharacterAlignmentWarEffortProgressionRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.alignment.war.effort.AlignmentWarEffortProgressionMessage import \
    AlignmentWarEffortProgressionMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.alignment.war.effort.AlignmentWarEffortProgressionRequestMessage import \
    AlignmentWarEffortProgressionRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.pvp.AlignmentRankUpdateMessage import \
    AlignmentRankUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.pvp.SetEnablePVPRequestMessage import \
    SetEnablePVPRequestMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class AlignmentFrame(Frame):

    def __init__(self):
        super().__init__()
        self._alignmentRank = -1

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def pulled(sef):
        return True

    @property
    def playerRank(self):
        return self._alignmentRank

    def setEnablePVPRequest(self, enable: bool):
        seprmsg = SetEnablePVPRequestMessage()
        seprmsg.init(enable)
        ConnectionsHandler().send(seprmsg)

    def characterAlignmentWarEffortProgressionRequest(self):
        caweprm = CharacterAlignmentWarEffortProgressionRequestMessage()
        ConnectionsHandler().send(caweprm)

    def alignmentWarEffortProgressionRequest(self):
        aweprm = AlignmentWarEffortProgressionRequestMessage()
        ConnectionsHandler().send(aweprm)

    def alignmentWarEffortDonateAction(self, donation):
        awedrqm = AlignmentWarEffortDonateRequestMessage()
        awedrqm.init(donation)
        ConnectionsHandler().send(awedrqm)

    def process(self, msg) -> bool:

        if isinstance(msg, AlignmentRankUpdateMessage):
            arumsg = msg
            self._alignmentRank = arumsg.alignmentRank
            if arumsg.verbose:
                KernelEventsManager().send(KernelEvent.AlignmentRankUpdate, arumsg.alignmentRank)
            return True

        elif isinstance(msg, CharacterAlignmentWarEffortProgressionMessage):
            cawepm = msg
            KernelEventsManager().send(
                KernelEvent.CharacterAlignmentWarEffortProgressionHook,
                cawepm.alignmentWarEffortDailyLimit,
                cawepm.alignmentWarEffortDailyDonation,
                cawepm.alignmentWarEffortPersonalDonation,
            )
            return True

        elif isinstance(msg, AlignmentWarEffortProgressionMessage):
            awepm = msg
            bontaParticipation = 0
            brakmarParticipation = 0
            for ainfo in awepm.effortProgressions:
                if ainfo.alignmentSide == AlignmentSideEnum.ALIGNMENT_ANGEL:
                    bontaParticipation = ainfo.alignmentWarEffort
                if ainfo.alignmentSide == AlignmentSideEnum.ALIGNMENT_EVIL:
                    brakmarParticipation = ainfo.alignmentWarEffort
            KernelEventsManager().send(
                KernelEvent.AlignmentWarEffortProgressionMessageHook, bontaParticipation, brakmarParticipation
            )
            return True

        elif isinstance(msg, AlignmentWarEffortDonationResultMessage):
            awedrm = msg
            if awedrm.result == AlignmentWarEffortDonationResultEnum.WAR_EFFORT_DONATION_SUCCESS:
                KernelEventsManager().send(KernelEvent.UpdateWarEffortHook)
            return True

        else:
            return False
