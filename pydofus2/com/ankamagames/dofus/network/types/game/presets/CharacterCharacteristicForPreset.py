from pydofus2.com.ankamagames.dofus.network.types.game.presets.SimpleCharacterCharacteristicForPreset import \
    SimpleCharacterCharacteristicForPreset


class CharacterCharacteristicForPreset(SimpleCharacterCharacteristicForPreset):
    stuff: int

    def init(self, stuff_: int, keyword_: str, base_: int, additionnal_: int):
        self.stuff = stuff_

        super().init(keyword_, base_, additionnal_)
