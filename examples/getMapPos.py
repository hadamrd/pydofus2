from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import \
    MapPosition

for mp in MapPosition.getMapPositions():
    print(mp.id, mp.posX, mp.posY, mp.outdoor, mp.subArea.name, mp.worldMap, mp.capabilities)
