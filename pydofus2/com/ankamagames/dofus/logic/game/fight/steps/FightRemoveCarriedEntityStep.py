from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.FightRemoveSubEntityStep import FightRemoveSubEntityStep


class FightRemoveCarriedEntityStep(FightRemoveSubEntityStep):

    _carriedId: float

    def __init__(self, fighterId: float, carriedId: float, category: int, slot: int):
        self._carriedId = carriedId
        super().__init__(fighterId, category, slot)

    @property
    def stepType(self) -> str:
        return "removeCarriedEntity"

    def start(self) -> None:
        super().start()
