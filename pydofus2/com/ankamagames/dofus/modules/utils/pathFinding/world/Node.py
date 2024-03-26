from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import \
    MapPosition
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import \
    Vertex

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.astar.AStar import \
        AStar


class Node:
    HEURISTIC_SCALE: int = 1
    INDOOR_WEIGHT: int = 0
    MAX_ITERATION: int = 10000

    def __init__(
        self,
        astar: "AStar",
        vertex: Vertex,
        parent: "Node" = None,
    ):
        self.parent = parent
        self.map = MapPosition.getMapPositionById(vertex.mapId)
        self.moveCost = 0
        self.heuristic = 0
        if parent is not None:
            self.moveCost = parent.moveCost + 1
            manhattanDistance = min(
                abs(self.map.posX - MapPosition.getMapPositionById(d.mapId).posX)
                + abs(self.map.posY - MapPosition.getMapPositionById(d.mapId).posY)
                for d in astar.destinations
            )
            self.heuristic = self.HEURISTIC_SCALE * manhattanDistance + (
                astar.INDOOR_WEIGHT if parent.map.outdoor and not self.map.outdoor else 0
            )
        self.totalCost = self.moveCost + self.heuristic
        self.vertex = vertex
        self.closed = False
        self.mapId = vertex.mapId
