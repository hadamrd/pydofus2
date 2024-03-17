from datetime import datetime

import pytz
from ankalauncher.pythonversion.Device import Device

from pydofus2.com.ankamagames.atouin.Haapi import Haapi
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.misc.stats.InternalStatisticEnum import \
    InternalStatisticTypeEnum
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class HaapiEventsManager(metaclass=Singleton):
    SCREEN_SIZE = 17
    GPU = "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.2206)"
    RAM = 32768
    DMG_PREV = True
    FORCE_CPU = False
    QUALITY = 0
    
    def __init__(self):
        self._events = {}

    @staticmethod
    def get_date():
        timezone = pytz.timezone('UTC')
        now = datetime.now(timezone)
        # Correctly format the date with microseconds limited to three digits and a correctly formatted timezone
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
        formatted_date = formatted_date[:-2] + ":" + formatted_date[-2:]
        return formatted_date

    def get_krozmos_launch_event(self, lang="en"):
        return {
            "event_id": 659,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "account_id": PlayerManager().accountId,
                "last_route": "/Krosmoz/games/game/dofus/main",
                "auto_launch": False,
                "auto_connect": True,
                "lang": "en",
                "games_install": '{"1":{"AU":true},"22":{"AU":true}}',
                "connection_type": "ankama",
            },
        }

    def get_dofus_laucnh_event(self):
        return {
            "event_id": 662,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "main_account_id": PlayerManager().accountId,
                "account_id": PlayerManager().accountId,
                "launch_game": 1,
                "launch_session": 1,
            },
        }

    def get_device_data(self):
        cpu_count, cpu_model = Device.get_cpu_info()
        return {
            "event_id": InternalStatisticTypeEnum.KOLIZEUM,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "account_id": PlayerManager().accountId,
                "machine_id": Device.machine_id(),
                "os": 0,
                "os_version": 10,
                "os_arch_is64": True,
                "cpu": [cpu_count, cpu_model, 3600],
                "gpu": [self.GPU],
                "ram": self.RAM,
                "gpu_directx": 0,
                "screens": [[1920, 1080, 1, 0, 0], [1920, 1080, 1, 0, 0]],
                "resolution": [1920, 1032],
                "maximized": False,
                "zoom": 1,
                "pic_quality": "lq",
                "anim_desac": True,
                "video_desac": True,
                "webtoon_auto_unlock": False,
                "zaap_version": Haapi().getZaapVersion(),
                "theme": "krosmoz",
            },
        }

    def get_num_connected_event(self, connected_accounts=1, active_accounts=1):
        return {
            "event_id": 711,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "account_id": PlayerManager().accountId,
                "main_account_id": PlayerManager().accountId,
                "total_accounts_connected": connected_accounts,
                "active_accounts": active_accounts,
            },
        }

    def sendStartEvent(self):
        Haapi().sendEvent(
            game=GameID.DOFUS,
            session_id=Haapi()._session_id,
            event_id=InternalStatisticTypeEnum.START_SESSION,
            data={"account_id": PlayerManager().accountId, "client_open": 1},
        )

    def sendEndEvent(self, num_client=1):
        Haapi().sendEvent(
            game=GameID.DOFUS,
            session_id=Haapi()._session_id,
            event_id=InternalStatisticTypeEnum.END_SESSION,
            data={
                "screen_size": self.SCREEN_SIZE,
                "account_id": PlayerManager().accountId,
                "damage_preview": self.DMG_PREV,
                "client_open": num_client,
                "force_cpu": self.FORCE_CPU,
                "quality": self.QUALITY,
            },
        )
    
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
        Haapi().sendEvent(GameID.DOFUS, Haapi()._session_id, InternalStatisticTypeEnum.BANNER, data)

    def sendInventoryOpenEvent(self):
        data = self.getButtonEventData(3, "Inventory")
        Haapi().sendEvent(GameID.DOFUS, Haapi()._session_id, InternalStatisticTypeEnum.BANNER, data)

    def sendQuestsOpenEvent(self):
        data = self.getButtonEventData(4, "Quests")
        Haapi().sendEvent(GameID.DOFUS, Haapi()._session_id, InternalStatisticTypeEnum.BANNER, data)
    
    def sendMapOpenEvent(self):
        data = self.getButtonEventData(5, "Map")
        Haapi().sendEvent(GameID.DOFUS, Haapi()._session_id, InternalStatisticTypeEnum.BANNER, data)

    def sendSocialOpenEvent(self):
        data = self.getButtonEventData(6, "Social")
        Haapi().sendEvent(GameID.DOFUS, Haapi()._session_id, InternalStatisticTypeEnum.BANNER, data)

    def sendEndEvents(self):
        events = [
            self.get_krozmos_launch_event(),
            self.get_dofus_laucnh_event(),
            self.get_device_data(),
            self.get_num_connected_event(),
        ]
        Haapi().sendEvents(game=GameID.ZAAP, session_id=Haapi()._session_id, events=events)
