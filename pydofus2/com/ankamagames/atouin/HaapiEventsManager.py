import json
from datetime import datetime

import pytz

from pydofus2.com.ankamagames.atouin.Haapi import Haapi
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.misc.stats.InternalStatisticEnum import \
    InternalStatisticTypeEnum
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiEvent import HaapiEvent
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import \
    HaapiKeyManager
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class HaapiEventsManager(metaclass=Singleton):
    DMG_PREV = True
    FORCE_CPU = False
    SCREEN_SIZE = 17
    QUALITY = 0

    def __init__(self):
        self.used_shortcuts = {}

    @staticmethod
    def get_date():
        timezone = pytz.timezone('UTC')
        now = datetime.now(timezone)
        # Correctly format the date with microseconds limited to three digits and a correctly formatted timezone
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
        formatted_date = formatted_date[:-2] + ":" + formatted_date[-2:]
        return formatted_date

    def sendStartEvent(self, sessionId):
        Haapi().sendEvent(
            game=GameID.DOFUS,
            session_id=sessionId,
            event_id=InternalStatisticTypeEnum.START_SESSION,
            data={"account_id": PlayerManager().accountId, "client_open": 1},
        )

    def getDofusCloseEvent(self, num_client=1):
        return {
            "event_id": InternalStatisticTypeEnum.END_SESSION,
            "data": {
                "screen_size": self.SCREEN_SIZE,
                "account_id": PlayerManager().accountId,
                "damage_preview": self.DMG_PREV,
                "client_open": num_client,
                "force_cpu": self.FORCE_CPU,
                "quality": self.QUALITY,
            },
            "date": self.get_date(),
        }
    
    def sendEndEvent(self, num_client=1):
        if not self.used_shortcuts:
            Haapi().sendEvent(
                game=GameID.DOFUS,
                session_id=Haapi().game_sessionId,
                **self.getDofusCloseEvent(num_client)
            )
        else:
            events = [ 
                self.getDofusCloseEvent(num_client),
                self.getShortCutsUsedEvent()
            ]
            Haapi().sendEvents(GameID.DOFUS, Haapi().game_sessionId, events)

    def registerShortcutUse(self, shortcut_id):
        if shortcut_id not in self.used_shortcuts:
            self.used_shortcuts[shortcut_id] = {"ratio": 0, "use": 0}
        self.used_shortcuts[shortcut_id]["use"] += 1
    
    def getShortCutsUsedEvent(self):
        return {
            "event_id": InternalStatisticTypeEnum.USE_SHORTCUT,
            "data": {
                "keyboard": "frFR",
                "character_level": PlayedCharacterManager().infos.level,
                "account_id": PlayerManager().accountId,
                "shortcuts_list": self.used_shortcuts,
                "character_id": int(PlayedCharacterManager().extractedServerCharacterIdFromInterserverCharacterId)
            },
            "date": self.get_date()
        }
    def getButtonEventData(self, button_id, button_name):
        return {
            "character_level": PlayedCharacterManager().infos.level,
            "button_id": button_id,
            "button_name": button_name,
            "server_id": PlayerManager().server.id,
            "character_id": int(PlayedCharacterManager().extractedServerCharacterIdFromInterserverCharacterId),
            "account_id": PlayerManager().accountId,
        }

    def sendCharacteristicsOpenEvent(self):
        data = self.getButtonEventData(1, "Characteristics")
        self.sendBannerEvent(data)

    def sendInventoryOpenEvent(self):
        data = self.getButtonEventData(3, "Inventory")
        self.sendBannerEvent(data)

    def sendQuestsOpenEvent(self):
        data = self.getButtonEventData(4, "Quests")
        self.sendBannerEvent(data)
    
    def sendMapOpenEvent(self):
        data = self.getButtonEventData(5, "Map")
        self.sendBannerEvent(data)

    def sendSocialOpenEvent(self):
        data = self.getButtonEventData(6, "Social")
        self.sendBannerEvent(data)

    def sendProfessionsOpenEvent(self):
        data = self.getButtonEventData(9, "Professions")
        self.sendBannerEvent(data)
        
    def sendBannerEvent(self, data):
        if not Haapi().game_sessionId:
            return HaapiKeyManager().once(HaapiEvent.GameSessionReadyEvent, lambda event, sessionId: self.sendBannerEvent(data), originator=self)
        Haapi().sendEvent(GameID.DOFUS, Haapi().game_sessionId, InternalStatisticTypeEnum.BANNER, data)