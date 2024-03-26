from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.chat.ChatServerCopyMessage import \
    ChatServerCopyMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem


class ChatServerCopyWithObjectMessage(ChatServerCopyMessage):
    objects: list["ObjectItem"]

    def init(
        self,
        objects_: list["ObjectItem"],
        receiverId_: int,
        receiverName_: str,
        channel_: int,
        content_: str,
        timestamp_: int,
        fingerprint_: str,
    ):
        self.objects = objects_

        super().init(receiverId_, receiverName_, channel_, content_, timestamp_, fingerprint_)
