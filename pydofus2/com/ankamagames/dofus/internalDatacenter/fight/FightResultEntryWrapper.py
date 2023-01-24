from pydofus2.com.ankamagames.dofus.datacenter.monsters.Companion import Companion
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.npcs.TaxCollectorFirstname import (
    TaxCollectorFirstname,
)
from pydofus2.com.ankamagames.dofus.datacenter.npcs.TaxCollectorName import TaxCollectorName
from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.FightLootWrapper import (
    FightLootWrapper,
)
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultExperienceData import (
    FightResultExperienceData,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultFighterListEntry import (
    FightResultFighterListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultListEntry import (
    FightResultListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultMutantListEntry import (
    FightResultMutantListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultPlayerListEntry import (
    FightResultPlayerListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultPvpData import (
    FightResultPvpData,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultTaxCollectorListEntry import (
    FightResultTaxCollectorListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacterInformations import (
    GameFightCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightEntityInformation import (
    GameFightEntityInformation,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightTaxCollectorInformations import (
    GameFightTaxCollectorInformations,
)
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class FightResultEntryWrapper(IDataCenter):

    _item: FightResultListEntry

    outcome: int

    id: float = None

    name: str

    alive: bool

    rewards: FightLootWrapper

    level: int

    type: int

    fightInitiator: bool

    breed: int = 0

    gender: int = 0

    wave: int

    isLastOfHisWave: bool = False

    rerollXpMultiplicator: int

    experience: float

    showExperience: bool = False

    experienceLevelFloor: float

    showExperienceLevelFloor: bool = False

    experienceNextLevelFloor: float

    showExperienceNextLevelFloor: bool = False

    experienceFightDelta: float

    showExperienceFightDelta: bool = False

    experienceForGuild: float

    showExperienceForGuild: bool = False

    experienceForRide: float

    showExperienceForRide: bool = False

    grade: int

    honor: int

    honorDelta: int = -1

    maxHonorForGrade: int

    minHonorForGrade: int

    isIncarnationExperience: bool

    def __init__(
        self,
        o: FightResultListEntry,
        infos: GameFightFighterInformations = None,
        isSpectator: bool = False,
    ):
        super().__init__()
        self._item = o
        self.outcome = o.outcome
        self.rewards = FightLootWrapper(o.rewards)
        if isinstance(o, FightResultPlayerListEntry):
            player = o
            if not infos:
                pass
            elif isinstance(infos, GameFightMonsterInformations):
                monsterInfos0 = infos
                monster0 = Monster.getMonsterById(monsterInfos0.creatureGenericId)
                self.name = monster0.name
                self.level = infos.creatureLevel
                self.id = monster0.id
                self.alive = monsterInfos0.spawnInfo.alive
                self.type = 1
            elif isinstance(infos, GameFightTaxCollectorInformations):
                tcInfos = infos
                self.name = (
                    TaxCollectorFirstname.getTaxCollectorFirstnameById(
                        tcInfos.firstNameId
                    ).firstname
                    + " "
                    + TaxCollectorName.getTaxCollectorNameById(tcInfos.lastNameId).name
                )
                self.level = tcInfos.level
                self.id = tcInfos.contextualId
                self.alive = tcInfos.spawnInfo.alive
                self.type = 2
            else:
                self.name = infos.name
                self.level = player.level
                self.id = player.id
                self.alive = player.alive
                if isinstance(infos, GameFightCharacterInformations):
                    self.breed = infos.breed
                    self.gender = int(infos.sex)
                self.type = 0
                if len(player.additional) == 0:
                    pass
                else:
                    for addInfo in player.additional:
                        if isinstance(addInfo, FightResultExperienceData):
                            self.rerollXpMultiplicator = addInfo.rerollExperienceMul
                            self.experience = addInfo.experience
                            self.showExperience = addInfo.showExperience
                            self.experienceLevelFloor = addInfo.experienceLevelFloor
                            self.showExperienceLevelFloor = (
                                addInfo.showExperienceLevelFloor
                            )
                            self.experienceNextLevelFloor = (
                                addInfo.experienceNextLevelFloor
                            )
                            self.showExperienceNextLevelFloor = (
                                addInfo.showExperienceNextLevelFloor
                            )
                            self.experienceFightDelta = addInfo.experienceFightDelta
                            self.showExperienceFightDelta = (
                                addInfo.showExperienceFightDelta
                            )
                            self.experienceForGuild = addInfo.experienceForGuild
                            self.showExperienceForGuild = addInfo.showExperienceForGuild
                            self.experienceForRide = addInfo.experienceForMount
                            self.showExperienceForRide = addInfo.showExperienceForMount
                            self.isIncarnationExperience = (
                                addInfo.isIncarnationExperience
                            )
                            self.honorDelta = -1
                        elif isinstance(addInfo, FightResultPvpData):
                            self.grade = addInfo.grade
                            self.honor = addInfo.honor
                            self.honorDelta = addInfo.honorDelta
                            self.maxHonorForGrade = addInfo.maxHonorForGrade
                            self.minHonorForGrade = addInfo.minHonorForGrade
        elif isinstance(o, FightResultTaxCollectorListEntry):
            taxCollector = o
            info = infos
            if info:
                self.name = (
                    TaxCollectorFirstname.getTaxCollectorFirstnameById(
                        info.firstNameId
                    ).firstname
                    + " "
                    + TaxCollectorName.getTaxCollectorNameById(info.lastNameId).name
                )
            else:
                self.name = taxCollector.guildInfo.guildName
            self.level = taxCollector.level
            self.experienceForGuild = taxCollector.experienceForGuild
            self.id = taxCollector.id
            self.alive = taxCollector.alive
            self.type = 2
        elif isinstance(o, FightResultMutantListEntry):
            mutant = o
            self.name = infos.name
            self.level = mutant.level
            self.id = mutant.id
            self.alive = mutant.alive
            self.type = 0
        elif isinstance(o, FightResultFighterListEntry):
            if isinstance(infos, GameFightMonsterInformations):
                monsterInfos = infos
                monster = Monster.getMonsterById(monsterInfos.creatureGenericId)
                self.name = monster.name
                breachFrame = Kernel().worker.getFrame("BreachFrame")
                if (
                    PlayedCharacterManager().isInBreach
                    and breachFrame
                    and not isSpectator
                ):
                    self.level = breachFrame.floor
                else:
                    self.level = monsterInfos.creatureLevel
                self.id = monster.id
                self.alive = monsterInfos.spawnInfo.alive
                self.type = 1
            elif isinstance(infos, GameFightEntityInformation):
                companionInfos = infos
                companion = Companion.getCompanionById(companionInfos.entityModelId)
                self.name = companion.name
                self.level = companionInfos.level
                self.id = companion.id
                self.alive = companionInfos.spawnInfo.alive
                self.type = 1
        elif isinstance(o, FightResultListEntry):
            pass
