from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.character.replay.CharacterReplayRequestMessage import (
    CharacterReplayRequestMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.choice.RemodelingInformation import (
        RemodelingInformation,
    )


class CharacterReplayWithRemodelRequestMessage(CharacterReplayRequestMessage):
    remodel: "RemodelingInformation"

    def init(self, remodel_: "RemodelingInformation", characterId_: int):
        self.remodel = remodel_

        super().init(characterId_)
