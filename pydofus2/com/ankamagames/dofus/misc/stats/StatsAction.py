import hashlib
import json
from datetime import datetime
from time import perf_counter

from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import AuthentificationManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import TimeManager
from pydofus2.com.ankamagames.dofus.misc.stats.StatisticsManager import StatisticsManager
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import HaapiKeyManager
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class StatsAction:
    _usersActions = {}

    def __init__(self, pId, pPersistent=False, pAggregate=False, pAddTimestamp=False, pSendOnExit=False):
        self._id = pId
        self._persistent = pPersistent
        self._aggregate = pAggregate
        self._addTimestamp = pAddTimestamp
        self._sendOnExit = pSendOnExit
        self._params = {}
        self._date = None
        self._userId = None
        self._gameSessionId = None
        self._started = False
        self._timestamp = None
        self._startTime = None

    @staticmethod
    def getUserId():
        login = AuthentificationManager().username
        if login:
            return "user-" + hashlib.md5(login.encode()).hexdigest()
        return None

    @classmethod
    def get(cls, pStatsActionId, pPersistent=False, pAggregate=False, pAddTimestamp=False, pSendOnExit=False):
        userId = StatsAction.getUserId()
        if pStatsActionId not in StatsAction._usersActions:
            sa = StatsAction(pStatsActionId, pPersistent, pAggregate, pAddTimestamp, pSendOnExit)
            sa._userId = userId
            sa._gameSessionId = HaapiKeyManager().getGameSessionId()
            cls._usersActions[pStatsActionId] = sa
        return cls._usersActions[pStatsActionId]

    @staticmethod
    def fromString(pString):
        try:
            obj = json.loads(pString)
            sa = StatsAction(obj["event_id"])
            if "user" in obj:
                sa._userId = obj["user"]
            if "gameSessionId" in obj:
                sa._gameSessionId = obj["gameSessionId"]
            for param in obj["data"]:
                sa.setParam(param, obj["data"][param])
            sa.date = datetime.strptime(obj["date"], "%Y-%m-%dT%H:%M:%S")  # TODO: Check if this is the correct format
            return sa
        except Exception as e:
            Logger().warning("Invalid event data from cache : " + pString)
            return None

    @classmethod
    def exists(cls, pStatsActionId):
        return pStatsActionId in cls._usersActions

    @classmethod
    def reset(cls):
        cls._usersActions = {}

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._userId

    @user.setter
    def user(self, pUser):
        self._userId = pUser

    @property
    def params(self):
        return self._params

    @property
    def paramsString(self):
        return json.dumps(self._params)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, pDate):
        self._date = pDate

    @property
    def sendOnExit(self):
        return self._sendOnExit

    @sendOnExit.setter
    def sendOnExit(self, pSendOnExit):
        self._sendOnExit = pSendOnExit

    @property
    def gameSessionId(self):
        return self._gameSessionId

    @gameSessionId.setter
    def gameSessionId(self, pGameSessionId):
        self._gameSessionId = pGameSessionId

    def start(self):
        if not self._started and self._addTimestamp:
            if not self._persistent:
                self._timestamp = TimeManager().getTimestamp()
                self._startTime = perf_counter()
            else:
                ts = StatisticsManager().getActionTimestamp(self._id)
                if ts is None:
                    ts = TimeManager().getTimestamp()
                    StatisticsManager().saveActionTimestamp(self._id, ts)
                self._timestamp = ts
        self._started = True

    def restart(self):
        self._started = False
        self.start()

    def cancel(self):
        self._usersActions.pop(self._id, None)

    def updateTimestamp(self):
        self._timestamp = TimeManager().getTimestamp()
        if self._persistent:
            StatisticsManager().saveActionTimestamp(self._id, self._timestamp)

    def addParam(self, pKey, pType):
        # Implement the logic for adding a parameter with type if necessary
        raise NotImplementedError()

    def hasParam(self, pKey):
        return pKey in self._params

    def setParam(self, pKey, pValue):
        self._params[pKey] = pValue

    def send(self):
        self._date = datetime.now()
        if self._addTimestamp:
            action_duration_seconds = int(
                (TimeManager().getTimestamp() - self._timestamp) / 1000
                if self._persistent
                else (perf_counter() - self._startTime) / 1000
            )
            self._params["action_duration_seconds"] = action_duration_seconds
            if self._persistent:
                StatisticsManager().deleteTimeStamp(self._id)
        StatisticsManager().sendAction(self)
        if self._id in StatsAction._usersActions:
            del StatsAction._usersActions[self._id]

    def toString(self, backup=False):
        obj = {"event_id": self._id, "data": self.paramsString()}

        if backup:
            obj["user"] = self._userId
            obj["gameSessionId"] = self._gameSessionId

        if self._date is not None:
            formatted_date = StatisticsManager().formatDate(self._date)
            obj["date"] = formatted_date

        return json.dumps(obj)
