import threading

from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.messages.MapLoadedMessage import MapLoadedMessage
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import WorldPointWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.AbstractEntitiesFrame import AbstractEntitiesFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import TimeManager
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.messages.DelayedActionMessage import DelayedActionMessage
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.Fight import Fight
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.FightTeam import FightTeam
from pydofus2.com.ankamagames.dofus.network.enums.MapObstacleStateEnum import MapObstacleStateEnum
from pydofus2.com.ankamagames.dofus.network.messages.common.basic.BasicPingMessage import BasicPingMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightUpdateTeamMessage import (
    GameFightUpdateTeamMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextRefreshEntityLookMessage import (
    GameContextRefreshEntityLookMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextRemoveElementMessage import (
    GameContextRemoveElementMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextRemoveMultipleElementsMessage import (
    GameContextRemoveMultipleElementsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapChangeOrientationMessage import (
    GameMapChangeOrientationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.anomaly.MapComplementaryInformationsAnomalyMessage import (
    MapComplementaryInformationsAnomalyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayRemoveChallengeMessage import (
    GameRolePlayRemoveChallengeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayShowChallengeMessage import (
    GameRolePlayShowChallengeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.GameRolePlayShowActorMessage import (
    GameRolePlayShowActorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.GameRolePlayShowMultipleActorsMessage import (
    GameRolePlayShowMultipleActorsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.houses.HousePropertiesMessage import (
    HousePropertiesMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataInHavenBagMessage import (
    MapComplementaryInformationsDataInHavenBagMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataInHouseMessage import (
    MapComplementaryInformationsDataInHouseMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataMessage import (
    MapComplementaryInformationsDataMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsWithCoordsMessage import (
    MapComplementaryInformationsWithCoordsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapFightCountMessage import (
    MapFightCountMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapInformationsRequestMessage import (
    MapInformationsRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.npc.ListMapNpcsQuestStatusUpdateMessage import (
    ListMapNpcsQuestStatusUpdateMessage,
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
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightCommonInformations import (
    FightCommonInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamInformations import FightTeamInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import (
    GameContextActorInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameRolePlayTaxCollectorInformations import (
    GameRolePlayTaxCollectorInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayCharacterInformations import (
    GameRolePlayCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayGroupMonsterInformations import (
    GameRolePlayGroupMonsterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayHumanoidInformations import (
    GameRolePlayHumanoidInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayMerchantInformations import (
    GameRolePlayMerchantInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayMountInformations import (
    GameRolePlayMountInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayNpcInformations import (
    GameRolePlayNpcInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayNpcWithQuestInformations import (
    GameRolePlayNpcWithQuestInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayPortalInformations import (
    GameRolePlayPortalInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayPrismInformations import (
    GameRolePlayPrismInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayTreasureHintInformations import (
    GameRolePlayTreasureHintInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GroupMonsterStaticInformationsWithAlternatives import (
    GroupMonsterStaticInformationsWithAlternatives,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanInformations import HumanInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOptionObjectUse import (
    HumanOptionObjectUse,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOptionSkillUse import HumanOptionSkillUse
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupLightInformations import (
    MonsterInGroupLightInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import InteractiveElement
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ClientStatusEnum import ClientStatusEnum


class RoleplayEntitiesFrame(AbstractEntitiesFrame, Frame):
    MAX_MAPDATA_REQ_FAILS = 3
    MAPDATA_REQ_TIMEOUT = 20

    def __init__(self):
        self._fights = dict[int, Fight]()
        self._objects = dict()
        self._fightNumber: int = 0
        self._playersId = list()
        self._merchantsList = list["GameRolePlayMerchantInformations"]()
        self._npcList = dict()
        self._housesList = dict()
        self._waitForMap: bool = False
        self._monstersIds = list[float]()
        self.mcidm_processed: bool = False
        self.mapDataRequestTimer = None
        self.treasureHuntNpc = None
        self.nbrFails = 0
        self.processingMapData = threading.Event()
        super().__init__()

    def pulled(self) -> bool:
        self._fights.clear()
        self._objects.clear()
        self._npcList.clear()
        self._housesList.clear()
        self.mcidm_processed = False
        return super().pulled()

    def pushed(self) -> bool:
        self.nbrFails = 0
        self.initNewMap()
        self.mcidm_processed = False
        if MapDisplayManager()._currentMapRendered:
            self.requestMapData()
        else:
            self._waitForMap = True
        return super().pushed()

    def initNewMap(self):
        self._npcList = dict()
        self._fights = dict()
        self._objects = dict()
        self._entities.clear()
        self._interactiveElements = list[InteractiveElement]()
        self._playersId = list[float]()
        self._merchantsList = list["GameRolePlayMerchantInformations"]()
        self._monstersIds = list[float]()
        self._fightfloat = None
        self._currentSubAreaId = None
        self.mapWithNoMonsters = True
        self._isIndoor = None
        self._worldPoint = None
        self._housesList = []
        self.treasureHuntNpc = False

    def requestMapData(self):
        KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.REQUESTING_MAP_DATA)
        self.mcidm_processed = False
        self._waitForMap = False
        self.sendMapDataRequest()

    def ontimeout(self):
        Logger().warning("Map data request timeout")
        pingMsg = BasicPingMessage()
        pingMsg.init(True)
        ConnectionsHandler().send(pingMsg)
        self.nbrFails += 1
        if self.nbrFails > self.MAX_MAPDATA_REQ_FAILS:
            return KernelEventsManager().send(KernelEvent.ClientRestart, "map data request timeout")
        self.sendMapDataRequest()

    def sendMapDataRequest(self):
        if self.mapDataRequestTimer:
            self.mapDataRequestTimer.cancel()
        # Logger().info(f"Requesting data for map {MapDisplayManager().currentMapPoint.mapId}")
        self.mapDataRequestTimer = BenchmarkTimer(self.MAPDATA_REQ_TIMEOUT, self.ontimeout)
        self.mapDataRequestTimer.start()
        msg = MapInformationsRequestMessage()
        msg.init(MapDisplayManager().currentMapPoint.mapId)
        ConnectionsHandler().send(msg)

    def process(self, msg: Message):

        if isinstance(msg, MapLoadedMessage):
            if self._waitForMap:
                self.nbrFails = 0
                self.requestMapData()
            return False

        elif isinstance(msg, MapComplementaryInformationsDataMessage):
            # Logger().info("Map data received")
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.MAP_DATA_RECEIVED)
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.PROCESSING_MAP_DATA)
            if self.mapDataRequestTimer:
                self.mapDataRequestTimer.cancel()
            self.processingMapData.clear()
            currentMapHasChanged = False
            self._interactiveElements = msg.interactiveElements
            self._fightfloat = len(msg.fights)

            if PlayedCharacterManager().isIndoor and not isinstance(
                msg, MapComplementaryInformationsWithCoordsMessage
            ):
                PlayedCharacterManager().isIndoor = False

            if isinstance(msg, MapComplementaryInformationsWithCoordsMessage):
                PlayedCharacterManager().isIndoor = True
                self._worldPoint = WorldPointWrapper(msg.mapId, True, msg.worldX, msg.worldY)

            elif isinstance(msg, MapComplementaryInformationsDataInHouseMessage):
                self.checkPlayerInHouse(msg)
                self._worldPoint = WorldPointWrapper(
                    msg.mapId,
                    True,
                    msg.currentHouse.worldX,
                    msg.currentHouse.worldY,
                )
            else:
                self._worldPoint = WorldPointWrapper(int(msg.mapId))
            self._isIndoor = PlayedCharacterManager().isIndoor
            roleplayContextFrame = Kernel().roleplayContextFrame
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
            if self._currentSubAreaId != msg.subAreaId or not PlayedCharacterManager().currentSubArea:
                self._currentSubAreaId = msg.subAreaId
                newSubArea = SubArea.getSubAreaById(self._currentSubAreaId)
                PlayedCharacterManager().currentSubArea = newSubArea

            self._playersId = list[float]()
            self._monstersIds = list[float]()
            for actor in msg.actors:
                if actor.contextualId > 0:
                    self._playersId.append(actor.contextualId)
                elif isinstance(actor, GameRolePlayGroupMonsterInformations):
                    self._monstersIds.append(actor.contextualId)
                elif isinstance(actor, GameRolePlayTreasureHintInformations):
                    self.treasureHuntNpc = actor
                    Kernel().questFrame.process(actor)

            self.mapWithNoMonsters = True
            for actor1 in msg.actors:
                ac = self.addOrUpdateActor(actor1)
                if ac:
                    if ac.id == PlayedCharacterManager().id:
                        ac.speedAdjust = PlayedCharacterManager().speedAdjust
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
                                    iumsg = InteractiveUsedMessage()
                                    iumsg.init(character.contextualId, hosu.elementId, hosu.skillId, duration, True)
                                    Kernel().worker.process(iumsg)
                if self.mapWithNoMonsters:
                    if isinstance(actor1, GameRolePlayGroupMonsterInformations):
                        self.mapWithNoMonsters = False
                elif isinstance(actor1, GameRolePlayMerchantInformations):
                    self._merchantsList.append(actor1)

            self._merchantsList.sort(key=lambda x: x.name)
            self._fights.clear()
            for fight in msg.fights:
                self.addFight(fight)
            if currentMapHasChanged:
                for mo in msg.obstacles:
                    DataMapProvider().updateCellMovLov(
                        mo.obstacleCellId,
                        mo.state == MapObstacleStateEnum.OBSTACLE_OPENED,
                    )
            if Kernel().interactiveFrame:
                imumsg = InteractiveMapUpdateMessage()
                imumsg.init(msg.interactiveElements)
                Kernel().interactiveFrame.process(imumsg)
                smumsg = StatedMapUpdateMessage()
                smumsg.init(msg.statedElements)
                Kernel().interactiveFrame.process(smumsg)

            if isinstance(msg, MapComplementaryInformationsAnomalyMessage):
                PlayedCharacterManager().isInAnomaly = True

            elif PlayedCharacterManager().isInAnomaly:
                PlayedCharacterManager().isInAnomaly = False
            self._isInAnomaly = PlayedCharacterManager().isInAnomaly
            self.mcidm_processed = True
            self.processingMapData.set()
            KernelEventsManager().send(KernelEvent.MapDataProcessed, msg.mapId)
            if type(msg) is MapComplementaryInformationsDataInHavenBagMessage:
                Logger().debug("Played entered haven bag")
                KernelEventsManager().send(KernelEvent.InHavenBag)
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.MAP_DATA_PROCESSED)
            return True

        if isinstance(msg, GameRolePlayShowActorMessage):
            # Logger().debug(f"Actor {msg.informations.contextualId} showed")
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
            if isinstance(msg.informations, GameRolePlayHumanoidInformations):
                KernelEventsManager().send(KernelEvent.ActorShowed, msg.informations)
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
            return True

        elif isinstance(msg, GameContextRemoveElementMessage):
            if msg.id in self._playersId:
                self._playersId.remove(msg.id)

            merchant_index = -1
            for i, merchant in enumerate(self._merchantsList):
                if merchant.contextualId == msg.id:
                    merchant_index = i
                    break

            if merchant_index > -1:
                del self._merchantsList[merchant_index]

            if msg.id in self._monstersIds:
                self._monstersIds.remove(msg.id)

            self.removeActor(msg.id)
            KernelEventsManager().send(KernelEvent.EntityVanished, msg.id)
            return True

        elif isinstance(msg, GameContextRemoveMultipleElementsMessage):
            gcrmemsg = msg
            for element_id in gcrmemsg.elementsIds:
                self.process(GameContextRemoveElementMessage(element_id))
            return True

        elif isinstance(msg, HousePropertiesMessage):
            return True

        elif isinstance(msg, GameContextRefreshEntityLookMessage):
            return True

        elif isinstance(msg, GameMapChangeOrientationMessage):
            return True

        elif isinstance(msg, ListMapNpcsQuestStatusUpdateMessage):
            return True

        elif isinstance(msg, MapFightCountMessage):
            KernelEventsManager().send(KernelEvent.MapFightCount, msg.fightCount)
            return True

    def checkPlayerInHouse(self, msg: MapComplementaryInformationsDataInHouseMessage):
        isPlayerHouse = (
            PlayerManager().nickname == msg.currentHouse.houseInfos.ownerTag.nickname
            and PlayerManager().tag == msg.currentHouse.houseInfos.ownerTag.tagNumber
        )
        PlayedCharacterManager().isInHouse = True
        if isPlayerHouse:
            PlayedCharacterManager().isInHisHouse = True

    def removeFight(self, fightId: int) -> None:
        fight: Fight = self._fights.get(fightId)
        if fight is None:
            return
        for team in fight.teams:
            Logger().debug(f"Removing the team {team.teamEntity.id}")
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
        teamEntity = AnimatedCharacter(EntitiesManager().getFreeEntityId())
        teamEntity.show()
        if self._fights.get(infos.fightId):
            return
        teams = list["FightTeam"]()
        fight = Fight(infos.fightId, teams)
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
        self._fights[infos.fightId] = fight
        Logger().info(
            f"Fight({infos.fightId}) appeared with team entities {['leader : ' + str(ft.leaderId) + ', cell: ' + str(infos.fightTeamsPositions[ft.teamId]) for ft in infos.fightTeams]}."
        )
        KernelEventsManager().send(KernelEvent.FightSwordShowed, infos)

    def getMonsterGroup(self, pStaticMonsterInfos):
        newGroup = None
        pmf = None
        nbMembers = 0
        infos = (
            pStaticMonsterInfos
            if isinstance(pStaticMonsterInfos, GroupMonsterStaticInformationsWithAlternatives)
            else None
        )

        if infos:
            pmf = Kernel().partyFrame
            partyMembers = pmf.partyMembers if pmf else None
            nbMembers = len(partyMembers) if partyMembers else 0

            if nbMembers == 0 and PlayedCharacterManager().hasCompanion:
                nbMembers = 2
            else:
                for member in partyMembers:
                    nbMembers += len(member.companions)

            for monsterGroup in infos.alternatives:
                if not newGroup or monsterGroup.playerCount <= nbMembers:
                    newGroup = monsterGroup.monsters[:]

        return newGroup.copy() if newGroup else None

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

    def addOrUpdateActor(self, infos: GameContextActorInformations) -> AnimatedCharacter:
        ac = super().addOrUpdateActor(infos)
        if isinstance(infos, GameRolePlayNpcWithQuestInformations):
            self._npcList[infos.contextualId] = ac
        elif isinstance(infos, GameRolePlayGroupMonsterInformations):
            groupHasMiniBoss = Monster.getMonsterById(infos.staticInfos.mainCreatureLightInfos.genericId).isMiniBoss
            if not groupHasMiniBoss and infos.staticInfos.underlings:
                for migi in infos.staticInfos.underlings:
                    groupHasMiniBoss = Monster.getMonsterById(migi.genericId).isMiniBoss
                    if groupHasMiniBoss:
                        break
                else:
                    # Only execute if the loop completes without breaking
                    self.updateMonstersGroup(infos)
                    if infos.contextualId not in self._monstersIds:
                        self._monstersIds.append(infos.contextualId)
            else:
                # If there are no underlings or if groupHasMiniBoss is already True
                self.updateMonstersGroup(infos)
                if infos.contextualId not in self._monstersIds:
                    self._monstersIds.append(infos.contextualId)
        elif isinstance(infos, GameRolePlayHumanoidInformations):
            if infos.contextualId and self._playersId and infos.contextualId not in self._playersId:
                self._playersId.append(infos.contextualId)
        elif isinstance(infos, GameRolePlayNpcInformations):
            self._npcList[infos.contextualId] = ac
        elif isinstance(
            infos,
            (
                GameRolePlayTaxCollectorInformations,
                GameRolePlayPrismInformations,
                GameRolePlayPortalInformations,
                GameRolePlayMountInformations,
            ),
        ):
            ac.allowMovementThrough = True
        else:
            Logger().error(f"Unknown actor type {type(infos)}")
