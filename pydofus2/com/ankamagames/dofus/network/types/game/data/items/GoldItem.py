from pydofus2.com.ankamagames.dofus.network.types.game.data.items.Item import Item


class GoldItem(Item):
    sum: int

    def init(self, sum_: int):
        self.sum = sum_

        super().init()
