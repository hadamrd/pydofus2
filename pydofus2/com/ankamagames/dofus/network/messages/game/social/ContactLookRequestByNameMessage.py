from pydofus2.com.ankamagames.dofus.network.messages.game.social.ContactLookRequestMessage import (
    ContactLookRequestMessage,
)


class ContactLookRequestByNameMessage(ContactLookRequestMessage):
    playerName: str

    def init(self, playerName_: str, requestId_: int, contactType_: int):
        self.playerName = playerName_

        super().init(requestId_, contactType_)
