from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Edge import Edge
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.TransitionTypeEnum import TransitionTypeEnum
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex
from pydofus2.mapTools import MapTools

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.astar.AStar import AStar


class Node:
    HEURISTIC_SCALE: int = 1
    INDOOR_WEIGHT: int = 3
    KAMAS_WEIGHT = 30

    def __init__(self, astar: "AStar", vertex: Vertex, parent: "Node" = None, edge: Edge = None):
        self.parent = parent
        self.map = MapPosition.getMapPositionById(vertex.mapId)
        self.moveCost = 0
        self.heuristic = 0
        self.total_kamas_spent = 0
        self.edge = edge

        if parent is not None:
            self.moveCost = parent.moveCost + 1
            self.total_kamas_spent = parent.total_kamas_spent + self.kamasCost
            manhattanDistance = min(
                abs(self.map.posX - MapPosition.getMapPositionById(d.mapId).posX)
                + abs(self.map.posY - MapPosition.getMapPositionById(d.mapId).posY)
                for d in astar.destinations
            )
            self.heuristic = self.HEURISTIC_SCALE * manhattanDistance + (
                self.INDOOR_WEIGHT if parent.map.outdoor and not self.map.outdoor else 0
            )

        self.totalCost = self.moveCost + self.heuristic + (self.KAMAS_WEIGHT * self.total_kamas_spent)
        self.vertex = vertex
        self.closed = False
        self.mapId = vertex.mapId

    @property
    def kamasCost(self) -> int:
        if not self.edge:
            return 0

        kamas_cost = float("inf")  # Start with infinity as initial min cost

        for tr in self.edge.transitions:
            if tr.type in [TransitionTypeEnum.ZAAP.value, TransitionTypeEnum.HAVEN_BAG_ZAAP.value]:
                tr_cost = 10 * MapTools.distL2Maps(self.edge.src.mapId, self.edge.dst.mapId)
            elif tr.type == TransitionTypeEnum.ITEM_TELEPORT:
                tr_cost = Kernel().averagePricesFrame.getItemAveragePrice(tr.itemGID)
            elif tr.type == TransitionTypeEnum.NPC_TRAVEL:
                tr_cost = tr._npc_travel_infos.get("kamas_cost", 0)
            else:
                tr_cost = 0

            # If we find a free transition, we can return immediately
            if tr_cost == 0:
                return 0

            # Update minimum cost if this transition is cheaper
            kamas_cost = min(kamas_cost, tr_cost)

        # Return 0 if no valid cost was found (kamas_cost is still inf)
        return 0 if kamas_cost == float("inf") else kamas_cost
