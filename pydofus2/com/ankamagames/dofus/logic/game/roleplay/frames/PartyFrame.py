from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.network.enums.PartyJoinErrorEnum import PartyJoinErrorEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.atlas.compass.CompassUpdatePartyMemberMessage import (
    CompassUpdatePartyMemberMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyAcceptInvitationMessage import (
    PartyAcceptInvitationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyCancelInvitationMessage import (
    PartyCancelInvitationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyCancelInvitationNotificationMessage import (
    PartyCancelInvitationNotificationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyCannotJoinErrorMessage import (
    PartyCannotJoinErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyDeletedMessage import (
    PartyDeletedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyFollowMemberRequestMessage import (
    PartyFollowMemberRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyInvitationMessage import (
    PartyInvitationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyInvitationRequestMessage import (
    PartyInvitationRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyJoinMessage import (
    PartyJoinMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyLeaveRequestMessage import (
    PartyLeaveRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyMemberInStandardFightMessage import (
    PartyMemberInStandardFightMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyMemberRemoveMessage import (
    PartyMemberRemoveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyNewGuestMessage import (
    PartyNewGuestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyNewMemberMessage import (
    PartyNewMemberMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyRefuseInvitationMessage import (
    PartyRefuseInvitationMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.common.PlayerSearchCharacterNameInformation import (
    PlayerSearchCharacterNameInformation,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyMemberInformations import (
    PartyMemberInformations,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class PartyFrame(Frame):
    ASK_INVITE_TIMOUT = 20
    CONFIRME_JOIN_TIMEOUT = 20

    def __init__(self) -> None:
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pulled(self):
        KernelEventsManager().clearAllByOrigin(self)
        self.leaveParty()
        self.partyMembers.clear()
        self.currentPartyId = None
        return True

    def pushed(self):
        self.currentPartyId = None
        self.partyMembers = dict[int, PartyMemberInformations]()
        return True

    def getMemberById(self, guestId: int) -> PartyMemberInformations:
        return self.partyMembers.get(guestId)

    def getMemberByName(self, name: str) -> PartyMemberInformations:
        for member in self.partyMembers.values():
            if member.name == name:
                return member
        return None

    def sendPartyInviteCancel(self, guestId):
        cpimsg = PartyCancelInvitationMessage()
        cpimsg.init(guestId, self.currentPartyId)
        ConnectionsHandler().send(cpimsg)

    def sendPartyInviteRequest(self, playerName):
        pimsg = PartyInvitationRequestMessage()
        pscni = PlayerSearchCharacterNameInformation()
        pscni.init(playerName)
        pimsg.init(pscni)
        ConnectionsHandler().send(pimsg)
        Logger().debug(f"Join party invitation sent to {playerName}")

    def sendFollowMember(self, memberId):
        pfmrm = PartyFollowMemberRequestMessage()
        pfmrm.init(memberId, self.currentPartyId)
        ConnectionsHandler().send(pfmrm)

    def leaveParty(self):
        if self.currentPartyId is None:
            return
        plmsg = PartyLeaveRequestMessage()
        plmsg.init(self.currentPartyId)
        ConnectionsHandler().send(plmsg)

    def sendRefusePartyinvite(self, partyId):
        pirmsg = PartyRefuseInvitationMessage()
        pirmsg.init(partyId)
        ConnectionsHandler().send(pirmsg)

    def sendAcceptPartyInvite(self, partyId):
        paimsg = PartyAcceptInvitationMessage()
        paimsg.init(partyId)
        ConnectionsHandler().send(paimsg)

    def process(self, msg: Message):

        if isinstance(msg, PartyNewGuestMessage):
            return True

        elif isinstance(msg, PartyMemberRemoveMessage):
            Logger().debug(f"{member.name} left the party")
            member = self.getMemberById(msg.leavingPlayerId)
            if member:
                del self.partyMembers[msg.leavingPlayerId]
            KernelEventsManager().send(KernelEvent.MemberLeftParty, member)
            return True

        elif isinstance(msg, PartyDeletedMessage):
            Logger().debug(f"party deleted")
            self.currentPartyId = None
            self.partyMembers.clear()
            KernelEventsManager().send(KernelEvent.PartyDeleted, msg.partyId)
            return True

        elif isinstance(msg, PartyInvitationMessage):
            notifText = (
                I18n.getUiText("ui.common.invitation")
                + " "
                + I18n.getUiText("ui.party.playerInvitation", [f"player,{msg.fromId}::{msg.fromName}"])
            )
            Logger().debug(f"{notifText}.")
            KernelEventsManager().send(KernelEvent.PartyInvited, msg.partyId, msg.partyType, msg.fromId, msg.fromName)
            return True

        elif isinstance(msg, PartyNewMemberMessage):
            member = msg.memberInformations
            Logger().info(f"Member ({member.name}) joined the party.")
            self.currentPartyId = msg.partyId
            self.partyMembers[member.id] = member
            KernelEventsManager().send(KernelEvent.MemberJoinedParty, msg.partyId, msg.memberInformations)
            return True

        elif isinstance(msg, PartyJoinMessage):
            Logger().info(f"Player joined Party ({msg.partyId}) of leader ({msg.partyLeaderId})")
            self.partyMembers.clear()
            self.currentPartyId = msg.partyId
            for member in msg.members:
                self.partyMembers[member.id] = member
            KernelEventsManager().send(KernelEvent.IJoinedParty, msg.partyId, msg.members)
            return True

        elif isinstance(msg, CompassUpdatePartyMemberMessage):
            if msg.memberId in self.partyMembers:
                member = self.partyMembers[msg.memberId]
                member.worldX = msg.coords.worldX
                member.worldY = msg.coords.worldY
                legend = (
                    I18n.getUiText("ui.cartography.positionof", [member.name])
                    + f" ({msg.coords.worldX}, {msg.coords.worldY})"
                )
                Logger().info(legend)
            else:
                KernelEventsManager().send(
                    KernelEvent.ClientRestart, f"Seems ig we are in party but not modeled yet in party frame"
                )
            return True

        elif isinstance(msg, PartyMemberInStandardFightMessage):
            Logger().info(f"member {msg.memberId} started fight {msg.fightId}")
            KernelEventsManager().send(KernelEvent.PartyMemberStartedFight, msg.memberId, msg.fightId)
            return True

        if isinstance(msg, PartyCannotJoinErrorMessage):
            reasonText = ""
            if msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_PARTY_FULL:
                reasonText = I18n.getUiText("ui.party.partyFull")
            elif msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_PARTY_NOT_FOUND:
                reasonText = I18n.getUiText("ui.party.cantFindParty")
            elif msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_PLAYER_BUSY:
                reasonText = I18n.getUiText("ui.party.cantInvitPlayerBusy")
            elif msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_PLAYER_NOT_FOUND:
                reasonText = I18n.getUiText("ui.common.playerNotFound", ["member"])
            elif msg.reason in (
                PartyJoinErrorEnum.PARTY_JOIN_ERROR_UNMET_CRITERION,
                PartyJoinErrorEnum.PARTY_JOIN_ERROR_PLAYER_LOYAL,
            ):
                pass
            elif msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_PLAYER_TOO_SOLLICITED:
                reasonText = I18n.getUiText("ui.party.playerTooSollicited")
            elif msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_UNMODIFIABLE:
                reasonText = I18n.getUiText("ui.party.partyUnmodifiable")
            elif msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_PLAYER_ALREADY_INVITED:
                reasonText = I18n.getUiText("ui.party.playerAlreayBeingInvited")
            elif msg.reason == PartyJoinErrorEnum.PARTY_JOIN_ERROR_NOT_ENOUGH_ROOM:
                reasonText = I18n.getUiText("ui.party.notEnoughRoom")
            elif msg.reason in (
                PartyJoinErrorEnum.PARTY_JOIN_ERROR_COMPOSITION_CHANGED,
                PartyJoinErrorEnum.PARTY_JOIN_ERROR_UNKNOWN,
            ):
                reasonText = I18n.getUiText("ui.party.cantInvit")
            Logger().warning(f"Can't join party: {reasonText}")
            KernelEventsManager().send(KernelEvent.PartyJoinFailed, msg.reason, reasonText)
            return True

        elif isinstance(msg, PartyCancelInvitationNotificationMessage):
            if msg.partyId == self.currentPartyId:
                pcinGuestName = msg.guestId
                pcinCancelerName = msg.cancelerId
                guestRefusingId = None
                for ctxid, member in self.partyMembers.items():
                    if msg.guestId == ctxid:
                        guestRefusingId = ctxid
                        pcinGuestName = member.name
                    if msg.cancelerId == ctxid:
                        pcinCancelerName = member.name
                if guestRefusingId:
                    del self.partyMembers[guestRefusingId]
                pcinText = I18n().getUiText("ui.party.invitationCancelled", [pcinCancelerName, pcinGuestName])
                Logger().warning(f"{pcinText}")
                KernelEventsManager().send(
                    KernelEvent.PartyInviteCancel, msg.partyId, msg.guestId, msg.cancelerId, pcinText
                )
                return True
