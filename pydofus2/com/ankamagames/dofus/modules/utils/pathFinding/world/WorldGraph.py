import json
import os
from time import perf_counter
from typing import List, Optional

from pydofus2.com.ankamagames.dofus.datacenter.world.Hint import Hint
from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Edge import Edge
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.MapMemoryManager import MapMemoryManager
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.TransitionTypeEnum import TransitionTypeEnum
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum
from pydofus2.mapTools import MapTools

WORLDGRAPH_PATH = XmlConfig().getEntry("config.data.pathFinding")
__dir__ = os.path.dirname(os.path.abspath(__file__))
NPC_TRAVEL_DATA_FILE = os.path.join(__dir__, "npc_travel_data.json")
EDGE_PATCHES_FILE = os.path.join(__dir__, "edge_patches.json")


class WorldGraph(metaclass=ThreadSharedSingleton):
    def __init__(self):
        self._vertices = dict[int, dict[int, Vertex]]()
        self._edges = dict[float, Edge]()
        self._outgoingEdges = dict[float, list[Edge]]()
        self._vertexUid: float = 0
        self._map_memory = MapMemoryManager()
        self.init()

    def addEdgePatches(self):
        with open(EDGE_PATCHES_FILE, "r") as f:
            edges_patches = json.load(f)
            for patch in edges_patches:
                src_vertex = self.getVertex(patch["src_vertex"]["mapId"], patch["src_vertex"]["zoneId"])
                dst_vertex = self.getVertex(patch["dst_vertex"]["mapId"], patch["dst_vertex"]["zoneId"])
                patch_edge = self.addEdge(src_vertex, dst_vertex)
                for tr in patch["transitions"]:
                    patch_edge.addTransition(**tr)

    def addNpcTravelEdges(self):
        with open(NPC_TRAVEL_DATA_FILE, "r") as f:
            npc_travel_infos = json.load(f)
            for info in npc_travel_infos.values():
                src_vertex = self.getVertex(info["npcMapId"], 1)
                dst_vertex = self.getVertex(info["landingMapId"], 1)
                npc_travel_edge = self.addEdge(src_vertex, dst_vertex)
                npc_travel_edge.addTransition(TransitionTypeEnum.NPC_TRAVEL, npcTravelInfos=info)

    def nextMapInDirection(self, mapId, direction):
        for vertex in self.getVertices(mapId).values():
            for edge in self.getOutgoingEdgesFromVertex(vertex):
                for transition in edge.transitions:
                    if transition.direction != -1 and transition.direction == direction:
                        return edge.dst.mapId

    def init(self):
        s = perf_counter()
        with open(WORLDGRAPH_PATH, "rb") as binaries:
            data = ByteArray(binaries.read())
            edgeCount: int = data.readInt()
            for _ in range(edgeCount):
                src = self.addVertex(data.readDouble(), data.readInt())
                dest = self.addVertex(data.readDouble(), data.readInt())
                edge = self.addEdge(src, dest)
                transitionCount = data.readInt()
                for _ in range(transitionCount):
                    tr_dir, tr_type, tr_skill, tr_criterion, tr_tran_mapId, tr_cell, tr_ieId = (
                        data.readByte(),
                        data.readByte(),
                        data.readInt(),
                        data.readUTFBytes(data.readInt()),
                        data.readDouble(),
                        data.readInt(),
                        data.readDouble(),
                    )
                    edge.addTransition(tr_type, tr_dir, tr_skill, tr_criterion, tr_tran_mapId, tr_cell, tr_ieId)
            del data
        self.addNpcTravelEdges()
        self.addEdgePatches()
        Logger().debug("WorldGraph loaded in %s seconds", perf_counter() - s)

    def addEdge(self, src: Vertex, dest: Vertex) -> Edge:
        edge: Edge = self._edges.get(src.UID, {}).get(dest.UID)
        if edge:
            return edge
        if not self.doesVertexExist(src) or not self.doesVertexExist(dest):
            return None
        edge = Edge(src, dest)
        if self._edges.get(src.UID) is None:
            self._edges[src.UID] = dict()
        self._edges[src.UID][dest.UID] = edge
        outgoing = self._outgoingEdges.get(src.UID)
        if outgoing is None:
            outgoing = list[Edge]()
            self._outgoingEdges[src.UID] = outgoing
        outgoing.append(edge)
        return edge

    def addVertex(self, mapId: float, zone: int) -> Vertex:
        vertex: Vertex = self._vertices.get(mapId, {}).get(zone)
        if vertex is None:
            vertex = Vertex(mapId, zone, self._vertexUid)
            self._vertexUid += 1
            if mapId not in self._vertices:
                self._vertices[mapId] = dict()
            self._vertices[mapId][zone] = vertex
        return vertex

    def doesVertexExist(self, v: Vertex) -> bool:
        return v.mapId in self._vertices and v.zoneId in self._vertices[v.mapId]

    def getEdges(self) -> dict:
        return self._edges

    def getVertex(self, mapId: float, mapRpZone: int) -> Vertex:
        mapId = float(mapId)
        mapRpZone = int(mapRpZone)
        return self._vertices.get(mapId, {}).get(mapRpZone)

    def getVertices(self, mapId) -> dict[int, Vertex]:
        return self._vertices.get(mapId)

    def getOutgoingEdgesFromVertex(self, src: Vertex) -> List[Edge]:
        if src is None:
            Logger().error("Got a None edge!")
            return None

        result = self._outgoingEdges.get(src.UID, [])
        rappel_potion_edge = self.getRappelPotionEdge(src)
        if rappel_potion_edge:
            result.append(rappel_potion_edge)
        zaap_edges = self.getOutgoingZaapEdges(src)
        if zaap_edges:
            result.extend(zaap_edges)
        return result

    def getOutgoingZaapEdges(self, src: Vertex):
        src_allow_havenbag = self._map_memory.is_havenbag_allowed(src.mapId)
        if src_allow_havenbag is None:
            src_allow_havenbag = MapPosition.getMapPositionById(src.mapId).allowTeleportFrom

        if not PlayerManager().isBasicAccount() and src_allow_havenbag:
            return self.getEdgesToKnownZaapsFromVertex(src, TransitionTypeEnum.HAVEN_BAG_ZAAP)

        if not src.mapId in Hint.getZaapMapIds() or self._map_memory.is_zaap_vertex(src) == "no":
            return []

        return self.getEdgesToKnownZaapsFromVertex(src, TransitionTypeEnum.ZAAP)

    def getRappelPotionEdge(self, src: Vertex) -> Edge:
        from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
        from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import InventoryManager

        if not Kernel().zaapFrame:
            return None

        for iw in InventoryManager().inventory.getView("storageConsumables").content:
            if iw.objectGID == DataEnum.RAPPEL_POTION_GUID:
                if Kernel().zaapFrame.spawnMapId:
                    dst_tp_vertex = self.getVertex(Kernel().zaapFrame.spawnMapId, 1)
                    if dst_tp_vertex == src:
                        return None
                    edge = self.getEdge(src, dst_tp_vertex)
                    if not edge:
                        edge = self.addEdge(src, dst_tp_vertex)
                    if not self.hasItemTeleportTransition(edge, DataEnum.RAPPEL_POTION_GUID):
                        edge.addTransition(TransitionTypeEnum.ITEM_TELEPORT, itemGID=DataEnum.RAPPEL_POTION_GUID)
                    return edge

        return None

    def hasItemTeleportTransition(self, edge: Edge, item_gid):
        for transition in edge.transitions:
            if transition.itemGID == item_gid:
                return True
        return False

    def hasZaapTransition(self, edge: Edge, tr_type: TransitionTypeEnum):
        for transition in edge.transitions:
            if TransitionTypeEnum(transition.type) == tr_type:
                return True
        return False

    def getEdgesToKnownZaapsFromVertex(self, src: Vertex, transition_type=TransitionTypeEnum.ZAAP) -> List[Edge]:
        """Get edges to all known zaap destinations from a source vertex."""
        zaap_edges = []

        def can_afford_teleport(src_map_id: int, dst_map_id: int) -> bool:
            tp_cost = 10 * MapTools.distL2Maps(src_map_id, dst_map_id)
            return int(tp_cost) <= PlayedCharacterManager().characteristics.kamas

        def can_travel_between_areas(src_map_id: int, dst_map_id: int) -> bool:
            src_sub_area = SubArea.getSubAreaByMapId(src_map_id)
            dst_sub_area = SubArea.getSubAreaByMapId(dst_map_id)
            return (src_sub_area.areaId == DataEnum.ANKARNAM_AREA_ID) == (
                dst_sub_area.areaId == DataEnum.ANKARNAM_AREA_ID
            )

        def get_or_create_zaap_edge(src: Vertex, dst: Vertex) -> Optional[Edge]:
            if src == dst:
                return None

            if not can_travel_between_areas(src.mapId, dst.mapId):
                return None

            edge = self.getEdge(src, dst) or self.addEdge(src, dst)
            if not self.hasZaapTransition(edge, transition_type):
                edge.addTransition(transition_type)
            return edge

        for zaap_map_id in PlayedCharacterManager()._knownZaapMapIds:
            if not can_afford_teleport(src.mapId, zaap_map_id):
                continue

            zaap_vertex_info = self._map_memory.get_zaap_vertex(zaap_map_id)

            if zaap_vertex_info is None:
                # Try all possible vertices on the map
                for dest_vertex in self.getVertices(zaap_map_id).values():
                    if edge := get_or_create_zaap_edge(src, dest_vertex):
                        zaap_edges.append(edge)
            else:
                # Use known zaap vertex
                map_id, zone_id = zaap_vertex_info
                dest_vertex = self.getVertex(map_id, zone_id)
                if edge := get_or_create_zaap_edge(src, dest_vertex):
                    zaap_edges.append(edge)

        return zaap_edges

    def getEdge(self, src: Vertex, dest: Vertex) -> Edge:
        return self._edges.get(src.UID, {}).get(dest.UID)

    def reset(self):
        self._vertices.clear()
        self._edges.clear()
        self._outgoingEdges.clear()
        self._vertexUid: float = 0

    def canChangeMap(self, mapId, direction):
        if not self.getVertices(mapId):
            return False
        for vertex in self.getVertices(mapId).values():
            for edge in WorldGraph().getOutgoingEdgesFromVertex(vertex):
                for transition in edge.transitions:
                    if transition.direction and DirectionsEnum(transition.direction) == direction:
                        return True
        return False

    def currMapActionCells(self):
        from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
            PlayedCharacterManager,
        )

        res = []
        currVertex = PlayedCharacterManager().currVertex
        if not currVertex:
            return res
        for edge in WorldGraph().getOutgoingEdgesFromVertex(currVertex):
            for tr in edge.transitions:
                if TransitionTypeEnum(tr.type) == TransitionTypeEnum.MAP_ACTION:
                    res.append(tr.cell)
        return res
