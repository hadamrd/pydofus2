from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Transition import Transition
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex


class Edge:
    _src: Vertex

    _dst: Vertex

    _transitions: list[Transition]

    def __init__(self, src: Vertex, dst: Vertex):
        super().__init__()
        self._src = src
        self._dst = dst
        self._transitions = list[Transition]()

    @property
    def src(self) -> Vertex:
        return self._src

    @property
    def dst(self) -> Vertex:
        return self._dst

    @property
    def transitions(self) -> list[Transition]:
        return self._transitions

    def addTransition(
        self,
        type: int,
        direction: int = -1,
        skill: int = -1,
        criterion: str = "",
        transitionMapId: float = -1,
        cell: int = -1,
        ieElemId: int = -1,
        npcTravelInfos=None,
        itemGID: int = -1,
    ) -> None:
        self.transitions.append(
            Transition(type, direction, skill, criterion, transitionMapId, cell, ieElemId, npcTravelInfos, itemGID)
        )

    def __str__(self):
        return "Edge(src={}, dst={}, transitions={})".format(self.src, self.dst, self.transitions)

    def __repr__(self) -> str:
        return self.__str__()

    def clone(self) -> "Edge":
        edge = Edge(self.src, self.dst)
        edge._transitions = [t.clone() for t in self.transitions]
        return edge

    def __eq__(self, other: object) -> bool:
        """Compare two edges for equality based on src and dst vertices"""
        if not isinstance(other, Edge):
            return False
        return self.src.UID == other.src.UID and self.dst.UID == other.dst.UID

    def __hash__(self) -> int:
        """Hash function for Edge objects based on src and dst vertices"""
        return hash((self.src.UID, self.dst.UID))
