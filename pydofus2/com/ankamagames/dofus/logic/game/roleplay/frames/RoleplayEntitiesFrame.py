from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightUpdateTeamMessage import (
    GameFightUpdateTeamMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayRemoveChallengeMessage import (
    GameRolePlayRemoveChallengeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayShowChallengeMessage import (
    GameRolePlayShowChallengeMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamInformations import FightTeamInformations
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.messages.MapLoadedMessage import MapLoadedMessage
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import (
    WorldPointWrapper,
)
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimerManager import TimeManager
import pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayContextFrame as rcf
import pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayInteractivesFrame as rif
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.messages.CharacterMovementStoppedMessage import (
    CharacterMovementStoppedMessage,
)
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.messages.DelayedActionMessage import (
    DelayedActionMessage,
)
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.Fight import Fight
from pydofus2.com.ankamagames.dofus.network.enums.MapObstacleStateEnum import (
    MapObstacleStateEnum,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.GameRolePlayShowActorMessage import (
    GameRolePlayShowActorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.GameRolePlayShowMultipleActorsMessage import (
    GameRolePlayShowMultipleActorsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsWithCoordsMessage import (
    MapComplementaryInformationsWithCoordsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.anomaly.MapComplementaryInformationsAnomalyMessage import (
    MapComplementaryInformationsAnomalyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveMapUpdateMessage import (
    InteractiveMapUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUsedMessage import (
    InteractiveUsedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.StatedMapUpdateMessage import (
    StatedMapUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import GameContextActorInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightCommonInformations import (
    FightCommonInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayCharacterInformations import (
    GameRolePlayCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayGroupMonsterInformations import (
    GameRolePlayGroupMonsterInformations,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.AbstractEntitiesFrame import (
    AbstractEntitiesFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataInHouseMessage import (
    MapComplementaryInformationsDataInHouseMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataMessage import (
    MapComplementaryInformationsDataMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapInformationsRequestMessage import (
    MapInformationsRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.breach.MapComplementaryInformationsBreachMessage import (
    MapComplementaryInformationsBreachMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayHumanoidInformations import (
    GameRolePlayHumanoidInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayMerchantInformations import (
    GameRolePlayMerchantInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanInformations import HumanInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOptionObjectUse import (
    HumanOptionObjectUse,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOptionSkillUse import (
    HumanOptionSkillUse,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupLightInformations import (
    MonsterInGroupLightInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import (
    InteractiveElement,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.FightTeam import FightTeam
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager, KernelEvts
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.ContextChangeFrame import ContextChangeFrame

logger = Logger("Dofus2")


class RoleplayEntitiesFrame(AbstractEntitiesFrame, Frame):
    
    def __init__(self):
        self._fights = dict[int, Fight]()

        self._objects = dict()

        self._objectsByCellId = dict()

        self._paddockItem = dict()

        self._fightNumber: int = 0

        self._timeout: float = None

        self._currentPaddockItemCellId: int = None

        self._currentEmoticon: int = 0

        self._mapTotalRewardRate: int = 0

        self._playersId: list = None

        self._merchantsList: list = None

        self._npcList = dict()

        self._housesList = dict()

        self._emoteTimesBySprite = dict()

        self._waitForMap: bool = False

        self._monstersIds = list[float]()

        self._lastStaticAnimations = dict()

        self._waitingEmotesAnims = dict()

        self._auraCycleTimer: BenchmarkTimer = None

        self._auraCycleIndex: int = None

        self._lastEntityWithAura: AnimatedCharacter = None

        self._dispatchPlayerNewLook: bool = None

        # self._aggressions = list[Aggression]()

        self._aggroTimeoutIdsMonsterAssoc = dict()
        
        self.mcidm_processessed : bool = False

        super().__init__()

    def pulled(self) -> bool:
        self._fights.clear()
        self._objects.clear()
        self._npcList.clear()
        self._objectsByCellId.clear()
        self._paddockItem.clear()
        self._housesList.clear()
        return super().pulled()

    def pushed(self) -> bool:
        self.initNewMap()
        self._playersId = list()
        self._merchantsList = list()
        self._monstersIds = list[float]()
        self._entitiesVisibleNumber = 0
        self.mcidm_processessed = False
        if MapDisplayManager()._currentMapRendered:
            ccFrame: 'ContextChangeFrame' = Kernel().worker.getFrame("ContextChangeFrame")
            mirmsg = MapInformationsRequestMessage()
            mirmsg.init(mapId_=MapDisplayManager().currentMapPoint.mapId)
            ConnectionsHandler()._conn.send(mirmsg)
            self._waitForMap = False
        else:
            self._waitForMap = True
        self._interactiveElements = list[InteractiveElement]()
        return super().pushed()

    def initNewMap(self):
        self._npcList = dict()
        self._fights = dict()
        self._objects = dict()
        self._objectsByCellId = dict()
        self._paddockItem = dict()

    def process(self, msg: Message):

        if isinstance(msg, MapLoadedMessage):
            if self._waitForMap:
                ccFrame: 'ContextChangeFrame' = Kernel().worker.getFrame("ContextChangeFrame")
                connexion = ""
                if ccFrame:
                    connexion = ccFrame.mapChangeConnexion
                self.mcidm_processessed = False
                mirmsg = MapInformationsRequestMessage()
                mirmsg.init(mapId_=MapDisplayManager().currentMapPoint.mapId)
                ConnectionsHandler()._conn.send(mirmsg)
                self._waitForMap = False
            return False

        elif isinstance(msg, MapComplementaryInformationsDataMessage):
            mcidmsg = msg
            currentMapHasChanged = False
            currentSubAreaHasChanged = False
            self._interactiveElements = mcidmsg.interactiveElements
            self._fightfloat = len(mcidmsg.fights)
            self._mapTotalRewardRate = 0

            if isinstance(msg, MapComplementaryInformationsBreachMessage):
                mcidm = msg
                if mcidm.subAreaId != DataEnum.SUBAREA_INFINITE_BREACH:
                    pass
                if PlayedCharacterManager().isInBreach:
                    PlayedCharacterManager().isInBreach = False

            if PlayedCharacterManager().isInHouse and not isinstance(
                msg, MapComplementaryInformationsDataInHouseMessage
            ):
                PlayedCharacterManager().isInHouse = False
                PlayedCharacterManager().isInHisHouse = False

            if PlayedCharacterManager().isIndoor and not isinstance(
                msg, MapComplementaryInformationsWithCoordsMessage
            ):
                PlayedCharacterManager().isIndoor = False

            if isinstance(msg, MapComplementaryInformationsWithCoordsMessage):
                mciwcmsg = msg
                PlayedCharacterManager().isIndoor = True
                self._worldPoint = WorldPointWrapper(mciwcmsg.mapId, True, mciwcmsg.worldX, mciwcmsg.worldY)

            elif isinstance(msg, MapComplementaryInformationsDataInHouseMessage):
                mcidihmsg = msg
                isPlayerHouse = (
                    PlayerManager().nickname == mcidihmsg.currentHouse.houseInfos.ownerTag.nickname
                    and PlayerManager().tag == mcidihmsg.currentHouse.houseInfos.ownerTag.tagNumber
                )
                PlayedCharacterManager().isInHouse = True
                if isPlayerHouse:
                    PlayedCharacterManager().isInHisHouse = True
                self._housesList = dict()
                self._housesList[0] = HouseWrapper.createInside(mcidihmsg.currentHouse)
                self._worldPoint = WorldPointWrapper(
                    mcidihmsg.mapId,
                    True,
                    mcidihmsg.currentHouse.worldX,
                    mcidihmsg.currentHouse.worldY,
                )

            else:
                self._worldPoint = WorldPointWrapper(int(mcidmsg.mapId))

            roleplayContextFrame: rcf.RoleplayContextFrame = Kernel().worker.getFrame("RoleplayContextFrame")
            previousMap = PlayedCharacterManager().currentMap
            if (
                roleplayContextFrame.newCurrentMapIsReceived
                or previousMap.mapId != self._worldPoint.mapId
                or previousMap.outdoorX != self._worldPoint.outdoorX
                or previousMap.outdoorY != self._worldPoint.outdoorY
            ):
                currentMapHasChanged = True
                PlayedCharacterManager().currentMap = self._worldPoint

            roleplayContextFrame.newCurrentMapIsReceived = False
            if self._currentSubAreaId != mcidmsg.subAreaId or not PlayedCharacterManager().currentSubArea:
                currentSubAreaHasChanged = True
                self._currentSubAreaId = mcidmsg.subAreaId
                newSubArea = SubArea.getSubAreaById(self._currentSubAreaId)
                PlayedCharacterManager().currentSubArea = newSubArea

            self._playersId = list()
            self._monstersIds = list[float]()

            for actor in mcidmsg.actors:
                if actor.contextualId > 0:
                    self._playersId.append(actor.contextualId)
                elif isinstance(actor, GameRolePlayGroupMonsterInformations):
                    self._monstersIds.append(actor.contextualId)

            self._entitiesVisibleNumber = len(self._playersId) + len(self._monstersIds)
            mapWithNoMonsters = True
            for actor1 in mcidmsg.actors:
                ac = self.addOrUpdateActor(actor1)
                if ac:
                    if ac.id == PlayedCharacterManager().id:
                        ac.speedAdjust = PlayedCharacterManager().speedAjust
                    character = actor1
                    if isinstance(character, GameRolePlayCharacterInformations):
                        for option in character.humanoidInfo.options:
                            if isinstance(option, HumanOptionObjectUse):
                                dam = DelayedActionMessage(
                                    character.contextualId,
                                    option.objectGID,
                                    option.delayEndTime,
                                )
                                Kernel().worker.process(dam)
                            elif isinstance(option, HumanOptionSkillUse):
                                hosu = option
                                duration = hosu.skillEndTime - TimeManager().getUtcTimestamp()
                                duration /= 100
                                if duration > 0:
                                    iumsg = InteractiveUsedMessage.from_json(
                                        {
                                            "__type__": "InteractiveUsedMessage",
                                            "skillId": hosu.skillId,
                                            "duration": duration,
                                            "entityId": character.contextualId,
                                            "elemId": hosu.elementId,
                                        }
                                    )
                                    Kernel().worker.process(iumsg)
                if mapWithNoMonsters:
                    if isinstance(actor1, GameRolePlayGroupMonsterInformations):
                        mapWithNoMonsters = False
                        # TODO: Here notify the bot that map contains monsters

                if isinstance(actor1, GameRolePlayCharacterInformations):
                    pass

                elif isinstance(actor1, GameRolePlayMerchantInformations):
                    self._merchantsList.append(actor1)

            self._merchantsList.sort(key=lambda x: x.name)
            selfFightExists = False
            fightIdsToRemove = list()

            for fight in mcidmsg.fights:
                selfFightExists = False
                for fightCache in self._fights.values():
                    if fight.fightId == fightCache.fightId:
                        selfFightExists = True
                if not selfFightExists:
                    self.addFight(fight)

            for fightCache in self._fights.values():
                selfFightExists = False
                for fight in mcidmsg.fights:
                    if fight.fightId == fightCache.fightId:
                        selfFightExists = True
                if not selfFightExists:
                    fightIdsToRemove.append(fightCache.fightId)

            for fightId in fightIdsToRemove:
                del self._fights[fightId]

            if currentMapHasChanged:
                for mo in mcidmsg.obstacles:
                    DataMapProvider().updateCellMovLov(
                        mo.obstacleCellId,
                        mo.state == MapObstacleStateEnum.OBSTACLE_OPENED,
                    )

            rpIntFrame: rif.RoleplayInteractivesFrame = Kernel().worker.getFrame("RoleplayInteractivesFrame")
            if rpIntFrame:
                imumsg = InteractiveMapUpdateMessage()
                imumsg.init(mcidmsg.interactiveElements)
                rpIntFrame.process(imumsg)
                smumsg = StatedMapUpdateMessage()
                smumsg.init(mcidmsg.statedElements)
                rpIntFrame.process(smumsg)

            if currentMapHasChanged or currentSubAreaHasChanged:
                # TODO: Here you notify the bot throught BotEventsManager that the map(or subarea) has changed
                pass

            if isinstance(msg, MapComplementaryInformationsAnomalyMessage):
                PlayedCharacterManager().isInAnomaly = True

            elif PlayedCharacterManager().isInAnomaly:
                PlayedCharacterManager().isInAnomaly = False
            
            logger.debug("MapComplementaryInformationsDataMessage processed")
            self.mcidm_processessed = True
            return False

        if isinstance(msg, CharacterMovementStoppedMessage):
            # TODO: notify bot here that he stopped moving for some usecases
            return True

        if isinstance(msg, GameRolePlayShowActorMessage):
            KernelEventsManager().send(KernelEvts.ACTORSHOWED, msg.informations)
            if int(msg.informations.contextualId) == int(PlayedCharacterManager().id):
                humi: HumanInformations = msg.informations.humanoidInfo
                PlayedCharacterManager().restrictions = humi.restrictions
                PlayedCharacterManager().infos.entityLook = msg.informations.look
                infos: GameRolePlayHumanoidInformations = self.getEntityInfos(PlayedCharacterManager().id)
                if infos:
                    infos.humanoidInfo.restrictions = PlayedCharacterManager().restrictions
            self.addOrUpdateActor(msg.informations)
            if isinstance(msg.informations, GameRolePlayMerchantInformations):
                self._merchantsList.append(msg.informations)
                self._merchantsList.sort(key=lambda e: e.name)
            return True

        if isinstance(msg, GameRolePlayShowMultipleActorsMessage):
            grpsmamsg = msg
            for actorInformation in grpsmamsg.informationsList:
                fakeShowActorMsg = GameRolePlayShowActorMessage()
                fakeShowActorMsg.informations = actorInformation
                self.process(fakeShowActorMsg)
            return True

        elif isinstance(msg, GameFightUpdateTeamMessage):
            gfutmsg = msg
            self.updateFight(gfutmsg.fightId, gfutmsg.team)
            return True

        elif isinstance(msg, GameRolePlayShowChallengeMessage):
            grpsclmsg = msg
            self.addFight(grpsclmsg.commonsInfos)
            return True

        elif isinstance(msg, GameRolePlayRemoveChallengeMessage):
            self.removeFight(msg.fightId)

    def removeFight(self, fightId: int) -> None:
        fight: Fight = self._fights.get(fightId)
        if fight is None:
            return
        for team in fight.teams:
            logger.debug(f"Removing the team {team.teamEntity.id}")
            self.unregisterActor(team.teamEntity.id)
            del team.teamEntity
        del self._fights[fightId]

    def updateFight(self, fightId: int, team: FightTeamInformations) -> None:
        present: bool = False
        fight: Fight = self._fights.get(fightId)
        if fight is None:
            return
        fightTeam: FightTeam = fight.getTeamById(team.teamId)
        tInfo: FightTeamInformations = self._entities[fightTeam.teamEntity.id].teamInfos
        if tInfo.teamMembers == team.teamMembers:
            return
        for newMember in team.teamMembers:
            present = False
            for teamMember in tInfo.teamMembers:
                if teamMember.id == newMember.id:
                    present = True
            if not present:
                tInfo.teamMembers.append(newMember)

    def isFight(self, entityId: int) -> bool:
        if not self._entities:
            return False
        return isinstance(self._entities[entityId], FightTeam)

    def getFightId(self, entityId: int) -> int:
        if isinstance(self._entities[entityId], FightTeam):
            return self._entities[entityId].fight.fightId

    def getFightLeaderId(self, entityId: int) -> int:
        if isinstance(self._entities[entityId], FightTeam):
            return self._entities[entityId].teamInfos.leaderId

    def getFightTeamType(self, entityId: int) -> int:
        if isinstance(self._entities[entityId], FightTeam):
            return self._entities[entityId].teamType

    def addFight(self, infos: FightCommonInformations):
        teamEntity: IEntity = AnimatedCharacter(EntitiesManager().getFreeEntityId())
        fightTeam: "FightTeam" = None
        if self._fights.get(infos.fightId):
            return
        teams = list["FightTeam"]()
        fight: Fight = Fight(infos.fightId, teams)
        teamCounter: int = 0
        for team in infos.fightTeams:
            fightTeam = FightTeam(
                fight,
                team.teamTypeId,
                teamEntity,
                team,
                infos.fightTeamsOptions[team.teamId],
            )
            self.registerActorWithId(fightTeam, teamEntity.id)
            teams.append(fightTeam)
            teamCounter += 1
        self._fights[infos.fightId] = fight

    def updateMonstersGroup(self, pMonstersInfo: GameRolePlayGroupMonsterInformations) -> None:
        monstersGroup: list[MonsterInGroupLightInformations] = self.getMonsterGroup(pMonstersInfo.staticInfos)
        groupHasMiniBoss: bool = Monster.getMonsterById(
            pMonstersInfo.staticInfos.mainCreatureLightInfos.genericId
        ).isMiniBoss
        if monstersGroup:
            for monsterInfos in monstersGroup:
                if monsterInfos.genericId == pMonstersInfo.staticInfos.mainCreatureLightInfos.genericId:
                    monstersGroup.remove(monsterInfos)
        for underling in pMonstersInfo.staticInfos.underlings:
            if not groupHasMiniBoss and Monster.getMonsterById(underling.genericId).isMiniBoss:
                groupHasMiniBoss = True

    def updateMonstersGroups(self) -> None:
        entityInfo: GameContextActorInformations = None
        entities: dict = entities
        for entityInfo in entities:
            if isinstance(entityInfo, GameRolePlayGroupMonsterInformations):
                self.updateMonstersGroup(entityInfo)
