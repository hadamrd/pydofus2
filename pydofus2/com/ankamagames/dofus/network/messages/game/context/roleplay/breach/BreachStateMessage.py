from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import (
        CharacterMinimalInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectInteger import (
        ObjectEffectInteger,
    )


class BreachStateMessage(NetworkMessage):
    owner: "CharacterMinimalInformations"
    bonuses: list["ObjectEffectInteger"]
    bugdet: int
    saved: bool

    def init(
        self, owner_: "CharacterMinimalInformations", bonuses_: list["ObjectEffectInteger"], bugdet_: int, saved_: bool
    ):
        self.owner = owner_
        self.bonuses = bonuses_
        self.bugdet = bugdet_
        self.saved = saved_

        super().__init__()
