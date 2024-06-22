from pydofus2.com.ankamagames.dofus.network.types.game.context.MapCoordinatesAndId import MapCoordinatesAndId


class MapCoordinatesExtended(MapCoordinatesAndId):
    subAreaId: int

    def init(self, subAreaId_: int, mapId_: int, worldX_: int, worldY_: int):
        self.subAreaId = subAreaId_

        super().init(mapId_, worldX_, worldY_)
