from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import \
    MapDisplayManager
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.astar.AStar import \
    AStar
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.WorldGraph import \
    WorldGraph

dstmapId = 152043521.0
dstMapRpz = 1

srcMapId = 153092354.0
srcMapRpz = 1

MapDisplayManager().loadMap(srcMapId)

dstV = WorldGraph().getVertex(dstmapId, dstMapRpz)
srcV = WorldGraph().getVertex(srcMapId, dstMapRpz)

path = AStar().search(WorldGraph(), srcV, dstV)
if path is None:
    print("No path found")
else:
    for e in path:
        print(f"|- src {e.src} -> dst ({e.dst})")
        for tr in e.transitions:
            print(f"\t|- direction : {tr.direction}, skill : {tr.skillId}, cell : {tr.cell}, type : {tr.type}")