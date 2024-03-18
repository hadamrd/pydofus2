import atexit
import json
import os
from datetime import datetime

import cloudscraper
import pytz
import yaml

from pydofus2.Zaap.Zaapi import Zaapi
from pydofus2.com.ankamagames.dofus.misc.stats.InternalStatisticEnum import \
    InternalStatisticTypeEnum
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.ThreadSharedSingleton import \
    ThreadSharedSingleton
from pydofus2.Zaap.helpers.Device import Device
from pydofus2.Zaap.helpers.CryptoHelper import CryptoHelper

class ZaapError(Exception):
    pass

class ZaapDecoy(metaclass=ThreadSharedSingleton):
    GPU = "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.2206)"
    RAM = 32768
    VERSION = None
    
    
    def __init__(self, mainAccountApiKey: str=None):
        self.haapi = Zaapi(self.version)
        appdata_path = os.getenv("APPDATA")
        settings_file_path = os.path.join(appdata_path, "zaap", "Settings")
        self._apikeys = CryptoHelper.get_all_stored_apikeys()
        self._certs = CryptoHelper.get_all_stored_certificates()
        with open(settings_file_path, "r") as file:
            self.settings = json.load(file)
        if mainAccountApiKey is None:
            mainAccountApiKey = self.find_main_account_apikey()
        self.mainAccountApiKey = mainAccountApiKey
        self.haapi.zaap_apikey = mainAccountApiKey
        self.connected_accounts = 1
        self.active_accounts = 0
        for account in self.settings["USER_ACCOUNTS"]:
            if account["active"]:
                self.active_accounts += 1
        self.mainAccount = self.haapi.signOnWithApikey(GameID.ZAAP, self.mainAccountApiKey)
        self.haapi.listWithApiKey(self.mainAccountApiKey)
        self.haapi.getAccountStatus(self.mainAccountApiKey)
        self.zaap_sessionId = self.haapi.startSessionWithApiKey(self.mainAccount['id'])
        atexit.register(self.send_exit_events, self.mainAccountApiKey, self.mainAccount['id'], self.zaap_sessionId)
        Logger().info(f"Session started with id {self.zaap_sessionId}")
        self.haapi.getFromCms("NEWS", "LAUNCHEREVENTS", self.settings["LANGUAGE"], 1, 1)
        self.haapi.getFromCms("BLOG", "LAUNCHEREVENTS", self.settings["LANGUAGE"], 1, 1)
        self.haapi.getLegalsTou(GameID.DOFUS, self.settings["LANGUAGE"], 11)
        self.haapi.sendDeviceInfos(
            session_id=self.mainAccount['id'],
            connection_type="ANKAMA",
            client_type="STANDALONE",
            os="WINDOWS",
            device="PC",
            partner="",
            device_uid=self.settings["DEVICE_UID"],
            apikey=self.mainAccountApiKey,
        )
        self.haapi.getCmsById("LAUNCHEREVENTS", self.settings["LANGUAGE"], self.settings["ANNOUNCEMENTS"])
        self.haapi.getFromCms("CHANGELOG", "LAUNCHER", "en", 1, 20)
        self._chatApiKey = self.haapi.createToken(GameID.CHAT, apikey=self.mainAccountApiKey)
        self.haapi.getCarouselForLauncher("DOFUS", self.settings["LANGUAGE"], 1, 1)
        self.haapi.getFromCms("NEWS", "ZAAP_PAGE_DOFUS", self.settings["LANGUAGE"], 1, 15)
        self.haapi.getFromCms("BLOG", "ZAAP_PAGE_DOFUS", self.settings["LANGUAGE"], 1, 15)
        self.haapi.getFromCms("NEWS", "LAUNCHER", self.settings["LANGUAGE"], 1, 15)
        self.haapi.getFromCms("BLOG", "LAUNCHER", self.settings["LANGUAGE"], 1, 15)

    def find_main_account_apikey(self):
        for account in self.settings["USER_ACCOUNTS"]:
            if account["isMain"]:
                Logger().info(f"Main account found: {account['login']}")
                accountLogin = account["login"]
                for api in self._apikeys:
                    if api["apikey"]["login"] == accountLogin:
                        Logger().info(f"Main account apikey found")
                        return api["apikey"]["key"]
        raise ZaapError("No main account apikey found on local disk")
    
    def send_exit_events(self, apiKey, accountId, sessionId):
        Logger().debug("ATEXIT CALLED :: sending zaap exit events")
        events = self.getCloseEvents(accountId)
        self.haapi.sendEvents(game=GameID.ZAAP, sessionId=sessionId, events=events)
        self.haapi.endSessionWithApiKey(sessionId, apikey=apiKey)

    @property
    def version(self):
        if self.VERSION is None:
            self.VERSION = self.fetch_version()
        return self.VERSION

    @classmethod
    def fetch_version(cls) -> str:
        url = "https://launcher.cdn.ankama.com/installers/production/latest.yml?noCache=1hkaeforb"
        # Make an HTTP request to get the YAML file
        client = cloudscraper.create_scraper()
        response = client.get(
            url,
            headers={
                "user-Agent": "electron-builder",
                "cache-control": "no-cache",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-dest": "empty",
                "accept-encoding": "identity",
                "accept-language": "en-US",
            },
        )

        if response.status_code != 200:
            raise ZaapError("Failed to download ZAAP version file")

        # Parse the YAML content
        try:
            data = yaml.safe_load(response.content)
        except yaml.YAMLError as e:
            raise ZaapError("Failed to parse Zaap version YAML file")

        # Save the file locally
        local_folder = os.path.dirname(os.path.abspath(__file__))
        local_file_path = os.path.join(local_folder, "latest.yml")
        with open(local_file_path, "wb") as file:
            file.write(response.content)

        # Extract the version
        version = data.get("version")
        if not version:
            raise ZaapError("Failed to extract ZAAP version from YAML file")

        return version

    def get_dofus_laucnh_event(self, accountId):
        return {
            "event_id": 662,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "main_account_id": self.mainAccount['id'],
                "account_id": accountId,
                "launch_game": 1,
                "launch_session": 1,
            },
        }

    def get_device_data(self, accountId):
        cpu_count, cpu_model = Device.get_cpu_info()
        return {
            "event_id": InternalStatisticTypeEnum.KOLIZEUM,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "account_id": accountId,
                "machine_id": Device.machine_id(),
                "os": 0,
                "os_version": 10,
                "os_arch_is64": self.settings["OS_ARCHITECTURE"] == "x64",
                "cpu": [cpu_count, cpu_model, 3600],
                "gpu": [self.GPU],
                "ram": self.RAM,
                "gpu_directx": 0,
                "screens": [[1920, 1080, 1, 0, 0], [1920, 1080, 1, 0, 0]],
                "resolution": [1920, 1032],
                "maximized": False,
                "zoom": 1,
                "pic_quality": self.settings["PRESELECT_PERFORMANCE"],
                "anim_desac": True,
                "video_desac": True,
                "webtoon_auto_unlock": False,
                "zaap_version": self.version,
                "theme": "krosmoz",
            },
        }

    def get_num_connected_event(self, accountId):
        return {
            "event_id": 711,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "account_id": self.mainAccount['id'],
                "main_account_id": accountId,
                "total_accounts_connected": self.connected_accounts,
                "active_accounts": self.active_accounts,
            },
        }

    def get_krozmos_launch_event(self, accountId):
        return {
            "event_id": 659,
            "date": self.get_date(),
            "data": {
                "device": "DESKTOP",
                "app_name": "ZAAP",
                "universe": "KROSMOZ",
                "account_id": accountId,
                "last_route": self.settings["LAST_ROUTE"],
                "auto_launch": self.settings["AUTO_LAUNCH"],
                "auto_connect": self.settings["AUTO_LAUNCH"],
                "lang": self.settings["LANGUAGE"],
                "games_install": '{"1":{"AU":true},"22":{"AU":true}}',
                "connection_type": "ankama",
            },
        }

    def getCloseEvents(self, accountId):
        return [
            self.get_krozmos_launch_event(accountId),
            self.get_dofus_laucnh_event(accountId),
            self.get_device_data(accountId),
            self.get_num_connected_event(accountId),
        ]

    @staticmethod
    def get_date():
        timezone = pytz.timezone('UTC')
        now = datetime.now(timezone)
        # Correctly format the date with microseconds limited to three digits and a correctly formatted timezone
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
        formatted_date = formatted_date[:-2] + ":" + formatted_date[-2:]
        return formatted_date
    
    def getLoginToken(self, game, certid="", certhash="", apikey=None, login=None):
        if apikey is None:
            if login is None:
                raise ZaapError("No apikey or login provided")
            for api in self._apikeys:
                if api["apikey"]["login"] == login:
                    apikey = api["apikey"]["key"]
                    break
        if apikey is None:
            raise ZaapError(f"No apikey found for login {login}")
        if not certid or not certhash:
            if not login:
                raise ZaapError("No login provided to find certificate")
            for cert in self._certs:
                if cert["cert"]["login"] == login:
                    certid = cert["cert"]["id"]
                    certhash = cert["hash"]
                    break
        if not certid or not certhash:
            raise ZaapError(f"No certificate found for login {login}")
        return self.haapi.createToken(game, certid, certhash, apikey)

if __name__ == "__main__":
    Logger().activateConsolLogging()
    zaap = ZaapDecoy()
    print(zaap.getLoginToken(GameID.DOFUS, login="m72044942@gmail.com"))
    