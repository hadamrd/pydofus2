from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import \
        AccountTagInformation


class IdentificationSuccessMessage(NetworkMessage):
    login: str
    accountTag: "AccountTagInformation"
    accountId: int
    communityId: int
    accountCreation: int
    subscriptionEndDate: int
    havenbagAvailableRoom: int
    hasRights: bool
    hasReportRight: bool
    hasForceRight: bool
    wasAlreadyConnected: bool
    hasRights: bool
    hasForceRight: bool
    wasAlreadyConnected: bool

    def init(
        self,
        login_: str,
        accountTag_: "AccountTagInformation",
        accountId_: int,
        communityId_: int,
        accountCreation_: int,
        subscriptionEndDate_: int,
        havenbagAvailableRoom_: int,
        hasRights_: bool,
        hasReportRight_: bool,
        hasForceRight_: bool,
        wasAlreadyConnected_: bool,
    ):
        self.login = login_
        self.accountTag = accountTag_
        self.accountId = accountId_
        self.communityId = communityId_
        self.accountCreation = accountCreation_
        self.subscriptionEndDate = subscriptionEndDate_
        self.havenbagAvailableRoom = havenbagAvailableRoom_
        self.hasRights = hasRights_
        self.hasReportRight = hasReportRight_
        self.hasForceRight = hasForceRight_
        self.wasAlreadyConnected = wasAlreadyConnected_

        super().__init__()
