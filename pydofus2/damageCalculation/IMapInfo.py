from abc import ABC, abstractmethod
from typing import List

from pydofus2.damageCalculation.fighterManagement.HaxeFighter import HaxeFighter
from pydofus2.damageCalculation.spellManagement.Mark import Mark


class IMapInfo(ABC):
    @abstractmethod
    def isCellWalkable(self, cell_id: int) -> bool:
        pass

    @abstractmethod
    def getOutputPortalCell(self, cell_id: int) -> int:
        pass

    @abstractmethod
    def getMarks(self, markType: int = None, teamId: int = None) -> List[Mark]:
        pass

    @abstractmethod
    def getMarkInteractingWithCell(self, cell_id: int, markType: int = None) -> List[Mark]:
        pass

    @abstractmethod
    def getLastKilledAlly(self, team_id: int) -> HaxeFighter:
        pass

    @abstractmethod
    def getFightersInitialPositions(self) -> List:
        pass

    @abstractmethod
    def getFighterById(self, fighter_id: float) -> HaxeFighter:
        pass

    @abstractmethod
    def getEveryFighterId(self) -> List[float]:
        pass

    @abstractmethod
    def getCarriedFighterIdBy(self, fighter: HaxeFighter) -> float:
        pass

    @abstractmethod
    def dispellIllusionOnCell(self, cell_id: int) -> None:
        pass
