import heapq
import os
import threading
import time
from typing import Callable, List, Optional, Union

from tinydb import TinyDB

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Edge import Edge
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.MapMemoryManager import MapMemoryManager
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Node import Node
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.TransitionTypeEnum import TransitionTypeEnum
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.WorldGraph import WorldGraph
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.pathfinding.Pathfinding import PathFinding
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

__dir__ = os.path.dirname(os.path.abspath(__file__))
FORBIDDEN_EDGES_FILE = os.path.join(__dir__, "forbidden_edges.json")
FORBIDDEN_EDGES_LOCK = threading.Lock()


class AStar(metaclass=Singleton):
    DEBUG = False
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
        self.worldGraph = WorldGraph()
        self.destinations: set[Vertex] = None
        self.running = None
        self.db = TinyDB(FORBIDDEN_EDGES_FILE)
        self.edges_table = self.db.table("forbidden_edges")
        self._initialize_forbidden_edges()

    def _initialize_forbidden_edges(self):
        """Initialize forbidden edges from database once WorldGraph is available"""
        with FORBIDDEN_EDGES_LOCK:
            edges_data = self.edges_table.all()
            forbidden_edges = []

            for edge_data in edges_data:
                src = self.worldGraph.getVertex(edge_data["src_mapId"], edge_data["src_zoneId"])
                dst = self.worldGraph.getVertex(edge_data["dst_mapId"], edge_data["dst_zoneId"])
                edge = self.worldGraph.getEdge(src, dst)
                if edge:
                    forbidden_edges.append(edge)

            self._forbiddenEdges = forbidden_edges

    def addForbiddenEdge(self, edge: Edge, reason: str = None) -> None:
        with FORBIDDEN_EDGES_LOCK:
            Logger().warning(f"Adding edge {edge} to forbidden list for reason : {reason}")
            edge_data = {
                "src_mapId": edge.src.mapId,
                "src_zoneId": edge.src.zoneId,
                "dst_mapId": edge.dst.mapId,
                "dst_zoneId": edge.dst.zoneId,
            }
            edge_data["reason"] = reason
            edge_data["timestamp"] = time.time()
            self._forbiddenEdges.append(edge)
            self.edges_table.insert(edge_data)

    def search(
        self, worldGraph: WorldGraph, src: Vertex, dst: Union[Vertex, List[Vertex]], maxPathLength=None
    ) -> list["Edge"]:
        if self.running:
            raise Exception("Pathfinding already in progress")
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

    def search_async(
        self,
        worldGraph: WorldGraph,
        src: Vertex,
        dst: Union[Vertex, List[Vertex]],
        callback: Callable[[int, Optional[str], Optional[List[Edge]]], None],
        maxPathLength=None,
    ) -> None:
        """
        Asynchronous version of search that runs in a separate thread.
        Callback receives (code, error, result):
            code: 0 for success, 1 for error
            error: error exception if code is 1, None otherwise
            result: list of edges if code is 0, None otherwise
        """
        if self.running:
            callback(1, "Pathfinding already in progress", None)
            return

        def worker():
            try:
                result = self.search(worldGraph, src, dst, maxPathLength)
                Kernel().defer(lambda: callback(0, None, result))
            except Exception as exc:
                Kernel().defer(lambda e=exc: callback(1, e, None))

        thread = threading.Thread(target=worker, name=threading.current_thread().name, daemon=True)
        thread.start()
        return thread

    def stopSearch(self) -> None:
        if self.running != None:
            self.callbackWithResult(None)

    def compute(self, e=None) -> None:
        while self.openList:
            if Kernel().worker._terminating.is_set():
                return
            if self.iterations > self.MAX_ITERATION:
                raise Exception("Too many iterations")
            self.iterations += 1
            _, _, current = heapq.heappop(self.openList)
            if self.DEBUG:
                Logger().debug(f"Processing vertex {current.vertex}")
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
            if self.DEBUG:
                Logger().debug(f"Processing Outgoing edges from {current.vertex}")
            for edge in edges:
                if Kernel().worker._terminating.is_set():
                    return

                if edge not in self._forbiddenEdges and self.hasValidTransition(edge):
                    existing = self.openDic.get(edge.dst)
                    if existing is None or current.moveCost + 1 < existing.moveCost:
                        node = Node(self, edge.dst, current)
                        self.openDic[edge.dst] = node
                        heapq.heappush(self.openList, (node.totalCost, id(node), node))
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
            if TransitionTypeEnum(transition.type) == TransitionTypeEnum.HAVEN_BAG_ZAAP:
                allowed = MapMemoryManager().is_havenbag_allowed(edge.src.mapId)
                if allowed is not None and not allowed:
                    continue
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

    def orderNodes(self, a: Node, b: Node) -> int:
        return 0 if a.heuristic == b.heuristic else (1 if a.heuristic > b.heuristic else -1)

    def buildResultPath(self, worldGraph: WorldGraph, node: Node) -> list[Edge]:
        result = list[Edge]()
        while node.parent is not None:
            result.append(worldGraph.getEdge(node.parent.vertex, node.vertex))
            node = node.parent
        result.reverse()
        return result
