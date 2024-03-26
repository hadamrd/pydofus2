from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
    GameFightFighterInformations
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable


class FightExchangePositionsStep(AbstractSequencable, IFightStep):

    _fighterOne: float

    _fighterOneNewCell: int

    _fighterTwo: float

    _fighterTwoNewCell: int

    _fighterOneVisibility: int

    def __init__(
        self,
        fighterOne: float,
        fighterOneNewCell: int,
        fighterTwo: float,
        fighterTwoNewCell: int,
    ):
        super().__init__()
        self._fighterOne = fighterOne
        self._fighterOneNewCell = fighterOneNewCell
        self._fighterTwo = fighterTwo
        self._fighterTwoNewCell = fighterTwoNewCell
        infos: "GameFightFighterInformations" = Kernel().fightEntitiesFrame.getEntityInfos(self._fighterOne)
        self._fighterOneVisibility = infos.stats.invisibilityState
        infos.disposition.cellId = self._fighterOneNewCell
        infos = Kernel().fightEntitiesFrame.getEntityInfos(self._fighterTwo)
        infos.disposition.cellId = self._fighterTwoNewCell

    @property
    def stepType(self) -> str:
        return "exchangePositions"

    def start(self) -> None:
        fighterInfosOne: GameFightFighterInformations = Kernel().fightEntitiesFrame.getEntityInfos(self._fighterOne)
        fighterInfosTwo: GameFightFighterInformations = Kernel().fightEntitiesFrame.getEntityInfos(self._fighterTwo)
        fighterInfosOne.disposition.cellId = self._fighterOneNewCell
        fighterInfosTwo.disposition.cellId = self._fighterTwoNewCell
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterOne, self._fighterTwo]
