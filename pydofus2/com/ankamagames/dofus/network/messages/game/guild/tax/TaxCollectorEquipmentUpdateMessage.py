from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristics import \
        CharacterCharacteristics
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem


class TaxCollectorEquipmentUpdateMessage(NetworkMessage):
    uniqueId: int
    object: "ObjectItem"
    added: bool
    characteristics: "CharacterCharacteristics"

    def init(self, uniqueId_: int, object_: "ObjectItem", added_: bool, characteristics_: "CharacterCharacteristics"):
        self.uniqueId = uniqueId_
        self.object = object_
        self.added = added_
        self.characteristics = characteristics_

        super().__init__()
