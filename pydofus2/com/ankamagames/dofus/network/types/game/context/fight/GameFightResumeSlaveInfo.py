from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightSpellCooldown import (
        GameFightSpellCooldown,
    )


class GameFightResumeSlaveInfo(NetworkMessage):
    slaveId: int
    spellCooldowns: list["GameFightSpellCooldown"]
    summonCount: int
    bombCount: int

    def init(self, slaveId_: int, spellCooldowns_: list["GameFightSpellCooldown"], summonCount_: int, bombCount_: int):
        self.slaveId = slaveId_
        self.spellCooldowns = spellCooldowns_
        self.summonCount = summonCount_
        self.bombCount = bombCount_

        super().__init__()
