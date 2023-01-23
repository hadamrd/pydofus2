from datetime import datetime
import json
import os
from pydofus2.com.ankamagames.dofus import Constants
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.network.enums.GameContextEnum import GameContextEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextCreateMessage import (
    GameContextCreateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.ObjectAveragePricesErrorMessage import (
    ObjectAveragePricesErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.ObjectAveragePricesGetMessage import (
    ObjectAveragePricesGetMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.ObjectAveragePricesMessage import (
    ObjectAveragePricesMessage,
)
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
logger = Logger("Dofus2")

class PricesData(object):
    
    def __init__(self):
        self.lastUpdate: datetime = datetime.now()
        self.items =  dict[int, float]()
        
class AveragePricesFrame(Frame):

    def __init__(self):
        super().__init__()
        self._pricesData = []
        self._serverName = PlayerManager().server.name
        self.averagePricesPath = Constants.AVERAGE_PRICES_PATH
        self.askDataTimer = None
        self.nbrAsked = 0

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def dataAvailable(self) -> bool:
        return self._pricesData

    @property
    def pricesData(self) -> object:
        return self._pricesData

    def pushed(self) -> bool:
        if os.path.exists(self.averagePricesPath):
            self._pricesData = json.load(open(self.averagePricesPath, "r"))
        return True

    def pulled(self) -> bool:
        if self.askDataTimer:
            self.askDataTimer.cancel()
        self._pricesData.clear()
        return True

    def process(self, pMsg: Message) -> bool:
        if isinstance(pMsg, GameContextCreateMessage):
            gccm = pMsg
            if gccm.context == GameContextEnum.ROLE_PLAY and self.updateAllowed():
                self.askPricesData()
            return False
        if isinstance(pMsg, ObjectAveragePricesMessage):
            if self.askDataTimer:
                self.askDataTimer.cancel()
            oapm = pMsg
            self.updatePricesData(oapm.ids, oapm.avgPrices)
            return True
        if isinstance(pMsg, ObjectAveragePricesErrorMessage):           
            logger.error("Error while getting average prices!")
            return True
        else:
            return False

    def updatePricesData(self, pItemsIds: list[int], pItemsAvgPrices: list[float]) -> None:
        self._pricesData = PricesData()
        for itemId, averagePrice in zip(pItemsIds, pItemsAvgPrices):
            self._pricesData.items[itemId] = averagePrice
        if not os.path.exists(os.path.dirname(self.averagePricesPath)):
            os.makedirs(os.path.dirname(self.averagePricesPath))
        json.dump(self._pricesData, open(self.averagePricesPath, "w"))

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

    def askPricesData(self) -> None:
        oapgm: ObjectAveragePricesGetMessage = ObjectAveragePricesGetMessage()
        oapgm.init()
        ConnectionsHandler()._conn.send(oapgm)