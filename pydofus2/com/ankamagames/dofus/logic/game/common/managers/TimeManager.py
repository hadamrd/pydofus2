import time
from datetime import datetime, timedelta, timezone

from pydofus2.com.ankamagames.dofus.network.messages.game.basic.BasicTimeMessage import BasicTimeMessage
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton


class TimeManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.server_time_lag_ms: int = 0
        self.server_utc_lag_ms: int = 0
        self.timezone_offset_ms: int = 0
        self.dofus_time_year_lag: int = 0

    def format_date_irl(self, timestamp_ms: int, use_timezone_offset: bool = False, unchanged: bool = False) -> str:
        """
        Format timestamp to real-world date (DD/MM/YYYY)

        Args:
            timestamp_ms: Server timestamp in milliseconds
            use_timezone_offset: Whether to apply timezone offset
            unchanged: If True, don't apply server lag compensation
        """
        if unchanged and timestamp_ms > 0:
            timestamp_ms -= self.server_time_lag_ms

        dt = self._get_datetime_from_timestamp(timestamp_ms, use_timezone_offset)
        return dt.strftime("%d/%m/%Y")

    def _get_datetime_from_timestamp(self, timestamp_ms: int, use_timezone_offset: bool = False) -> datetime:
        """Convert millisecond timestamp to datetime with proper timezone handling"""
        base_dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)

        if use_timezone_offset:
            return base_dt + timedelta(milliseconds=self.timezone_offset_ms)
        return base_dt

    def format_clock(self, timestamp: int, showSeconds: bool = False, useTimezoneOffset: bool = False) -> str:
        """
        Format timestamp to clock time (HH:mm or HH:mm:ss)
        Args:
            timestamp: Server timestamp in seconds
            showSeconds: Whether to include seconds
            useTimezoneOffset: Whether to apply server timezone offset
        """
        dt = self.server_timestamp_to_datetime(timestamp)
        if useTimezoneOffset:
            dt = dt + timedelta(milliseconds=self.timezone_offset_ms)

        format_str = "%H:%M:%S" if showSeconds else "%H:%M"
        return dt.strftime(format_str)

    def server_timestamp_to_datetime(self, timestamp: int) -> datetime:
        """
        Convert server timestamp to datetime with lag compensation

        Args:
            timestamp: Server timestamp in seconds
        """
        return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

    def getUtcTimestamp(self):
        return time.time() * 1000 + self.server_utc_lag_ms

    def getTimestamp(self):
        return time.time() * 1000 + self.server_time_lag_ms

    def getFormatterDateFromTime(
        self, timeUTC: int, useTimezoneOffset: bool = False, format: str = "DD/MM/YYYY HH:mm"
    ) -> str:
        [nminute, nhour, nday, nmonth, nyear] = self.getDateFromTime(timeUTC, useTimezoneOffset)
        format = format.replace("DD", str(nday).zfill(2))
        format = format.replace("MM", str(nmonth).zfill(2))
        format = format.replace("YYYY", str(nyear))
        format = format.replace("HH", str(nhour).zfill(2))
        format = format.replace("mm", str(nminute).zfill(2))
        return format

    def getDateFromTime(self, timestamp_ms: int = 0, use_timezone_offset: bool = False) -> list:
        """
        Get date components from timestamp

        Args:
            timestamp_ms: Server timestamp in milliseconds (uses current time if None)
            use_timezone_offset: Whether to apply timezone offset

        Returns:
            List of [minute, hour, day, month, year]
        """
        if timestamp_ms is None:
            dt = datetime.now() + timedelta(milliseconds=self.server_time_lag_ms)
        else:
            dt = self._get_datetime_from_timestamp(timestamp_ms, use_timezone_offset)

        return [dt.minute, dt.hour, dt.day, dt.month, dt.year]

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

    def get_date_ig(self, timestamp_ms: int):
        """
        Get in-game date components

        Args:
            timestamp_ms: Server timestamp in milliseconds

        Returns:
            Tuple of (day, month_name, year)
        """
        date_components = self.getDateFromTime(timestamp_ms)
        game_year = date_components[4] + self.dofus_time_year_lag
        # Note: You'll need to implement Month.get_month_by_id() to get month names
        month_name = f"Month{date_components[3]}"  # Placeholder
        return (date_components[2], month_name, game_year)

    def sync_with_server(self, msg: "BasicTimeMessage") -> None:
        """
        Synchronize time manager with server time from BasicTimeMessage

        Args:
            msg: BasicTimeMessage containing server timestamp and timezone
        """
        # Convert current time to milliseconds (like AS3's getTime())
        current_time_ms = int(time.time() * 1000)

        # Convert reception delay to milliseconds
        reception_delay_ms = int((time.perf_counter() - msg.receptionTime) * 1000)

        # Set time lags (in milliseconds)
        self.server_time_lag_ms = (
            msg.timestamp
            + msg.timezoneOffset * 60 * 1000  # Server time
            - current_time_ms  # Convert minutes to milliseconds
            + reception_delay_ms  # Local time  # Network delay compensation
        )

        # UTC lag doesn't include timezone offset
        self.server_utc_lag_ms = msg.timestamp - current_time_ms + reception_delay_ms

        # Store timezone offset in milliseconds
        self.timezone_offset_ms = msg.timezoneOffset * 60 * 1000
