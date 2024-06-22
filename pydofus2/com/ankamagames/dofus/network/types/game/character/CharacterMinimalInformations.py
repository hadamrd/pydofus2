from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterBasicMinimalInformations import (
    CharacterBasicMinimalInformations,
)


class CharacterMinimalInformations(CharacterBasicMinimalInformations):
    level: int

    def init(self, level_: int, name_: str, id_: int):
        self.level = level_

        super().init(name_, id_)
