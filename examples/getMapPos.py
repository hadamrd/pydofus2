from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition

for mp in MapPosition.getMapPositions():
    # print(mp.id, mp.posX, mp.posY, mp.outdoor, mp.subArea.name, mp.worldMap, mp.capabilities)
    if mp.posX == 12 and mp.posY == -63:
        print("area: ", mp.subArea.area.id, mp.subArea.area.name)
        print("subarea :", mp.subArea.id, mp.subArea.name)
        print("MapId: ", mp.id)
