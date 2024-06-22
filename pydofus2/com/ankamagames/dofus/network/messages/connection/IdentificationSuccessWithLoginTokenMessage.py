from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationSuccessMessage import (
    IdentificationSuccessMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import AccountTagInformation


class IdentificationSuccessWithLoginTokenMessage(IdentificationSuccessMessage):
    loginToken: str

    def init(
        self,
        loginToken_: str,
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
        self.loginToken = loginToken_

        super().init(
            login_,
            accountTag_,
            accountId_,
            communityId_,
            accountCreation_,
            subscriptionEndDate_,
            havenbagAvailableRoom_,
            hasRights_,
            hasReportRight_,
            hasForceRight_,
            wasAlreadyConnected_,
        )
