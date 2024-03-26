from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import \
        AccountTagInformation


class AcquaintanceSearchMessage(NetworkMessage):
    tag: "AccountTagInformation"

    def init(self, tag_: "AccountTagInformation"):
        self.tag = tag_

        super().__init__()
