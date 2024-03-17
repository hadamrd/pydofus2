from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class SpellState(IDataCenter):
    MODULE: str = "SpellStates"

    id: int

    nameId: int

    preventsSpellCast: bool

    preventsFight: bool

    isSilent: bool

    cantDealDamage: bool

    invulnerable: bool

    incurable: bool

    cantBeMoved: bool

    cantBePushed: bool

    cantSwitchPosition: bool

    effectsIds: list[int]

    icon: str = ""

    iconVisibilityMask: int

    invulnerableMelee: bool

    invulnerableRange: bool

    cantTackle: bool

    cantBeTackled: bool

    displayTurnRemaining: bool

    @staticmethod
    def getSpellStateById(id: int) -> "SpellState":
        return GameData().getObject(SpellState.MODULE, id)

    @staticmethod
    def getSpellStates() -> list["SpellState"]:
        return GameData().getObjects(SpellState.MODULE)

    idAccessors: IdAccessors = IdAccessors(getSpellStateById, getSpellStates)
