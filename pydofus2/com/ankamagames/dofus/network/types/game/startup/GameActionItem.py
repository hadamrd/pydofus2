from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemInformationWithQuantity import (
        ObjectItemInformationWithQuantity,
    )


class GameActionItem(NetworkMessage):
    uid: int
    title: str
    text: str
    descUrl: str
    pictureUrl: str
    items: list["ObjectItemInformationWithQuantity"]

    def init(
        self,
        uid_: int,
        title_: str,
        text_: str,
        descUrl_: str,
        pictureUrl_: str,
        items_: list["ObjectItemInformationWithQuantity"],
    ):
        self.uid = uid_
        self.title = title_
        self.text = text_
        self.descUrl = descUrl_
        self.pictureUrl = pictureUrl_
        self.items = items_

        super().__init__()
