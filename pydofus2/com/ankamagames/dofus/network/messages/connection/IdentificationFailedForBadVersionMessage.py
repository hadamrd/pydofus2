from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationFailedMessage import \
    IdentificationFailedMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.version.Version import \
        Version


class IdentificationFailedForBadVersionMessage(IdentificationFailedMessage):
    requiredVersion: "Version"

    def init(self, requiredVersion_: "Version", reason_: int):
        self.requiredVersion = requiredVersion_

        super().init(reason_)
