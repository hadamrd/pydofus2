from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.idol.Idol import \
        Idol


class IdolFightPreparationUpdateMessage(NetworkMessage):
    idolSource: int
    idols: list["Idol"]

    def init(self, idolSource_: int, idols_: list["Idol"]):
        self.idolSource = idolSource_
        self.idols = idols_

        super().__init__()
