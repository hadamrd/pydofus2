from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.chat.ChatAbstractClientMessage import \
    ChatAbstractClientMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AbstractPlayerSearchInformation import \
        AbstractPlayerSearchInformation
    

class ChatClientPrivateMessage(ChatAbstractClientMessage):
    receiver: 'AbstractPlayerSearchInformation'
    def init(self, receiver_: 'AbstractPlayerSearchInformation', content_: str):
        self.receiver = receiver_
        
        super().init(content_)
    