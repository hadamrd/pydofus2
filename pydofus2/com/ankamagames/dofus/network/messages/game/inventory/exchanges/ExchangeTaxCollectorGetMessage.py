from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemGenericQuantity import (
        ObjectItemGenericQuantity,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class ExchangeTaxCollectorGetMessage(NetworkMessage):
    collectorName: str
    worldX: int
    worldY: int
    mapId: int
    subAreaId: int
    userName: str
    callerId: int
    callerName: str
    pods: int
    objectsInfos: list["ObjectItemGenericQuantity"]
    look: "EntityLook"

    def init(
        self,
        collectorName_: str,
        worldX_: int,
        worldY_: int,
        mapId_: int,
        subAreaId_: int,
        userName_: str,
        callerId_: int,
        callerName_: str,
        pods_: int,
        objectsInfos_: list["ObjectItemGenericQuantity"],
        look_: "EntityLook",
    ):
        self.collectorName = collectorName_
        self.worldX = worldX_
        self.worldY = worldY_
        self.mapId = mapId_
        self.subAreaId = subAreaId_
        self.userName = userName_
        self.callerId = callerId_
        self.callerName = callerName_
        self.pods = pods_
        self.objectsInfos = objectsInfos_
        self.look = look_

        super().__init__()
