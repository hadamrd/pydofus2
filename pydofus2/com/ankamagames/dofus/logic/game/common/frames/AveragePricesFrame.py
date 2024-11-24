import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Dict

from dataclasses_json import LetterCase, config, dataclass_json

from pydofus2.com.ankamagames.dofus import settings
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
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

pricesDataLock = Lock()


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PricesData:
    lastUpdate: datetime = field(metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat))
    items: Dict[int, float] = field(default_factory=dict)

    def getItemPrice(self, gid):
        return self.items.get(str(gid))


class AveragePricesFrame(Frame):
    _pricesData: Dict[str, PricesData] = {}

    def __init__(self):
        super().__init__()
        if not AveragePricesFrame._pricesData:
            if os.path.exists(settings.AVERAGE_PRICES_PATH):
                try:
                    with open(settings.AVERAGE_PRICES_PATH, "r") as file:
                        data: Dict = json.load(file)
                        with pricesDataLock:
                            for server, prices_data in data.items():
                                prices_data["lastUpdate"] = datetime.fromisoformat(prices_data["lastUpdate"])
                                AveragePricesFrame._pricesData[server] = PricesData(**prices_data)
                                Logger().info(
                                    f"Loaded average prices for server '{server}', last updated {prices_data['lastUpdate']}"
                                )
                except json.JSONDecodeError as e:
                    Logger().error(f"Error loading average prices JSON data: {e}")
        self._server_name = PlayerManager().server.name
        self._prices_data_asked = False

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def dataAvailable(self) -> bool:
        return AveragePricesFrame._pricesData is not None

    @property
    def pricesData(self) -> PricesData:
        return self._pricesData

    def pushed(self) -> bool:
        self._server_name = PlayerManager().server.name
        return True

    def pulled(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameContextCreateMessage):
            if msg.context == GameContextEnum.ROLE_PLAY and self.updateAllowed():
                self.askPricesData()
            return False

        if isinstance(msg, ObjectAveragePricesMessage):
            self.updatePricesData(msg.ids, msg.avgPrices)
            return True

        if isinstance(msg, ObjectAveragePricesErrorMessage):
            return True

        return False

    def updatePricesData(self, pItemsIds: list[int], pItemsAvgPrices: list[float]) -> None:
        with pricesDataLock:
            # Initialize PricesData with current datetime and empty items
            self._pricesData[self._server_name] = PricesData(lastUpdate=datetime.now(), items={})

            # Update the items dictionary with the provided IDs and average prices
            for itemId, averagePrice in zip(pItemsIds, pItemsAvgPrices):
                self._pricesData[self._server_name].items[str(itemId)] = averagePrice

            # Ensure the directory for the averagePricesPath exists
            if not os.path.exists(os.path.dirname(settings.AVERAGE_PRICES_PATH)):
                os.makedirs(os.path.dirname(settings.AVERAGE_PRICES_PATH))

            # Serialize the PricesData to JSON and write to the file
            with open(settings.AVERAGE_PRICES_PATH, "w") as file:
                prices_data_dict = {
                    server_name: prices_data.to_dict() for server_name, prices_data in self._pricesData.items()
                }
                json.dump(prices_data_dict, file, indent=4)

        Logger().debug("Average prices data updated and saved.")

    def updateAllowed(self) -> bool:
        if (
            self._pricesData
            and self._server_name in self._pricesData
            and datetime.now().date() == self._pricesData[self._server_name].lastUpdate.date()
        ):
            Logger().debug("Average prices data already up to date")
            return False
        return True

    def getItemAveragePrice(self, guid: int):
        server_items = self._pricesData[self._server_name].items
        avg_price = server_items.get(str(guid))
        if not avg_price:
            Logger().error(f"Item '{guid}' not found in server items")
            # Logger().debug(f"Available items gids : {list(server_items.keys())}")
            return 0
        return avg_price

    def askPricesData(self) -> None:
        if self._prices_data_asked:
            return
        Logger().debug("Asking for average prices data")
        self._prices_data_asked = True
        oapgm = ObjectAveragePricesGetMessage()
        oapgm.init()
        ConnectionsHandler().send(oapgm)
