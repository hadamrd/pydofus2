from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicDetailed import \
        CharacterCharacteristicDetailed


class CharacterSpellModification(NetworkMessage):
    modificationType: int
    spellId: int
    value: "CharacterCharacteristicDetailed"

    def init(self, modificationType_: int, spellId_: int, value_: "CharacterCharacteristicDetailed"):
        self.modificationType = modificationType_
        self.spellId = spellId_
        self.value = value_

        super().__init__()
