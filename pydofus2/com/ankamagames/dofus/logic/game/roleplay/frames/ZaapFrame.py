from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.taxi.TeleportDestinationWrapper import (
    TeleportDestinationWrapper,
)
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.enums.DialogTypeEnum import DialogTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.TeleporterTypeEnum import TeleporterTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogMessage import LeaveDialogMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.zaap.TeleportDestinationsMessage import (
    TeleportDestinationsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.zaap.TeleportRequestMessage import (
    TeleportRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.zaap.ZaapDestinationsMessage import (
    ZaapDestinationsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.zaap.ZaapRespawnSaveRequestMessage import (
    ZaapRespawnSaveRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.zaap.ZaapRespawnUpdatedMessage import (
    ZaapRespawnUpdatedMessage,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.DataStoreEnum import DataStoreEnum
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class ZaapFrame(Frame):
    DATASTORE_SAVED_ZAAP = DataStoreType(
        "spawnMapId", True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_CHARACTER
    )

    def __init__(self):
        super().__init__()
        self._zaapsList = []
        self.spawnMapId = StoreDataManager().getData(self.DATASTORE_SAVED_ZAAP, "spawnMapId")
        if self.spawnMapId is None:
            self.spawnMapId = 0
        else:
            Logger().info("Loaded Spawn map id: " + str(self.spawnMapId))

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self):
        self._zaapsList = list[TeleportDestinationWrapper]()

        return True

    def pulled(self) -> bool:
        return True

    def sendTeleportRequest(self, cost, sourceType, destinationType, mapId):
        if cost <= PlayedCharacterManager().characteristics.kamas:
            trmsg = TeleportRequestMessage()
            trmsg.init(sourceType, destinationType, mapId)
            ConnectionsHandler().send(trmsg)
        else:
            Logger().warning(I18n.getUiText("ui.popup.not_enough_rich"))
            return False
        return True

    def zaapRespawnSaveRequest(self):
        zrsrmsg = ZaapRespawnSaveRequestMessage()
        ConnectionsHandler().send(zrsrmsg)
        return True

    def isZaapKnown(self, mapId):
        for zaap in self._zaapsList:
            if zaap.mapId == mapId:
                return True
        return False

    def process(self, msg):

        if isinstance(msg, ZaapDestinationsMessage):
            self._zaapsList = []
            for dest in msg.destinations:
                self._zaapsList.append(
                    TeleportDestinationWrapper(
                        msg.type,
                        dest.mapId,
                        dest.subAreaId,
                        dest.type,
                        dest.level,
                        dest.cost,
                        msg.spawnMapId == dest.mapId,
                    )
                )
            self.spawnMapId = msg.spawnMapId
            StoreDataManager().setData(self.DATASTORE_SAVED_ZAAP, "spawnMapId", msg.spawnMapId)
            KernelEventsManager().send(
                KernelEvent.TeleportDestinationList,
                self._zaapsList,
                (
                    TeleporterTypeEnum.TELEPORTER_HAVENBAG
                    if msg.type == TeleporterTypeEnum.TELEPORTER_HAVENBAG
                    else TeleporterTypeEnum.TELEPORTER_ZAAP
                ),
            )
            return True

        elif isinstance(msg, TeleportDestinationsMessage):
            destinations = []
            if msg.type == TeleporterTypeEnum.TELEPORTER_SUBWAY:
                for dest in msg.destinations:
                    hints = TeleportDestinationWrapper.getHintsFromMapId(dest.mapId)
                    for hint in hints:
                        destinations.append(
                            TeleportDestinationWrapper(
                                msg.type,
                                dest.mapId,
                                dest.subAreaId,
                                TeleporterTypeEnum.TELEPORTER_SUBWAY,
                                dest.level,
                                dest.cost,
                                False,
                                hint,
                            )
                        )
            else:
                for dest in msg.destinations:
                    destinations.append(
                        TeleportDestinationWrapper(
                            msg.type, dest.mapId, dest.subAreaId, dest.type, dest.level, dest.cost
                        )
                    )
            KernelEventsManager().send(KernelEvent.TeleportDestinationList, destinations, msg.type)
            return True

        elif isinstance(msg, ZaapRespawnUpdatedMessage):
            for zaap in self._zaapsList:
                zaap.spawn = zaap.mapId == msg.mapId
            self.spawnMapId = msg.mapId
            StoreDataManager().setData(self.DATASTORE_SAVED_ZAAP, "spawnMapId", msg.mapId)
            KernelEventsManager().send(
                KernelEvent.TeleportDestinationList, self._zaapsList, TeleporterTypeEnum.TELEPORTER_ZAAP
            )
            return True

        elif isinstance(msg, LeaveDialogMessage):
            if msg.dialogType == DialogTypeEnum.DIALOG_TELEPORTER:
                Kernel().worker.removeFrame(self)
            return True
