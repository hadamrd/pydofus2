from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationMessage import IdentificationMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.version.Version import Version


class IdentificationAccountForceMessage(IdentificationMessage):
    forcerAccountLogin: str

    def init(
        self,
        forcerAccountLogin_: str,
        version_: "Version",
        lang_: str,
        credentials_: list[int],
        serverId_: int,
        sessionOptionalSalt_: int,
        failedAttempts_: list[int],
        autoconnect_: bool,
        useCertificate_: bool,
        useLoginToken_: bool,
    ):
        self.forcerAccountLogin = forcerAccountLogin_

        super().init(
            version_,
            lang_,
            credentials_,
            serverId_,
            sessionOptionalSalt_,
            failedAttempts_,
            autoconnect_,
            useCertificate_,
            useLoginToken_,
        )
