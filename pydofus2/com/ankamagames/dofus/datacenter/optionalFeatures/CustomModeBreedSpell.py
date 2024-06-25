from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class CustomModeBreedSpell(IDataCenter):

    MODULE: str = "CustomModeBreedSpells"

    _allSpellsId: list = None

    id: int

    pairId: int

    breedId: int

    isInitialSpell: bool

    isHidden: bool

    def __init__(self):
        super().__init__()

    @classmethod
    def getCustomModeBreedSpellById(cls, id: int) -> "CustomModeBreedSpell":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getCustomModeBreedSpells(cls) -> list["CustomModeBreedSpell"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getCustomModeBreedSpellById, getCustomModeBreedSpells)

    @classmethod
    def getAllCustomModeBreedSpellIds(cls) -> list:
        if cls._allSpellsId is None:
            cls._allSpellsId = []
            customModeBreedSpells = cls.getCustomModeBreedSpells()
            for index in range(len(customModeBreedSpells)):
                cls._allSpellsId.append(customModeBreedSpells[index].id)
        return cls._allSpellsId

    @classmethod
    def getCustomModeBreedSpellIds(cls, breedId: int) -> list:
        toReturn: list = []
        customModeBreedSpells: list = cls.getCustomModeBreedSpells()
        currentCustomModeBreedSpell: CustomModeBreedSpell = None
        for index in range(len(customModeBreedSpells)):
            currentCustomModeBreedSpell = customModeBreedSpells[index]
            if currentCustomModeBreedSpell.breedId == breedId:
                toReturn.append(currentCustomModeBreedSpell.id)
        return toReturn

    @classmethod
    def getCustomModeBreedSpellList(cls, breedId: int) -> list["CustomModeBreedSpell"]:
        toReturn = []
        customModeBreedSpells = cls.getCustomModeBreedSpells()
        for index in range(len(customModeBreedSpells)):
            currentCustomModeBreedSpell = customModeBreedSpells[index]
            if currentCustomModeBreedSpell.breedId == breedId:
                toReturn.append(currentCustomModeBreedSpell)
        return toReturn
