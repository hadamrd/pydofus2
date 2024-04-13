from pydofus2.com.ankamagames.dofus.network.types.common.basic.StatisticData import StatisticData


class StatisticDataByte(StatisticData):
    value: int

    def init(self, value_: int):
        self.value = value_

        super().init()
