from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterBasicMinimalInformations import (
        CharacterBasicMinimalInformations,
    )


class ArenaFighterLeaveMessage(NetworkMessage):
    leaver: "CharacterBasicMinimalInformations"

    def init(self, leaver_: "CharacterBasicMinimalInformations"):
        self.leaver = leaver_

        super().__init__()
