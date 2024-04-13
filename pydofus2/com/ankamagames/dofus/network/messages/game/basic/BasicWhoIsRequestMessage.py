from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AbstractPlayerSearchInformation import (
        AbstractPlayerSearchInformation,
    )


class BasicWhoIsRequestMessage(NetworkMessage):
    verbose: bool
    target: "AbstractPlayerSearchInformation"

    def init(self, verbose_: bool, target_: "AbstractPlayerSearchInformation"):
        self.verbose = verbose_
        self.target = target_

        super().__init__()
