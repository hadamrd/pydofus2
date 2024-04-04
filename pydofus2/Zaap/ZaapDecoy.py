import atexit
import json
import os
from datetime import datetime
import threading
from urllib import request

import psutil
import pytz
import requests
import yaml

from pydofus2.Zaap.models import StoredApikey, StoredCertificate
from pydofus2.com.ankamagames.dofus.misc.stats.InternalStatisticEnum import \
    InternalStatisticTypeEnum
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.ThreadSharedSingleton import \
    ThreadSharedSingleton
from pydofus2.Zaap.helpers.CryptoHelper import CryptoHelper
from pydofus2.Zaap.helpers.Device import Device
from pydofus2.Zaap.Zaapi import Zaapi


class ZaapError(Exception):
    pass


class ZaapDecoy(metaclass=ThreadSharedSingleton):
    GPU = "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.2206)"
    RAM = 32768
    VERSION = None
    SETTINGS = None
    ANKAMA_LAUNCHER_PROCESS_NAME = "Ankama Launcher.exe"
    CONNECTED_ACCOUNTS = 0
    SESSIONS_LAUNCH = 0
    INITIALIZED = threading.Event()

    def __init__(self, mainAccountApiKey: str = ""):
        self.kill_ankama_launcher()
        self.zaapi = Zaapi(zaap_version=self.version)
        self._apikeys = self.get_apikeys()
        self._certs = self.get_certificates()
        self.load_settings()
        if not mainAccountApiKey:
            mainAccountApiKey = self.find_main_account_apikey()
        self.mainAccountApiKey = mainAccountApiKey
        self.zaapi.zaap_apikey = mainAccountApiKey
        self.active_accounts = 0
        for account in self.SETTINGS["USER_ACCOUNTS"]:
            if account["active"]:
                self.active_accounts += 1
        self.mainAccount = self.fetch_account_data(mainAccountApiKey)
        self.zaapi.listWithApiKey(self.mainAccountApiKey)
        self.zaapi.getAccountStatus(self.mainAccountApiKey)
        self.zaap_sessionId = self.zaapi.startSessionWithApiKey(self.mainAccount["id"], apikey=self.mainAccountApiKey)
        atexit.register(
            self.send_exit_events,
            self.mainAccountApiKey,
            self.mainAccount["id"],
            self.zaap_sessionId,
        )
        Logger().info(f"Zaap Session started with id {self.zaap_sessionId}")
        self.zaapi.getFromCms("NEWS", "LAUNCHEREVENTS", self.SETTINGS["LANGUAGE"], 1, 1)
        self.zaapi.getFromCms("BLOG", "LAUNCHEREVENTS", self.SETTINGS["LANGUAGE"], 1, 1)
        self.zaapi.getLegalsTou(GameID.DOFUS, self.SETTINGS["LANGUAGE"], 11)
        self.zaapi.sendDeviceInfos(
            session_id=self.mainAccount["id"],
            connection_type="ANKAMA",
            client_type="STANDALONE",
            os="WINDOWS",
            device="PC",
            partner="",
            device_uid=self.SETTINGS["DEVICE_UID"],
            apikey=self.mainAccountApiKey,
        )
        if "ANNOUNCEMENTS" in self.SETTINGS:
            self.zaapi.getCmsById("LAUNCHEREVENTS", self.SETTINGS["LANGUAGE"], self.SETTINGS["ANNOUNCEMENTS"])
        self.zaapi.getFromCms("CHANGELOG", "LAUNCHER", "en", 1, 20)
        self._chatApiKey = self.zaapi.createToken(GameID.CHAT, apikey=self.mainAccountApiKey)
        self.zaapi.getCarouselForLauncher("DOFUS", self.SETTINGS["LANGUAGE"], 1, 1)
        self.zaapi.getFromCms("NEWS", "ZAAP_PAGE_DOFUS", self.SETTINGS["LANGUAGE"], 1, 15)
        self.zaapi.getFromCms("BLOG", "ZAAP_PAGE_DOFUS", self.SETTINGS["LANGUAGE"], 1, 15)
        self.zaapi.getFromCms("NEWS", "LAUNCHER", self.SETTINGS["LANGUAGE"], 1, 15)
        self.zaapi.getFromCms("BLOG", "LAUNCHER", self.SETTINGS["LANGUAGE"], 1, 15)
        self.INITIALIZED.set()
        Logger().info("ZAAP DECOY INITIALIZED")

    @classmethod
    def load_settings(cls):
        settings_file_path = os.path.join(cls.getZaapPath(), "Settings")
        if not os.path.exists(settings_file_path):
            raise ZaapError(f"Settings file not found at path {settings_file_path}")
        with open(settings_file_path, "r") as file:
            cls.SETTINGS = json.load(fp=file)
        
    def kill_dofus_processes(self):
        for process in psutil.process_iter(["name"]):
            if "Dofus" in process.info["name"]:
                pid = process.pid
                try:
                    process.kill()
                    Logger().debug(f"Process Dofus.exe (PID: {pid}) has been killed.")
                except psutil.NoSuchProcess:
                    Logger().debug(f"Process Dofus.exe (PID: {pid}) does not exist.")
                except psutil.AccessDenied:
                    Logger().debug(f"Process Dofus.exe (PID: {pid}) could not be killed due to access denial.")

    def kill_ankama_launcher(self):
        self.kill_dofus_processes()
        process_found = False

        for process in psutil.process_iter(["name"]):
            if process.info["name"] == self.ANKAMA_LAUNCHER_PROCESS_NAME:
                process_found = True
                pid = process.pid
                Logger().warning(
                    f"Found a running Launcher process {process.info['name']} while trying to run the zaapDecoy launcher, will try to close it"
                )
                try:
                    process.kill()
                    Logger().debug(f"Process {self.ANKAMA_LAUNCHER_PROCESS_NAME} (PID: {pid}) has been killed.")
                except psutil.NoSuchProcess:
                    Logger().debug(f"Process {self.ANKAMA_LAUNCHER_PROCESS_NAME} (PID: {pid}) does not exist.")
                except psutil.AccessDenied:
                    Logger().debug(
                        f"Process {self.ANKAMA_LAUNCHER_PROCESS_NAME} (PID: {pid}) could not be killed due to access denial."
                    )
                    raise SystemError(
                        f"Failed to kill process {self.ANKAMA_LAUNCHER_PROCESS_NAME} (PID: {pid}) due to access denial."
                    )
                except Exception as e:
                    Logger().debug(f"Error killing process {self.ANKAMA_LAUNCHER_PROCESS_NAME} (PID: {pid}): {e}")
                    raise SystemError(f"Failed to kill process {self.ANKAMA_LAUNCHER_PROCESS_NAME} (PID: {pid}): {e}")

        if not process_found:
            Logger().debug(f"Process {self.ANKAMA_LAUNCHER_PROCESS_NAME} was not found running.")

    def fetch_account_data(self, apikey):
        account_data = self.zaapi.signOnWithApikey(GameID.ZAAP, apikey)
        return account_data

    def find_main_account_apikey(self):
        for account in self.SETTINGS["USER_ACCOUNTS"]:
            if account["isMain"]:
                Logger().info(f"Main account found: {account['login']}")
                accountLogin = account["login"]
                for api in self._apikeys:
                    if api.login == accountLogin:
                        Logger().info(f"Main account apikey found")
                        return api.key
        raise ZaapError("No main account apikey found on local disk")

    def send_exit_events(self, apiKey, accountId, sessionId):
        Logger().debug("ZAAP ATEXIT CALLED :: sending zaap exit events")
        self.zaapi.endSessionWithApiKey(sessionId, apikey=apiKey)
        events = self.getCloseEvents(accountId)
        self.zaapi.sendEvents(game=GameID.ZAAP, sessionId=sessionId, events=events)
        self.INITIALIZED.clear()

    @property
    def version(self):
        if self.VERSION is None:
            self.VERSION = self.fetch_version()
        return self.VERSION

    @classmethod
    def fetch_version(cls) -> str:
        url = "https://launcher.cdn.ankama.com/installers/production/latest.yml?noCache=1hkaeforb"
        response = requests.get(
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
        except yaml.YAMLError:
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
                "main_account_id": self.mainAccount["id"],
                "account_id": accountId,
                "launch_game": GameID.DOFUS,
                "launch_session": self.SESSIONS_LAUNCH,
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
                "os_arch_is64": self.SETTINGS["OS_ARCHITECTURE"] == "x64",
                "cpu": [cpu_count, cpu_model, 3600],
                "gpu": [self.GPU],
                "ram": self.RAM,
                "gpu_directx": 0,
                "screens": [[1920, 1080, 1, 0, 0], [1920, 1080, 1, 0, 0]],
                "resolution": [1920, 1032],
                "maximized": False,
                "zoom": 1,
                "pic_quality": self.SETTINGS.get("PRESELECT_PERFORMANCE", "lp"),
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
                "account_id": self.mainAccount["id"],
                "main_account_id": accountId,
                "total_accounts_connected": self.CONNECTED_ACCOUNTS,
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
                "last_route": self.SETTINGS["LAST_ROUTE"],
                "auto_launch": self.SETTINGS["AUTO_LAUNCH"],
                "auto_connect": self.SETTINGS["AUTO_LAUNCH"],
                "lang": self.SETTINGS["LANGUAGE"],
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
        timezone = pytz.timezone("UTC")
        now = datetime.now(timezone)
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
        formatted_date = formatted_date[:-2] + ":" + formatted_date[-2:]
        return formatted_date

    def getLoginToken(self, game, certid=0, certhash="", apikey=None, login=None):
        if apikey is None:
            if login is None:
                raise ZaapError("No apikey or login provided")
            for api in self._apikeys:
                if api.login == login:
                    apikey = api.key
                    break
        if apikey is None:
            raise ZaapError(f"No apikey found for login {login}")
        for cert in self._certs:
            if cert.login == login:
                certid = cert.id
                certhash = cert.hash
                break
        return self.zaapi.createToken(game, certid, certhash, apikey)

    @classmethod
    def getZaapPath(cls):
        return os.path.join(os.environ["APPDATA"], "zaap")

    @classmethod
    def get_certificate_folder_path(cls):
        return os.path.join(cls.getZaapPath(), "certificate")

    @classmethod
    def get_apikey_folder_path(cls):
        return os.path.join(cls.getZaapPath(), "keydata")

    @classmethod
    def get_certificates(cls, cert_folder=None) -> list[StoredCertificate]:
        if not cert_folder:
            cert_folder = cls.get_certificate_folder_path()
        cert_files = os.listdir(cert_folder)
        deciphered_certs = []
        encoders = CryptoHelper.create_hm_encoder()
        for cert_file in cert_files:
            if not cert_file.startswith(".certif"):
                continue
            cert_path = os.path.join(cert_folder, cert_file)
            Logger().debug(f"Extracting certificate data from file {cert_path}")
            cert_dict = CryptoHelper.decrypt_from_file(cert_path)
            cert: StoredCertificate = StoredCertificate.from_dict(cert_dict)
            Logger().debug(f"Found certificate data for login {cert.login} with id {cert.id}")
            cert.hash = CryptoHelper.generate_hash_from_cert(cert.encodedCertificate, encoders["hm1"], encoders["hm2"])
            deciphered_certs.append(cert)
        cls._certs = deciphered_certs
        return deciphered_certs

    @classmethod
    def get_apikeys(cls, apikeys_folder=None) -> list[StoredApikey]:
        if not apikeys_folder:
            apikeys_folder = cls.get_apikey_folder_path()
        apikeys_files = os.listdir(apikeys_folder)
        deciphered_apikeys = list[StoredApikey]()
        for apikey_filename in apikeys_files:
            if not apikey_filename.startswith(".keydata"):
                continue
            apikey_file_path = os.path.join(apikeys_folder, apikey_filename)
            Logger().debug(f"Extracting apikey data from file {apikey_file_path} ...")
            apikey_dict = CryptoHelper.decrypt_from_file(apikey_file_path)
            apikey_data: StoredApikey = StoredApikey.from_dict(apikey_dict)
            Logger().debug(f"Found Apikey data : {apikey_data.key} for account {apikey_data.accountId}")
            deciphered_apikeys.append(apikey_data)
        cls._apikeys = deciphered_apikeys
        return deciphered_apikeys

    @classmethod
    def get_username_hash(cls, username, length=32) -> str:
        hash = CryptoHelper.string_hash(username, algo="sha256")
        return hash[:length]
    
    @classmethod
    def get_certficate_filepath(cls, username) -> str:
        if not username:
            raise ZaapError("No username provided")
        certFolder = cls.get_certificate_folder_path()
        user_name_hash = cls.get_username_hash(username)
        cert_path = os.path.join(certFolder, f".certif{user_name_hash}")
        if not os.path.exists(cert_path):
            raise ZaapError(f"Certificate file for user {username} not found")
        return cert_path
    
    @classmethod
    def get_apikey_filepath(cls, username) -> str:
        if not username:
            raise ZaapError("No username provided")
        apikeys_folder = cls.get_apikey_folder_path()
        user_name_hash = cls.get_username_hash(username)
        apikey_file_path = os.path.join(apikeys_folder, f".keydata{user_name_hash}")
        if not os.path.exists(apikey_file_path):
            raise ZaapError(f"Apikey file for user {username} not found")
        return apikey_file_path
        
    @classmethod
    def get_stored_certificate(cls, username) -> StoredCertificate:
        cert_path = cls.get_certficate_filepath(username)
        cert_dict = CryptoHelper.decrypt_from_file(cert_path)
        cert: StoredCertificate = StoredCertificate.from_dict(cert_dict)
        encoders = CryptoHelper.create_hm_encoder()
        cert.hash = CryptoHelper.generate_hash_from_cert(cert.encodedCertificate, encoders["hm1"], encoders["hm2"])
        return cert

    @classmethod
    def get_stored_apikey(cls, accountId) -> StoredApikey:
        apikey_file_path = cls.get_apikey_filepath(accountId)
        apikey_dict = CryptoHelper.decrypt_from_file(str(apikey_file_path))
        apikey_data = StoredApikey.from_dict(apikey_dict)
        return apikey_data
    
    @classmethod
    def get_api_cert(cls, apikey: StoredApikey) -> StoredCertificate:
        for cert in cls._certs:
            if cert.login == apikey.login:
                return cert
        return None

    @classmethod
    def get_dofus_location(cls):
        zaap_path = cls.getZaapPath()
        dofus_release_config_path = os.path.join(zaap_path, "repositories", "production", "dofus", "main", "release.json")
        with open(dofus_release_config_path, "r") as file:
            dofus_release_config = json.load(file)
        return dofus_release_config["location"]
        

if __name__ == "__main__":
    print(ZaapDecoy.get_certificates())
    print(ZaapDecoy.get_apikeys())
    print(ZaapDecoy.get_dofus_location())