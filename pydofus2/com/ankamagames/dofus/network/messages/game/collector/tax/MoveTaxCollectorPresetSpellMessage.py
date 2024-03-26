from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.uuid import Uuid


class MoveTaxCollectorPresetSpellMessage(NetworkMessage):
    presetId: "Uuid"
    movedFrom: int
    movedTo: int

    def init(self, presetId_: "Uuid", movedFrom_: int, movedTo_: int):
        self.presetId = presetId_
        self.movedFrom = movedFrom_
        self.movedTo = movedTo_

        super().__init__()
