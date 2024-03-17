from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.chat.ChatClientMultiMessage import \
    ChatClientMultiMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem
    

class ChatClientMultiWithObjectMessage(ChatClientMultiMessage):
    objects: list['ObjectItem']
    def init(self, objects_: list['ObjectItem'], channel_: int, content_: str):
        self.objects = objects_
        
        super().init(channel_, content_)
    