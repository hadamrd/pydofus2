from time import perf_counter

from pydofus2.com.ankamagames.berilia.managers.EventsHandler import Event, EventsHandler, Listener
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightCommonInformations import (
    FightCommonInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayHumanoidInformations import (
    GameRolePlayHumanoidInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyMemberInformations import (
    PartyMemberInformations,
)
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.positions.MovementPath import MovementPath


class KernelEventsManager(EventsHandler, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    def onceFramePushed(self, frameName, callback, args=[], originator=None):
        def onEvt(evt: Event, frame):
            if str(frame) == frameName:
                evt.listener.delete()
                callback(*args)

        return self.on(KernelEvent.FramePushed, onEvt, originator=originator)

    def onceFramePulled(self, frameName, callback, args=[], originator=None):
        def onEvt(e: Event, frame):
            if str(frame) == frameName:
                e.listener.delete()
                callback(*args)

        return self.on(KernelEvent.FramePulled, onEvt, originator=originator)

    def onceMapProcessed(
        self, callback, args=[], mapId=None, timeout=None, ontimeout=None, originator=None
    ) -> "Listener":
        once = mapId is None
        startTime = perf_counter()

        def onEvt(event: Event, processedMapId):
            if mapId is not None:
                if processedMapId == mapId:
                    event.listener.delete()
                    return callback(*args)
                if timeout:
                    remaining = timeout - (perf_counter() - startTime)
                    if remaining > 0:
                        event.listener.armTimer(remaining)
                    else:
                        ontimeout(event.listener)
            else:
                callback(*args)

        return self.on(
            KernelEvent.MapDataProcessed, onEvt, once=once, timeout=timeout, ontimeout=ontimeout, originator=originator
        )

    def send(self, event_id: KernelEvent, *args, **kwargs):
        self._listeners.get(event_id, [])
        if event_id == KernelEvent.ClientCrashed:
            self._crashMessage = kwargs.get("message", None)
        super().send(event_id, *args, **kwargs)

    def onceActorShowed(self, actorId, callback, args=[], originator=None):
        def onActorShowed(event: Event, infos: "GameRolePlayHumanoidInformations"):
            if int(actorId) == int(infos.contextualId):
                event.listener.delete()
                callback(*args)

        return self.on(KernelEvent.ActorShowed, onActorShowed, originator=originator)

    def onEntityMoved(self, entityId, callback, timeout=None, ontimeout=None, once=False, originator=None):
        startTime = perf_counter()

        def onEntityMoved(event: Event, movedEntityId, clientMovePath: MovementPath):
            if movedEntityId == entityId:
                if once:
                    event.listener.delete()
                return callback(event, clientMovePath)
            if timeout:
                remaining = timeout - (perf_counter() - startTime)
                if remaining > 0:
                    event.listener.armTimer(remaining)
                else:
                    ontimeout(event.listener)

        return self.on(
            KernelEvent.EntityMoving, onEntityMoved, timeout=timeout, ontimeout=ontimeout, originator=originator
        )

    def onceEntityMoved(self, entityId, callback, timeout=None, ontimeout=None, originator=None):
        return self.onEntityMoved(
            entityId, callback, timeout=timeout, ontimeout=ontimeout, once=True, originator=originator
        )

    def onceEntityVanished(self, entityId, callback, args=[], originator=None):
        def onEntityVanished(event: Event, vanishedEntityId):
            if vanishedEntityId == entityId:
                event.listener.delete()
                callback(*args)

        return self.on(KernelEvent.EntityVanished, onEntityVanished, originator=originator)

    def onceFightSword(self, entityId, entityCell, callback, args=[], originator=None):
        def onFightSword(event: Event, infos: FightCommonInformations):
            for team in infos.fightTeams:
                if team.leaderId == entityId:
                    event.listener.delete()
                    callback(*args)

        return self.on(KernelEvent.FightSwordShowed, onFightSword, originator=originator)

    def onceFightStarted(self, callback, timeout, ontimeout, retryNbr=None, retryAction=None, originator=None):
        return self.on(
            KernelEvent.FightStarted,
            callback,
            timeout=timeout,
            ontimeout=ontimeout,
            once=True,
            retryNbr=retryNbr,
            retryAction=retryAction,
            originator=originator,
        )

    def onceMemberJoinedParty(self, memberId, callback, args=[], timeout=None, ontimeout=None, originator=None):
        startTime = perf_counter()

        def onNewMember(event: Event, partyId, member: PartyMemberInformations):
            if member.id == memberId:
                event.listener.delete()
                return callback(*args)
            if timeout:
                remaining = timeout - (perf_counter() - startTime)
                if remaining > 0:
                    event.listener.armTimer(remaining)
                else:
                    ontimeout(event.listener)

        KernelEventsManager().on(
            KernelEvent.MemberJoinedParty, onNewMember, timeout=timeout, ontimeout=ontimeout, originator=originator
        )
