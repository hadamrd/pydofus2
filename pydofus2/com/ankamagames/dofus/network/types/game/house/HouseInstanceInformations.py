from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import AccountTagInformation


class HouseInstanceInformations(NetworkMessage):
    instanceId: int
    ownerTag: "AccountTagInformation"
    price: int
    secondHand: bool
    isLocked: bool
    hasOwner: bool
    isSaleLocked: bool
    isAdminLocked: bool
    secondHand: bool
    isLocked: bool
    hasOwner: bool
    isSaleLocked: bool
    isAdminLocked: bool

    def init(
        self,
        instanceId_: int,
        ownerTag_: "AccountTagInformation",
        price_: int,
        secondHand_: bool,
        isLocked_: bool,
        hasOwner_: bool,
        isSaleLocked_: bool,
        isAdminLocked_: bool,
    ):
        self.instanceId = instanceId_
        self.ownerTag = ownerTag_
        self.price = price_
        self.secondHand = secondHand_
        self.isLocked = isLocked_
        self.hasOwner = hasOwner_
        self.isSaleLocked = isSaleLocked_
        self.isAdminLocked = isAdminLocked_

        super().__init__()
