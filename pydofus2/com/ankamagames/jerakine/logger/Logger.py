import datetime
import logging
import os
import sys
import threading
from pathlib import Path

from pydofus2.com.ankamagames.dofus import Constants

LOGS_PATH = Path(Constants.LOGS_DIR)
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

CYAN_COLOR = '\033[0;36m'
YELLOW_COLOR = '\033[0;33m'
RED_COLOR = '\033[0;31m'
MAGNETA_COLOR = '\033[0;35m'
GREEN_COLOR = '\033[0;32m'
ORANGE_COLOR = '\033[38;5;208m'
DARK_GRAY_COLOR = '\033[90m'

COLORS = {
    "ServerConnection": CYAN_COLOR,
    "ConnectionsHandler": CYAN_COLOR,
    "DisconnectionHandlerFrame": CYAN_COLOR,
    "HandshakeFrame": CYAN_COLOR,
    "QueueFrame": DARK_GRAY_COLOR,
    "RoleplayEntitiesFrame": GREEN_COLOR,
    "RoleplayMovementFrame": GREEN_COLOR,
    "MapMove": GREEN_COLOR,
    "AttackMonsters": MAGNETA_COLOR,
    "RoleplayContextFrame": GREEN_COLOR,
    "ChangeMap": GREEN_COLOR,
    "BotFightFrame": MAGNETA_COLOR,
    "BotMuleFightFrame": MAGNETA_COLOR,
    "FightSequenceFrame": MAGNETA_COLOR,
    "FightTurnFrame": MAGNETA_COLOR,
    "FightContextFrame": MAGNETA_COLOR,
    "FarmPath": GREEN_COLOR,
    "BotPartyFrame": GREEN_COLOR,
    "PlayedCharacterUpdatesFrame": MAGNETA_COLOR,
    "AbstractFarmBehavior": MAGNETA_COLOR,
    "Kernel": ORANGE_COLOR,
    "Haapi": ORANGE_COLOR,
    "WorldGraph": ORANGE_COLOR,
    "I18nFileAccessor": ORANGE_COLOR,
    "FeatureManager": ORANGE_COLOR,
    "DofusClient": ORANGE_COLOR,
    "ChatFrame": YELLOW_COLOR,
    "AbstractEntitiesFrame": GREEN_COLOR,
    "AutoTrip": GREEN_COLOR,
    "BotWorkflowFrame": DARK_GRAY_COLOR,
    "AbstractBehavior": GREEN_COLOR,
    "RoleplayInteractivesFrame": GREEN_COLOR,
    "WaitForPartyMembersToShow": ORANGE_COLOR,
    "SynchronisationFrame": DARK_GRAY_COLOR,
    "Singleton": DARK_GRAY_COLOR,
    "RequestMapData": GREEN_COLOR,
    "GiveItems": MAGNETA_COLOR,
    "UnloadInBank": GREEN_COLOR,
    "NetworkMessageClassDefinition": GREEN_COLOR,
    "NetworkMessageDataField": MAGNETA_COLOR
}
class MyFormatter(logging.Formatter):
    
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)
        self.max_module_length = max(len(module) for module in COLORS)
        self.max_level_length = max(len(levelname) for levelname in logging._nameToLevel)
        self.module_format = 12
        self.levelname_format = 6

    def format(self, record):
        if record.levelno == logging.ERROR:
            color = RED_COLOR
        elif record.levelno == logging.WARNING:
            color = YELLOW_COLOR
        elif "Step" in record.module:
            color = DARK_GRAY_COLOR
        else:
            color = COLORS.get(record.module, '')
        record.module = f"{record.module[:self.module_format]:{self.module_format}}"
        record.levelname = f"{record.levelname[:self.levelname_format]:{self.levelname_format}}"
        return f"{color}{super().format(record)}\033[0m"

class Logger(logging.Logger, metaclass=LoggerSingleton):
    logToConsole = False
    
    def __init__(self, name="DofusLogger", consoleOut=False):
        self.name = name
        self.prefix = threading.current_thread().name
        super().__init__(self.prefix)
        self.setLevel(logging.DEBUG)
        self.formatter = MyFormatter(
            "%(asctime)s.%(msecs)03d | %(levelname)s | [%(module)s] %(message)s", datefmt="%H:%M:%S"
        )
        now = datetime.datetime.now()
        self.outputFile = LOGS_PATH / f"{self.prefix}_{now.strftime('%Y-%m-%d')}.log"
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
        formatter = MyFormatter("%(asctime)s.%(msecs)03d | %(levelname)s | [%(module)s] %(message)s", datefmt="%H:%M:%S")
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
