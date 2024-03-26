from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.chat.ChatClientPrivateMessage import \
    ChatClientPrivateMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AbstractPlayerSearchInformation import \
        AbstractPlayerSearchInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem


class ChatClientPrivateWithObjectMessage(ChatClientPrivateMessage):
    objects: list["ObjectItem"]

    def init(self, objects_: list["ObjectItem"], receiver_: "AbstractPlayerSearchInformation", content_: str):
        self.objects = objects_

        super().init(receiver_, content_)
