from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.idol.PartyIdol import \
        PartyIdol


class IdolPartyRefreshMessage(NetworkMessage):
    partyIdol: "PartyIdol"

    def init(self, partyIdol_: "PartyIdol"):
        self.partyIdol = partyIdol_

        super().__init__()
