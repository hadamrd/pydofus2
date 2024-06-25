from typing import List

from pydofus2.damageCalculation.fighterManagement.HaxeFighter import HaxeFighter
from pydofus2.damageCalculation.spellManagement.Mark import Mark


class IMapInfo:
    def isCellWalkable(self, cell_id: int) -> bool:
        pass

    def getOutputPortalCell(self, cell_id: int) -> int:
        pass

    def getMarks(self, markType: int = None, teamId: int = None) -> List[Mark]:
        pass

    def getMarkInteractingWithCell(self, cell_id: int, markType: int = None) -> List[Mark]:
        pass

    def getLastKilledAlly(self, team_id: int) -> HaxeFighter:
        pass

    def getFightersInitialPositions(self) -> List:
        pass

    def getFighterById(self, fighter_id: float) -> HaxeFighter:
        pass

    def getEveryFighterId(self) -> List[float]:
        pass

    def getCarriedFighterIdBy(self, fighter: HaxeFighter) -> float:
        pass

    def dispellIllusionOnCell(self, cell_id: int) -> None:
        pass
