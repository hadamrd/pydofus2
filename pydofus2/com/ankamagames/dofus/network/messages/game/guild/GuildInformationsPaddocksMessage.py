from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.paddock.PaddockContentInformations import (
        PaddockContentInformations,
    )


class GuildInformationsPaddocksMessage(NetworkMessage):
    nbPaddockMax: int
    paddocksInformations: list["PaddockContentInformations"]

    def init(self, nbPaddockMax_: int, paddocksInformations_: list["PaddockContentInformations"]):
        self.nbPaddockMax = nbPaddockMax_
        self.paddocksInformations = paddocksInformations_

        super().__init__()
