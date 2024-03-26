from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AbstractPlayerSearchInformation import \
        AbstractPlayerSearchInformation


class BasicWhoIsNoMatchMessage(NetworkMessage):
    target: "AbstractPlayerSearchInformation"

    def init(self, target_: "AbstractPlayerSearchInformation"):
        self.target = target_

        super().__init__()
