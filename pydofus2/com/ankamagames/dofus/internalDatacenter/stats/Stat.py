from pydofus2.com.ankamagames.dofus.datacenter.characteristics.Characteristic import \
    Characteristic


class Stat:

    UNKNOWN_STAT_NAME: str = "unknown"

    def __init__(self, id: float, totalValue: float):
        self._id = id
        self._totalValue = totalValue
        self._name = self.getStatName()
        self._entityId: float = None

    def getStatName(self) -> str:
        characteristic: Characteristic = Characteristic.getCharacteristicById(self._id)
        if characteristic is not None:
            return characteristic.keyword
        return self.UNKNOWN_STAT_NAME

    @property
    def entityId(self) -> float:
        return self._entityId

    @entityId.setter
    def entityId(self, entityId: float) -> None:
        self._entityId = entityId

    @property
    def id(self) -> float:
        return self._id

    @property
    def totalValue(self) -> float:
        return self._totalValue

    @totalValue.setter
    def totalValue(self, value: float) -> None:
        self._totalValue = value

    def __str__(self) -> str:
        return self.getFormattedMessage("total: " + str(self._totalValue))

    def reset(self) -> None:
        self._totalValue = 0

    def getFormattedMessage(self, message: str) -> str:
        return (
            "Stat"
            + " "
            + self._name
            + " (Entity ID: "
            + str(self._entityId)
            + ", ID: "
            + str(self._id)
            + "): "
            + message
        )
