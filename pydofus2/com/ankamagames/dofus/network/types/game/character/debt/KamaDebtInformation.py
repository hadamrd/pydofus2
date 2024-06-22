from pydofus2.com.ankamagames.dofus.network.types.game.character.debt.DebtInformation import DebtInformation


class KamaDebtInformation(DebtInformation):
    kamas: int

    def init(self, kamas_: int, id_: int, timestamp_: int):
        self.kamas = kamas_

        super().init(id_, timestamp_)
