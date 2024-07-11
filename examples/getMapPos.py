from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition

for mp in MapPosition.getMapPositions():
    # print(mp.id, mp.posX, mp.posY, mp.outdoor, mp.subArea.name, mp.worldMap, mp.capabilities)
    if mp.id == 68422145.0:
        print("area: ", mp.subArea.area.id, mp.subArea.area.name)
        print("subarea :", mp.subArea.id, mp.subArea.name)
        print(mp.subArea.npcs)
        print("MapId: ", mp.id)
