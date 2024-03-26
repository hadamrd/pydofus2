from pydofus2.com.ankamagames.dofus.network.types.game.rank.RankMinimalInformation import \
    RankMinimalInformation


class RankPublicInformation(RankMinimalInformation):
    order: int
    gfxId: int

    def init(self, order_: int, gfxId_: int, id_: int, name_: str):
        self.order = order_
        self.gfxId = gfxId_

        super().init(id_, name_)
