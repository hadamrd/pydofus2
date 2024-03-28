import pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager as pcm
from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import \
    EntitiesManager
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import \
    StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import \
    DofusEntities
from pydofus2.com.ankamagames.dofus.network.messages.game.context.EntityDispositionInformations import \
    EntityDispositionInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
    GameFightFighterInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import \
    GameFightMonsterInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import \
    GameContextActorInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayHumanoidInformations import \
    GameRolePlayHumanoidInformations
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import \
    InteractiveElement
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import \
    AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class AbstractEntitiesFrame(Frame):

    def __init__(self):
        self._entities = dict[int, GameContextActorInformations]()
        self._interactiveElements = list[InteractiveElement]()
        self._carriedEntities = dict()
        self._pendingCarriedEntities = dict()
        self._currentSubAreaId = None
        super().__init__()

    def pulled(self) -> bool:
        self._entities = dict[int, GameContextActorInformations]()
        self._interactiveElements = list[InteractiveElement]()
        self._entitiesIcons = dict()
        self._carriedEntities = dict()
        self._pendingCarriedEntities = dict()
        EntitiesManager().clearEntities()
        return True

    @property
    def entities(self):
        return self._entities

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        self._entities = dict()
        self._interactiveElements = list[InteractiveElement]()
        return True

    @property
    def interactiveElements(self) -> list[InteractiveElement]:
        return self._interactiveElements

    def process(msg: Message) -> bool:
        raise NotImplementedError()

    def getEntityInfos(self, entityId: float) -> GameContextActorInformations:
        if entityId == 0 or entityId is None:
            return None
        return self._entities.get(float(entityId))

    def updateEntityCellId(self, entityId, cellId) -> None:
        entityId = float(entityId)
        info = self.getEntityInfos(entityId)
        if info:
            info.disposition.cellId = cellId
            self._entities[entityId] = info

    def getEntitiesIdsList(self) -> list[float]:
        entitiesList = [gcai.contextualId for gcai in self._entities.values()]
        return entitiesList

    def hasEntity(self, entityId: float) -> bool:
        return self._entities is not None and entityId in self._entities

    def registerActor(self, infos: GameContextActorInformations) -> None:
        self.registerActorWithId(infos, infos.contextualId)

    def registerActorWithId(self, infos: GameContextActorInformations, actorId: float) -> None:
        actorId = float(actorId)
        if self._entities is None:
            self._entities = dict[int, GameContextActorInformations]()
        if actorId not in self._entities:
            self._entities[actorId] = infos
            # Logger().info(f"Registred Actor {actorId}")
        if isinstance(infos, GameFightFighterInformations):
            StatsManager().addRawStats(actorId, infos.stats.characteristics.characteristics)

    def unregisterActor(self, actorId: float) -> None:
        actorId = float(actorId)
        if self._entities.get(actorId):
            del self._entities[actorId]
            # Logger().debug(f"Actor {actorId} removed from the scene")
        StatsManager().deleteStats(actorId)

    def addOrUpdateActor(self, infos: GameContextActorInformations) -> AnimatedCharacter:
        characterEntity: AnimatedCharacter = DofusEntities().getEntity(infos.contextualId)
        self.registerActor(infos)
        if isinstance(infos, GameFightFighterInformations):
            StatsManager().addRawStats(infos.contextualId, infos.stats.characteristics.characteristics)
        if characterEntity is None:
            characterEntity = AnimatedCharacter(infos.contextualId)
            if isinstance(infos, GameFightMonsterInformations):
                characterEntity.speedAdjust = Monster.getMonsterById(infos.creatureGenericId).speedAdjust
            EntitiesManager().addEntity(infos.contextualId, characterEntity)
            if infos.contextualId == pcm.PlayedCharacterManager().id:
                KernelEventsManager().send(KernelEvent.PlayerAddedToSceene, characterEntity)
            # else:
            #     KernelEventsManager().send(KernelEvent.ActorShowed, characterEntity)
        else:
            if infos.contextualId == pcm.PlayedCharacterManager().id:
                # Logger().info(f"Current Player updated on the sceene")
                pass
        if isinstance(infos, GameRolePlayHumanoidInformations):
            if infos.contextualId == pcm.PlayedCharacterManager().id:
                pcm.PlayedCharacterManager().restrictions = infos.humanoidInfo.restrictions
        if infos.disposition.cellId != -1:
            characterEntity.position = MapPoint.fromCellId(infos.disposition.cellId)
        return characterEntity

    def updateActorDisposition(self, actorId: float, newDisposition: EntityDispositionInformations) -> None:
        actorId = float(actorId)
        if self._entities.get(actorId):
            self._entities[actorId].disposition = newDisposition
        else:
            Logger().error(f"Cannot update unknown actor disposition ({actorId}) in informations.")

    def removeActor(self, actorId: float) -> None:
        self.unregisterActor(actorId)

    def addCarrier(
        self,
        carrierEntity: AnimatedCharacter,
        carriedEntity: AnimatedCharacter,
        isPending: bool = False,
    ) -> None:
        if carrierEntity is None or carriedEntity is None:
            return

        if carriedEntity.id in self._pendingCarriedEntities:
            del self._pendingCarriedEntities[carriedEntity.id]

        if carriedEntity.id in self._entitiesIcons:
            self._carriedEntities[carriedEntity.id] = carrierEntity

        elif isPending:
            self._pendingCarriedEntities[carriedEntity.id] = {
                "carrierEntity": carrierEntity,
                "carriedEntity": carriedEntity,
            }
