from typing import List

from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.DamagePreview import DamagePreview
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.FighterDataTranslator import FighterDataTranslator
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.BuffManager import BuffManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import FightersStateManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import ActionIdHelper
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import StatBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StateBuff import StateBuff
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightAIInformations import (
    GameFightAIInformations,
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
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterNamedInformations import (
    GameFightFighterNamedInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)
from pydofus2.damageCalculation.fighterManagement.HaxeFighter import HaxeFighter
from pydofus2.damageCalculation.fighterManagement.playerTypeEnum import PlayerTypeEnum


class FighterTranslator(HaxeFighter):
    BOMBS_TYPE_ID = 95
    UPDATED_STATS = [
        "PUSH_DAMAGE_BONUS",
        "PUSH_DAMAGE_REDUCTION",
        "WATER_ELEMENT_RESIST_PERCENT",
        "EARTH_ELEMENT_RESIST_PERCENT",
        "FIRE_ELEMENT_RESIST_PERCENT",
        "AIR_ELEMENT_RESIST_PERCENT",
        "NEUTRAL_ELEMENT_RESIST_PERCENT",
        "RECEIVED_DAMAGE_MULTIPLIER_DISTANCE",
    ]

    def __init__(self, fighterInfos: GameFightFighterInformations, fighterId, isSummondCastPreviewed=False):
        self._fighterInfos = fighterInfos
        buffs = self.initializeBuffs(fighterId)
        level = min(Kernel().fightContextFrame.getFighterLevel(fighterId), 200)
        data = FighterDataTranslator(self._fighterInfos, fighterId)
        super().__init__(
            fighterId,
            level,
            self.getBreed(),
            self.getPlayerType(),
            self._fighterInfos.spawnInfo.teamId,
            self.isAStaticElement(fighterId),
            buffs,
            data,
            isSummondCastPreviewed,
        )

    def isBomb(self):
        if isinstance(self._fighterInfos, GameFightMonsterInformations):
            infos = Monster.getMonsterById(self._fighterInfos.creatureGenericId)
            if infos is not None and infos.type.id == self.BOMBS_TYPE_ID:
                return True
        return False

    def getModelId(self):
        if isinstance(self._fighterInfos, GameFightEntityInformation):
            return self._fighterInfos.entityModelId
        return 0

    def initializeBuffs(self, fighterId: float) -> List:
        unknownBaseStats = not (
            CurrentPlayedFighterManager().currentFighterId == fighterId
            or PlayedCharacterManager().id == fighterId
            or isinstance(self._fighterInfos, GameFightMonsterInformations)
        )
        buffs = []
        for buff in BuffManager().getAllBuff(fighterId):
            if not (isinstance(buff, StatBuff) and not buff.isRecent and unknownBaseStats):
                if not (
                    (unknownBaseStats or isinstance(self._fighterInfos, GameFightMonsterInformations))
                    and ActionIdHelper.getActionIdStatName(buff.actionId) in self.UPDATED_STATS
                ):
                    if buff.stack:
                        for stack in buff.stack:
                            if stack.effect.delay == 0 and (
                                not isinstance(buff, StateBuff)
                                or FightersStateManager().hasState(fighterId, buff.stateId)
                            ):
                                buffs.append(DamagePreview.createHaxeBuff(stack))
                    elif buff.effect.delay == 0 and (
                        not isinstance(buff, StateBuff) or FightersStateManager().hasState(fighterId, buff.stateId)
                    ):
                        buffs.append(DamagePreview.createHaxeBuff(buff))
        return buffs

    def getBreed(self):
        if isinstance(self._fighterInfos, GameFightCharacterInformations):
            return self._fighterInfos.breed
        if isinstance(self._fighterInfos, GameFightMonsterInformations):
            return self._fighterInfos.creatureGenericId
        return -1

    def getPlayerType(self):
        if isinstance(self._fighterInfos, GameFightFighterNamedInformations):
            return PlayerTypeEnum.HUMAN
        if isinstance(self._fighterInfos, GameFightEntityInformation):
            return PlayerTypeEnum.SIDEKICK
        if isinstance(self._fighterInfos, GameFightAIInformations):
            return PlayerTypeEnum.MONSTER
        return PlayerTypeEnum.UNKNOWN

    def isAStaticElement(self, id: float) -> bool:
        fef = Kernel().fightEntitiesFrame
        if fef:
            monsterInfo = fef.getEntityInfos(id)
            if (
                monsterInfo
                and isinstance(monsterInfo, GameFightMonsterInformations)
                and not Monster.getMonsterById(monsterInfo.creatureGenericId).canPlay
            ):
                return True
        return False

    def isAlive(self):
        return self._fighterInfos.spawnInfo.alive and super().isAlive()
