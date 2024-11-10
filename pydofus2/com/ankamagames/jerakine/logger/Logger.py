import datetime
import logging
import os
import sys
import threading
from pathlib import Path

from pydofus2.com.ankamagames.dofus import settings

LOGS_PATH = Path(settings.LOGS_DIR)
if not os.path.isdir(LOGS_PATH):
    os.makedirs(LOGS_PATH)

from typing import Type, TypeVar

T = TypeVar("T")


class LoggerSingleton(type):
    _instances = dict[str, object]()

    def __call__(cls: Type[T], *args, **kwargs) -> T:
        threadName = threading.current_thread().name
        if threadName not in LoggerSingleton._instances:
            LoggerSingleton._instances[threadName] = super(LoggerSingleton, cls).__call__(*args, **kwargs)
        return LoggerSingleton._instances[threadName]

    def clear(cls):
        del LoggerSingleton._instances[threading.current_thread().name]

    def getInstance(cls: Type[T], thname: int) -> T:
        return LoggerSingleton._instances.get(thname)


CYAN_COLOR = "\033[0;36m"
YELLOW_COLOR = "\033[0;33m"
RED_COLOR = "\033[0;31m"
MAGENTA_COLOR = "\033[0;35m"
GREEN_COLOR = "\033[0;32m"
ORANGE_COLOR = "\033[38;5;208m"
DARK_GRAY_COLOR = "\033[90m"

ansi_to_color_style = {
    CYAN_COLOR: "color: #2aa198;",  # Solarized Cyan
    YELLOW_COLOR: "color: #b58900;",  # Solarized Yellow
    RED_COLOR: "color: #dc322f;",  # Solarized Red
    MAGENTA_COLOR: "color: #d33682;",  # Solarized Magenta
    GREEN_COLOR: "color: #859900;",  # Solarized Green
    ORANGE_COLOR: "color: #cb4b16;",  # Solarized Orange
    DARK_GRAY_COLOR: "color: #586e75;",  # Solarized Base01
}

# Updated color constants with modern terminal colors
COLORS = {
    # System & Connection
    "ServerConnection": "#7aa2f7",  # Bright Blue
    "ConnectionsHandler": "#7aa2f7",
    "DisconnectionHandlerFrame": "#7aa2f7",
    "HandshakeFrame": "#7aa2f7",
    # Queue & Synchronization
    "QueueFrame": "#a9b1d6",  # Light Gray
    "SynchronisationFrame": "#a9b1d6",
    "Singleton": "#a9b1d6",
    # Roleplay & Movement
    "RoleplayEntitiesFrame": "#9ece6a",  # Bright Green
    "RoleplayMovementFrame": "#9ece6a",
    "MapMove": "#9ece6a",
    "RoleplayContextFrame": "#9ece6a",
    "ChangeMap": "#9ece6a",
    # Combat
    "AttackMonsters": "#f7768e",  # Bright Pink
    "BotFightFrame": "#f7768e",
    "BotMuleFightFrame": "#f7768e",
    "FightSequenceFrame": "#f7768e",
    "FightTurnFrame": "#f7768e",
    "FightContextFrame": "#f7768e",
    # Farming & Party
    "FarmPath": "#ff9e64",  # Bright Orange
    "BotPartyFrame": "#ff9e64",
    "AbstractFarmBehavior": "#ff9e64",
    # System Core
    "Kernel": "#bb9af7",  # Bright Purple
    "Haapi": "#bb9af7",
    "WorldGraph": "#bb9af7",
    "I18nFileAccessor": "#bb9af7",
    "FeatureManager": "#bb9af7",
    "DofusClient": "#bb9af7",
    # Chat & Interaction
    "ChatFrame": "#7dcfff",  # Bright Cyan
    "AbstractEntitiesFrame": "#7dcfff",
    "RoleplayInteractivesFrame": "#7dcfff",
    # Default fallback color
    "default": "#c0caf5",  # Visible Light Gray
}

# Update the severity level colors to be more visible
ERROR_COLOR = "#f7768e"  # Bright Red
WARNING_COLOR = "#e0af68"  # Bright Yellow
INFO_COLOR = "#c0caf5"  # Light Gray
DEBUG_COLOR = "#a9b1d6"  # Visible Gray


def getRecordColor(record: logging.LogRecord, type="html") -> str:
    if record.levelno == logging.ERROR:
        color = ERROR_COLOR
    elif record.levelno == logging.WARNING:
        color = WARNING_COLOR
    elif "Step" in record.module:
        color = DEBUG_COLOR
    else:
        color = COLORS.get(record.module, COLORS["default"])

    if type == "html":
        return f"color: {color};"
    return color


class AnsiFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)
        self.max_module_length = max(len(module) for module in COLORS)
        self.max_level_length = max(len(levelname) for levelname in logging._nameToLevel)
        self.module_format = 12
        self.levelname_format = 6

    def format(self, record):
        color = getRecordColor(record)
        formatted_module = f"{record.module[:self.module_format]:{self.module_format}}"
        formatted_levelname = f"{record.levelname[:self.levelname_format]:{self.levelname_format}}"

        original_format = self._fmt
        try:
            self._fmt = self._fmt.replace("%(module)s", formatted_module).replace("%(levelname)s", formatted_levelname)
            formatted_message = super().format(record)
        finally:
            self._fmt = original_format

        return f"{color}{formatted_message}\033[0m"


class HtmlFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)
        self.max_module_length = max(len(module) for module in COLORS)
        self.max_level_length = max(len(levelname) for levelname in logging._nameToLevel)
        self.module_format = 12
        self.levelname_format = 6

    def format(self, record):
        color_style = getRecordColor(record, "html")
        record.module = f"{record.module[:self.module_format]:{self.module_format}}"
        record.levelname = f"{record.levelname[:self.levelname_format]:{self.levelname_format}}"
        formatted_message = super().format(record)
        formatted_message = formatted_message.replace("\n", "<br>")
        # Add specific styling to ensure visibility on dark background
        timestamp_style = "color: #565f89;"  # Subtle gray for timestamp
        module_style = "color: #7aa2f7;"  # Blue for module name
        level_style = getRecordColor(record, "html")  # Color based on level

        # Format each part with appropriate color
        parts = formatted_message.split(" | ")
        if len(parts) == 3:
            timestamp, level, message = parts
            styled_msg = (
                f'<span style="{timestamp_style}">{timestamp}</span> | '
                f'<span style="{level_style}">{level}</span> | '
                f'<span style="{color_style}">{message}</span>'
            )
        else:
            styled_msg = f'<span style="{color_style}">{formatted_message}</span>'

        return f'<pre class="log-line">{styled_msg}</pre>'


class Logger(logging.Logger, metaclass=LoggerSingleton):
    logToConsole = False

    def __init__(self, name="DofusLogger", consoleOut=False):
        self.name = name
        self.prefix = threading.current_thread().name
        super().__init__(self.prefix)
        self.setLevel(logging.DEBUG)
        self.formatter = AnsiFormatter(
            "%(asctime)s.%(msecs)03d | %(levelname)s | [%(module)s] %(message)s", datefmt="%H:%M:%S"
        )
        now = datetime.datetime.now()
        self.outputFile = str(LOGS_PATH / f"{self.prefix}_{now.strftime('%Y-%m-%d')}.log")
        if not os.path.exists(LOGS_PATH):
            os.makedirs(LOGS_PATH)
        fileHandler = logging.FileHandler(self.outputFile)
        fileHandler.setFormatter(self.formatter)
        self.addHandler(fileHandler)
        if Logger.logToConsole:
            streamHandler = logging.StreamHandler(sys.stdout)
            streamHandler.setFormatter(self.formatter)
            self.addHandler(streamHandler)

    def activateConsolLogging(self):
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(self.formatter)
        self.addHandler(streamHandler)

    def separator(self, msg, separator="="):
        format_row = "\n{:<50} {:^30} {:>70}\n"
        text = format_row.format(separator * 50, msg, separator * 70)
        self.info(text)


class TraceLoggerSingleton(type):
    _instances = dict[str, object]()

    def __call__(cls, *args, **kwargs) -> object:
        threadName = threading.current_thread().name
        if threadName not in TraceLoggerSingleton._instances:
            TraceLoggerSingleton._instances[threadName] = super(TraceLoggerSingleton, cls).__call__(*args, **kwargs)
        return TraceLoggerSingleton._instances[threadName]

    def clear(cls):
        del TraceLoggerSingleton._instances[threading.current_thread().name]

    def getInstance(cls: Type[T], thname: int) -> T:
        return TraceLoggerSingleton._instances.get(thname)


class TraceLogger(logging.Logger, metaclass=TraceLoggerSingleton):
    def __init__(self, name="TraceLogger", consoleOut=False):
        self.name = name
        self.prefix = "TraceLogger_" + threading.current_thread().name
        super().__init__(self.prefix)
        self.setLevel(logging.DEBUG)
        formatter = AnsiFormatter(
            "%(asctime)s.%(msecs)03d | %(levelname)s | [%(module)s] %(message)s", datefmt="%H:%M:%S"
        )
        now = datetime.datetime.now()
        fileHandler = logging.FileHandler(LOGS_PATH / f"{self.prefix}_{now.strftime('%Y-%m-%d')}.log")
        fileHandler.setFormatter(formatter)
        self.addHandler(fileHandler)
        if consoleOut:
            streamHandler = logging.StreamHandler(sys.stdout)
            streamHandler.setFormatter(formatter)
            self.addHandler(streamHandler)

    def separator(self, msg, separator="="):
        format_row = "\n{:<50} {:^30} {:>70}\n"
        text = format_row.format(separator * 50, msg, separator * 70)
        self.info(text)
