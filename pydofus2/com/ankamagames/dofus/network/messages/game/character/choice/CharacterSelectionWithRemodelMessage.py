from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectionMessage import (
    CharacterSelectionMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.choice.RemodelingInformation import (
        RemodelingInformation,
    )


class CharacterSelectionWithRemodelMessage(CharacterSelectionMessage):
    remodel: "RemodelingInformation"

    def init(self, remodel_: "RemodelingInformation", id_: int):
        self.remodel = remodel_

        super().init(id_)
