from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.spellmodifier.SpellModifierMessage import (
        SpellModifierMessage,
    )


class ApplySpellModifierMessage(NetworkMessage):
    actorId: int
    modifier: "SpellModifierMessage"

    def init(self, actorId_: int, modifier_: "SpellModifierMessage"):
        self.actorId = actorId_
        self.modifier = modifier_

        super().__init__()
