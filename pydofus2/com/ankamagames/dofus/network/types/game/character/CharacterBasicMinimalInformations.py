from pydofus2.com.ankamagames.dofus.network.types.game.character.AbstractCharacterInformation import (
    AbstractCharacterInformation,
)


class CharacterBasicMinimalInformations(AbstractCharacterInformation):
    name: str

    def init(self, name_: str, id_: int):
        self.name = name_

        super().init(id_)
