from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.common.AbstractPlayerSearchInformation import \
    AbstractPlayerSearchInformation

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import \
        AccountTagInformation


class PlayerSearchTagInformation(AbstractPlayerSearchInformation):
    tag: "AccountTagInformation"

    def init(self, tag_: "AccountTagInformation"):
        self.tag = tag_

        super().init()
