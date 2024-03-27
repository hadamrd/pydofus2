import json
import os
from datetime import datetime

from pydofus2.com.ankamagames.dofus import Constants
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.network.enums.GameContextEnum import \
    GameContextEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextCreateMessage import \
    GameContextCreateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.ObjectAveragePricesErrorMessage import \
    ObjectAveragePricesErrorMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.ObjectAveragePricesGetMessage import \
    ObjectAveragePricesGetMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.ObjectAveragePricesMessage import \
    ObjectAveragePricesMessage
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import \
    BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class PricesData(object):
    def __init__(self):
        self.lastUpdate: datetime = datetime.now()
        self.items = dict[int, float]()

    def __json__(self):
        return {"lastUpdate": self.lastUpdate.isoformat(), "items": self.items}

    def __dict__(self):
        return {"lastUpdate": self.lastUpdate.isoformat(), "items": self.items}

    def clear(self):
        self.items = None
        self.lastUpdate = None


class AveragePricesFrame(Frame):
    def __init__(self):
        super().__init__()
        self._pricesData = PricesData()
        self._serverName = PlayerManager().server.name
        self.averagePricesPath = Constants.AVERAGE_PRICES_PATH
        self.askDataTimer: BenchmarkTimer = None
        self.nbrAsked = 0
        self.pricesDataAsked = False

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def dataAvailable(self) -> bool:
        return self._pricesData is not None

    @property
    def pricesData(self) -> PricesData:
        return self._pricesData

    def pushed(self) -> bool:
        if os.path.exists(self.averagePricesPath):
            try:
                json_pricesData = json.load(open(self.averagePricesPath, "r"))
                self._pricesData.items = json_pricesData["items"]
                self._pricesData.lastUpdate = datetime.fromisoformat(
                    json_pricesData["lastUpdate"]
                )
            except json.JSONDecodeError as e:
                Logger().error("Error loading JSON data:", str(e))
                with open(self.averagePricesPath, "w") as file:
                    json.dump({}, file)
                self._pricesData.items = {}
                self._pricesData.lastUpdate = datetime.now()
        return True

    def pulled(self) -> bool:
        if self.askDataTimer:
            self.askDataTimer.cancel()
        self._pricesData.clear()
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameContextCreateMessage):
            if msg.context == GameContextEnum.ROLE_PLAY and not self.pricesDataAsked:
                self.askPricesData()
            return False

        if isinstance(msg, ObjectAveragePricesMessage):
            if self.askDataTimer:
                self.askDataTimer.cancel()
            self.updatePricesData(msg.ids, msg.avgPrices)
            return True

        if isinstance(msg, ObjectAveragePricesErrorMessage):
            return True

        else:
            return False

    def updatePricesData(self, pItemsIds: list[int], pItemsAvgPrices: list[float]) -> None:
        self._pricesData = PricesData()
        self._pricesData.items = {}
        for itemId, averagePrice in zip(pItemsIds, pItemsAvgPrices):
            self._pricesData.items[itemId] = averagePrice
        if not os.path.exists(os.path.dirname(self.averagePricesPath)):
            os.makedirs(os.path.dirname(self.averagePricesPath))
        with open(self.averagePricesPath, "w") as file:
            json.dump(self._pricesData.__json__(), file, indent=4)
        Logger().debug("Average prices data received")

    def updateAllowed(self) -> bool:
        if self.dataAvailable:
            now = datetime.now()
            if (
                now.year == self._pricesData.lastUpdate.year
                and now.month == self._pricesData.lastUpdate.month
                and now.date == self._pricesData.lastUpdate.date
            ):
                return False
        return True

    def getItemAveragePrice(self, guid):
        return self._pricesData.items.get(guid)

    def askPricesData(self) -> None:
        self.pricesDataAsked = True
        oapgm: ObjectAveragePricesGetMessage = ObjectAveragePricesGetMessage()
        oapgm.init()
        ConnectionsHandler().send(oapgm)
