from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.friend.IgnoredInformations import IgnoredInformations


class IgnoredListMessage(NetworkMessage):
    ignoredList: list["IgnoredInformations"]

    def init(self, ignoredList_: list["IgnoredInformations"]):
        self.ignoredList = ignoredList_

        super().__init__()
