from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultFighterListEntry import \
    FightResultFighterListEntry

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightLoot import \
        FightLoot


class FightResultMutantListEntry(FightResultFighterListEntry):
    level: int

    def init(self, level_: int, id_: int, alive_: bool, outcome_: int, wave_: int, rewards_: "FightLoot"):
        self.level = level_

        super().init(id_, alive_, outcome_, wave_, rewards_)
