from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyMemberRemoveMessage import (
    PartyMemberRemoveMessage,
)


class PartyMemberEjectedMessage(PartyMemberRemoveMessage):
    kickerId: int

    def init(self, kickerId_: int, leavingPlayerId_: int, partyId_: int):
        self.kickerId = kickerId_

        super().init(leavingPlayerId_, partyId_)
