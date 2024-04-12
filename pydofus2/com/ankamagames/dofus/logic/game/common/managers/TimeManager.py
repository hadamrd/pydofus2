import time
from datetime import datetime, timedelta, timezone

from pydofus2.com.ankamagames.dofus.datacenter.misc.Month import Month
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class TimeManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.serverTimeLag: int = 0
        self.serverUtcTimeLag: int = 0
        self.timezoneOffset: int = 0
        self.dofusTimeYearLag: int = 0

    def getUtcTimestamp(self):
        dt = datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        return utc_timestamp

    def getTimestamp(self):
        current_time = time.time() * 1000  # Convert to milliseconds
        return current_time + self.serverTimeLag

    def getFormatterDateFromTime(self, timeUTC: int, useTimezoneOffset: bool = False, format: str = "DD/MM/YYYY HH:mm") -> str:
        [nminute, nhour, nday, nmonth, nyear] = self.getDateFromTime(timeUTC, useTimezoneOffset)
        format = format.replace("DD", str(nday).zfill(2))
        format = format.replace("MM", str(nmonth).zfill(2))
        format = format.replace("YYYY", str(nyear))
        format = format.replace("HH", str(nhour).zfill(2))
        format = format.replace("mm", str(nminute).zfill(2))
        return format
    
    def getDateFromTime(self, timeUTC: int, useTimezoneOffset: bool = False) -> list:
        date: datetime = None
        nday = nmonth = nyear = nhour = nminute = None
        if timeUTC == 0:
            date = datetime.now() + timedelta(seconds=self.serverTimeLag / 1000)
        else:
            date = datetime.fromtimestamp(timeUTC / 1000) + timedelta(seconds=self.serverTimeLag / 1000)
        if useTimezoneOffset:
            nday = date.day
            nmonth = date.month
            nyear = date.year
            nhour = date.hour
            nminute = date.minute
        else:
            nday = date.now(timezone.utc).day
            nmonth = date.now(timezone.utc).month
            nyear = date.now(timezone.utc).year
            nhour = date.now(timezone.utc).hour
            nminute = date.now(timezone.utc).minute
        return [nminute, nhour, nday, nmonth, nyear]

    def initText(self):
        self._nameYears = I18n.getUiText("ui.time.years")
        self._nameMonths = I18n.getUiText("ui.time.months")
        self._nameDays = I18n.getUiText("ui.time.days")
        self._nameHours = I18n.getUiText("ui.time.hours")
        self._nameMinutes = I18n.getUiText("ui.time.minutes")
        self._nameSeconds = I18n.getUiText("ui.time.seconds")
        self._nameYearsShort = I18n.getUiText("ui.time.short.year")
        self._nameMonthsShort = I18n.getUiText("ui.time.short.month")
        self._nameDaysShort = I18n.getUiText("ui.time.short.day")
        self._nameHoursShort = I18n.getUiText("ui.time.short.hour")
        self._nameAnd = I18n.getUiText("ui.common.and").lower()
        self._bTextInit = True

    def getDateIG(self, time: int):
        date = self.getDateFromTime(time)
        nyear = date[4] + self.dofusTimeYearLag
        month = Month.getMonthById(date[3] - 1).name
        return [date[2], month, nyear]
