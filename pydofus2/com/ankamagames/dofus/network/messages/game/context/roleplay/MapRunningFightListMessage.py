from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightExternalInformations import \
        FightExternalInformations


class MapRunningFightListMessage(NetworkMessage):
    fights: list["FightExternalInformations"]

    def init(self, fights_: list["FightExternalInformations"]):
        self.fights = fights_

        super().__init__()
