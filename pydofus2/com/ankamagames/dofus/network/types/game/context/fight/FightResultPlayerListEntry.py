from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultFighterListEntry import (
    FightResultFighterListEntry,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightLoot import FightLoot
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultAdditionalData import (
        FightResultAdditionalData,
    )


class FightResultPlayerListEntry(FightResultFighterListEntry):
    level: int
    additional: list["FightResultAdditionalData"]

    def init(
        self,
        level_: int,
        additional_: list["FightResultAdditionalData"],
        id_: int,
        alive_: bool,
        outcome_: int,
        wave_: int,
        rewards_: "FightLoot",
    ):
        self.level = level_
        self.additional = additional_

        super().init(id_, alive_, outcome_, wave_, rewards_)
