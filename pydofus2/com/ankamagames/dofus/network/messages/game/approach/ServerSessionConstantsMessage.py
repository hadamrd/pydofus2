from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.approach.ServerSessionConstant import \
        ServerSessionConstant


class ServerSessionConstantsMessage(NetworkMessage):
    variables: list["ServerSessionConstant"]

    def init(self, variables_: list["ServerSessionConstant"]):
        self.variables = variables_

        super().__init__()
