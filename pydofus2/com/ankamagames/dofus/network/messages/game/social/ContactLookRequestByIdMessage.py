from pydofus2.com.ankamagames.dofus.network.messages.game.social.ContactLookRequestMessage import (
    ContactLookRequestMessage,
)


class ContactLookRequestByIdMessage(ContactLookRequestMessage):
    playerId: int

    def init(self, playerId_: int, requestId_: int, contactType_: int):
        self.playerId = playerId_

        super().init(requestId_, contactType_)
