import os
from typing import Optional, Tuple

from tinydb import Query, TinyDB

from pydofus2.com.ankamagames.dofus.datacenter.houses.HavenbagTheme import HavenbagTheme
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton

__dir__ = os.path.dirname(os.path.abspath(__file__))
MAP_MEMORY_FILE = os.path.join(__dir__, "map_memory.json")

from threading import Lock


class MapMemoryManager(metaclass=ThreadSharedSingleton):
    """Manages persistent memory for map-related information using TinyDB."""

    def __init__(self):
        """Initialize the memory manager with the database path."""
        self._lock = Lock()
        self._db = TinyDB(MAP_MEMORY_FILE)
        self._zaap_table = self._db.table("zaap_vertices")
        self._havenbag_table = self._db.table("allow_havenbag")
        self._query = Query()

    def is_havenbag_allowed(self, map_id: float) -> Optional[bool]:
        """
        Check if haven bag teleportation is allowed from a map.
        Thread-safe implementation.
        """
        with self._lock:
            result = self._havenbag_table.get(self._query.map_id == map_id)
            return result.get("allowed") if result else None

    def register_havenbag_allowance(self, map_id: float, allowed: bool) -> None:
        """
        Register whether haven bag teleportation is allowed from a map.
        Thread-safe implementation.
        """
        with self._lock:
            self._havenbag_table.upsert({"map_id": map_id, "allowed": allowed}, self._query.map_id == map_id)
            Logger().debug(f"Registered haven bag allowance for map {map_id}: {allowed}")

    def register_zaap_vertex(self, vertex: Vertex, is_zaap: bool = True) -> None:
        """
        Register a vertex as a zaap location.
        Thread-safe implementation.
        """
        if not vertex or HavenbagTheme.isMapIdInHavenbag(vertex.mapId):
            return

        with self._lock:
            key = self._get_vertex_key(vertex)
            self._zaap_table.upsert(
                {"key": key, "is_zaap": is_zaap, "map_id": vertex.mapId, "zone_id": vertex.zoneId},
                self._query.key == key,
            )
            Logger().debug(f"Registered zaap vertex {key} with status {is_zaap}")

    def _get_vertex_key(self, vertex: Vertex) -> str:
        """Generate a unique key for a vertex."""
        return f"{vertex.mapId},{vertex.zoneId}"

    def is_zaap_vertex(self, vertex: Vertex) -> str:
        """
        Check if a vertex is a zaap location.
        Thread-safe implementation.
        """
        with self._lock:
            key = self._get_vertex_key(vertex)
            result = self._zaap_table.get(self._query.key == key)
            if result is None:
                return "unknown"
            return "yes" if result["is_zaap"] else "no"

    def get_zaap_vertex(self, map_id: float) -> Optional[Tuple[float, int]]:
        """
        Get the zaap vertex information for a given map ID.
        Thread-safe implementation.
        """
        with self._lock:
            results = self._zaap_table.search((self._query.map_id == map_id) & (self._query.is_zaap == True))
            if not results:
                return None
            return (results[0]["map_id"], results[0]["zone_id"])

    def clear_all(self) -> None:
        """
        Clear all stored data.
        Thread-safe implementation.
        """
        with self._lock:
            self._zaap_table.truncate()
            self._havenbag_table.truncate()
            Logger().debug("Cleared all map memory data")

    def __del__(self):
        """Ensure the database is closed properly."""
        with self._lock:
            self._db.close()
