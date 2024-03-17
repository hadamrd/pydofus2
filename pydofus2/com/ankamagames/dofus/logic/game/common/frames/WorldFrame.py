from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.roleplay.AnomalySubareaInformationRequestAction import \
    AnomalySubareaInformationRequestAction
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameRefreshMonsterBoostsMessage import \
    GameRefreshMonsterBoostsMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.AnomalySubareaInformationRequestMessage import \
    AnomalySubareaInformationRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.AnomalySubareaInformationResponseMessage import \
    AnomalySubareaInformationResponseMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.modificator.AreaFightModificatorUpdateMessage import \
    AreaFightModificatorUpdateMessage
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterBoosts import \
    MonsterBoosts
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class WorldFrame(Frame):

    _settings: list = None

    _currentFightModificator: int = -1

    _monsterBoosts: list[MonsterBoosts]

    _raceBoosts: list[MonsterBoosts]

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def settings(self) -> list:
        return self._settings

    def pushed(self) -> bool:
        return True

    def pulled(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, AreaFightModificatorUpdateMessage):
            afmumsg = msg
            if self._currentFightModificator != afmumsg.spellPairId:
                self._currentFightModificator = afmumsg.spellPairId
            return True

        elif isinstance(msg, GameRefreshMonsterBoostsMessage):
            grmbmsg = msg
            self._monsterBoosts = grmbmsg.monsterBoosts
            self._raceBoosts = grmbmsg.familyBoosts
            return True

        elif isinstance(msg, AnomalySubareaInformationRequestAction):
            sireqmsg = AnomalySubareaInformationRequestMessage()
            ConnectionsHandler().send(sireqmsg)
            return True

        elif isinstance(msg, AnomalySubareaInformationResponseMessage):
            return True

        return False

    def getMonsterXpBoostMultiplier(self, pMonsterId: int) -> float:
        boost: MonsterBoosts = self.getMonsterBoost(pMonsterId)
        return (boost.xpBoost / 100 if not boost else 1) * self.getRaceXpBoostMultiplier(
            Monster.getMonsterById(pMonsterId).race
        )

    def getMonsterDropBoostMultiplier(self, pMonsterId: int) -> float:
        boost: MonsterBoosts = self.getMonsterBoost(pMonsterId)
        return (boost.dropBoost / 100 if not boost else 1) * self.getRaceDropBoostMultiplier(
            Monster.getMonsterById(pMonsterId).race
        )

    def getRaceXpBoostMultiplier(self, pRaceId: int) -> float:
        boost: MonsterBoosts = self.getRaceBoost(pRaceId)
        return float(boost.xpBoost / 100) if not boost else float(1)

    def getRaceDropBoostMultiplier(self, pRaceId: int) -> float:
        boost: MonsterBoosts = self.getRaceBoost(pRaceId)
        return float(boost.dropBoost / 100) if not boost else float(1)

    def getMonsterBoost(self, pId: int) -> MonsterBoosts:
        boost: MonsterBoosts = None
        for boost in self._monsterBoosts:
            if boost.id == pId:
                return boost
        return None

    def getRaceBoost(self, pRaceId: int) -> MonsterBoosts:
        boost: MonsterBoosts = None
        for boost in self._raceBoosts:
            if boost.id == pRaceId:
                return boost
        return None
