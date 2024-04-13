from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.prism.PrismFightersInformation import (
        PrismFightersInformation,
    )


class PrismsInfoValidMessage(NetworkMessage):
    fights: list["PrismFightersInformation"]

    def init(self, fights_: list["PrismFightersInformation"]):
        self.fights = fights_

        super().__init__()
