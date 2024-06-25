import heapq
from typing import List, Union

from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.misc.utils.GameDataQuery import GameDataQuery
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Edge import Edge
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Node import Node
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.WorldGraph import WorldGraph
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.pathfinding.Pathfinding import PathFinding
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class AStar(metaclass=Singleton):
    DEBUG = False
    _forbiddenSubareaIds = list[int]()
    _forbiddenEdges = list[Edge]()
    HEURISTIC_SCALE: int = 1
    INDOOR_WEIGHT: int = 0
    MAX_ITERATION: int = 10000
    CRITERION_WHITE_LIST = ["Ad", "DM", "MI", "Mk", "Oc", "Pc", "QF", "Qo", "Qs", "Sv", "PG"]

    def __init__(self):
        super().__init__()
        self.openList = list[Node]()
        self.openDic = dict()
        self.iterations: int = 0
        self.worldGraph: WorldGraph = None
        self.dstinations: set[Vertex] = None
        self.running = None

    def addForbidenEdge(self, edge: Edge) -> None:
        self._forbiddenEdges.append(edge)

    def resetForbinedEdges(self) -> None:
        self._forbiddenEdges.clear()

    def search(
        self, worldGraph: WorldGraph, src: Vertex, dst: Union[Vertex, List[Vertex]], maxPathLength=None
    ) -> list["Edge"]:
        if self.running:
            raise Exception("Pathfinding already in progress")
        self.initForbiddenSubareaList()
        self.worldGraph = worldGraph
        if not isinstance(dst, list):
            dst = [dst]
        if src in dst:
            Logger().info("Source vertex is one of the destinations.")
            return []
        self.destinations = set(dst)
        self.running = True
        self.openList = list[tuple[int, int, Node, MapPoint]]()
        self.openDic = dict[Vertex, Node]()
        self.maxPathLength = maxPathLength
        self.iterations = 0
        node = Node(self, src)
        heapq.heappush(self.openList, (0, id(node), node))
        return self.compute()

    def initForbiddenSubareaList(self) -> None:
        self._forbiddenSubareaIds = GameDataQuery.queryEquals(SubArea, "mountAutoTripAllowed", False)

    def stopSearch(self) -> None:
        if self.running != None:
            self.callbackWithResult(None)

    def compute(self, e=None) -> None:
        while self.openList:
            if self.iterations > self.MAX_ITERATION:
                raise Exception("Too many iterations")
            self.iterations += 1
            _, _, current = heapq.heappop(self.openList)
            if current.closed:
                continue
            current.closed = True
            if self.maxPathLength and current.moveCost > self.maxPathLength:
                continue
            if current.vertex in self.destinations:
                result = self.buildResultPath(self.worldGraph, current)
                self.running = False
                return result
            edges = self.worldGraph.getOutgoingEdgesFromVertex(current.vertex)
            for edge in edges:
                if (
                    edge not in self._forbiddenEdges
                    and self.hasValidTransition(edge)
                    and self.hasValidDestinationSubarea(edge)
                ):
                    existing = self.openDic.get(edge.dst)
                    if existing is None or current.moveCost + 1 < existing.moveCost:
                        node = Node(self, edge.dst, current)
                        self.openDic[edge.dst] = node
                        heapq.heappush(self.openList, (node.totalCost, id(node), node))
                else:
                    if self.DEBUG:
                        reasons = []
                        if edge in self._forbiddenEdges:
                            reasons.append("Edge is in forbidden edges list")
                        if not self.hasValidTransition(edge):
                            reasons.append("Edge has a non valid transition")
                        if not self.hasValidDestinationSubarea(edge):
                            reasons.append("Edge has a non valid destination subarea")
                        Logger().debug(f"Edge dismissed for reason {', '.join(reasons)}")
        self.running = False
        return None

    def findDstCell(self, edge: Edge, mp: MapPoint) -> int:
        for reverse_edge in self.worldGraph.getOutgoingEdgesFromVertex(edge.dst):
            if reverse_edge.dst == edge.src:
                for tr in reverse_edge.transitions:
                    if tr.cell:
                        candidate = MapPoint.fromCellId(tr.cell)
                        movePath = PathFinding().findPath(mp, candidate)
                        if movePath.end.distanceTo(candidate) <= 2:
                            return candidate
        return None

    @classmethod
    def hasValidTransition(cls, edge: Edge) -> bool:
        from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import GroupItemCriterion

        valid = False
        for transition in edge.transitions:
            if transition.criterion:
                if (
                    "&" not in transition.criterion
                    and "|" not in transition.criterion
                    and transition.criterion[0:2] not in cls.CRITERION_WHITE_LIST
                ):
                    return False
                criterion = GroupItemCriterion(transition.criterion)
                return criterion.isRespected
            valid = True
        return valid

    def hasValidDestinationSubarea(self, edge: Edge) -> bool:
        fromMapId = edge.src.mapId
        fromMapPos = MapPosition.getMapPositionById(fromMapId)
        fromSubareaId = fromMapPos.subAreaId
        toMapId = edge.dst.mapId
        toMapPos = MapPosition.getMapPositionById(toMapId)
        if not toMapPos:
            Logger().error(f"MapPosition {toMapId} not found")
            return False
        if fromSubareaId == toMapPos.subAreaId:
            return True
        if toMapPos.subAreaId in self._forbiddenSubareaIds:
            return False
        return True

    def orderNodes(self, a: Node, b: Node) -> int:
        return 0 if a.heuristic == b.heuristic else (1 if a.heuristic > b.heuristic else -1)

    def buildResultPath(self, worldGraph: WorldGraph, node: Node) -> list[Edge]:
        result = list[Edge]()
        while node.parent is not None:
            result.append(worldGraph.getEdge(node.parent.vertex, node.vertex))
            node = node.parent
        result.reverse()
        return result
