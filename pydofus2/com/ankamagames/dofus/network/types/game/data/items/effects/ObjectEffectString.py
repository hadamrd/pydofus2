from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import ObjectEffect


class ObjectEffectString(ObjectEffect):
    value: str

    def init(self, value_: str, actionId_: int):
        self.value = value_

        super().init(actionId_)
