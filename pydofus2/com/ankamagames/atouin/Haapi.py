import json
import os
import ssl
from datetime import datetime
from time import sleep
from urllib.parse import urlencode

import cloudscraper
import pytz
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pydofus2.com.ankamagames.atouin.HappiConfig import (AUTH_STATES,
                                                         ZAAP_CONFIG)
from pydofus2.com.ankamagames.dofus.BuildInfos import BuildInfos
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class HaapiException(Exception):
    pass

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Haapi(metaclass=Singleton):
    MAX_CREATE_API_KEY_RETRIES = 5

    def __init__(self):
        self.BASE_URL = f"https://{XmlConfig().getEntry('config.haapiUrlAnkama')}"
        self.zaap_session = requests.Session()
        self.dofus_session = requests.Session()
        self._curr_account = None
        self._session_id = None
        self._api_key = None
        self.zaap_headers = {
            "if-none-match": "null",
            "user-Agent": f"Zaap {self.getZaapVersion()}",
            "accept": "*/*",
            "accept-encoding": "gzip,deflate",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-dest": "empty",
            "accept-language": "en-US",
        }
        self.dofus_headers = {
            "Referer": "app:/DofusInvoker.swf",
            "Host": "haapi.ankama.com",
            "x-flash-version": "31,1,1,889",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": f"Dofus Client {BuildInfos().VERSION}",
            "Accept": "text/xml, application/xml, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8, text/css, image/png, image/jpeg, image/gif;q=0.8, application/x-shockwave-flash, video/mp4;q=0.9, flv-application/octet-stream;q=0.8, video/x-flv;q=0.7, audio/mp4, application/futuresplash, */*;q=0.5, application/x-mpegURL",
            "Accept-Encoding": "gzip,deflate",
            "Connection": "keep-alive",
            "Cookie": "LANG=en",
        }
        self.zaap_session.headers.update(self.zaap_headers)
        self.dofus_session.headers.update(self.dofus_headers)
        self.dofus_session.proxies.update(
            {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080",
            }
        )
        self.zaap_session.proxies.update(
            {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080",
            }
        )
        self.verify_ssl = False

    def getUrl(self, request, params={}):
        result = (
            self.BASE_URL
            + {
                "CREATE_API_KEY": "/Ankama/v4/Api/CreateApiKey",
                "GET_LOGIN_TOKEN": "/Ankama/v5/Account/CreateToken",
                "SIGN_ON_WITH_APIKEY": "/Ankama/v5/Account/SignOnWithApiKey",
                "SET_NICKNAME": "/Ankama/v5/Account/SetNicknameWithApiKey",
                "START_SESSION_WITH_API_KEY": "/Ankama/v5/Game/StartSessionWithApiKey",
                "LIST_WITH_API_KEY": "/Ankama/v5/Game/ListWithApiKey",
                "SEND_MAIL_VALIDATION": "/Ankama/v5/Account/SendMailValidation",
                "SECURITY_CODE": "/Ankama/v5/Shield/SecurityCode",
                "VALIDATE_CODE": "/Ankama/v5/Shield/ValidateCode",
                "DELETE_API_KEY": "/Ankama/v5/Api/DeleteApiKey",
                "CREATE_GUEST": "/Ankama/v2/Account/CreateGuest",
                "CREATE_TOKEN_WITH_PASSWORD": "/Ankama/v4/Account/CreateTokenWithPassword",
                "CREATE_TOKEN": "/Ankama/v4/Account/CreateToken",
                "GET_ACCESS_TOKEN": "/Ankama/v4/Account/GetAccessToken",
                "SEND_EVENTS": "/Ankama/v5/Game/SendEvents",
                "SEND_EVENT": "/Ankama/v5/Game/SendEvent",
                "SEND_EVENT_V4": "/Ankama/v4/Game/SendEvent",
                "END_SESSION_WITH_API_KEY": "/Ankama/v5/Game/EndSessionWithApiKey",
                "ANKAMA_ACCOUNT_STATUS": "/Ankama/v5/Account/Status",
                "GET_FROM_CMS": "/Ankama/v5/Cms/Items/Get",
                "GET_FROM_CMS_BYID": "/Ankama/v5/Cms/Items/GetById",
                "GET_LEGALS_TOU": "/Ankama/v5/Legals/Tou",
                "SEND_DEVICE_INFOS": "/Ankama/v5/Account/SendDeviceInfos",
                "CAROUSEL_FORLAUNCHER": "/Ankama/v5/Cms/Items/Carousel/GetForLauncher",
                "GET_ALMANAX_EVENT": "/Ankama/v4/Almanax/GetEvent",
                "GET_LOADING_SCREEN": "/Ankama/v4/Cms/Items/Loadingscreen/Get",
                "GET_CMS_FEEDS": "/Ankama/v4/Cms/Items/GetFeeds",
            }[request]
        )
        if params:
            result += "?" + urlencode(params)
        return result

    def getCmsFeeds(self, site, page, lang, count, apikey=None):
        if not apikey:
            apikey = self.api_key
        url = self.getUrl(
            "GET_CMS_FEEDS",
            {
                "site": site,
                "lang": lang,
                "page": page,
                "count": count,
            },
        )
        response = self.dofus_session.get(url, headers={"apikey": self.api_key}, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        return response.json()

    def getLoadingScreen(self, page, accountId, lang, count):
        url = self.getUrl("GET_LOADING_SCREEN", {"page": page, "accountId": accountId, "lang": lang, "count": count})
        response = self.dofus_session.get(url, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        return response.json()

    def getAlmanaxEvent(self, lang):
        url = self.getUrl("GET_ALMANAX_EVENT", {"lang": lang, "date": self.get_date()})
        response = self.dofus_session.get(url, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        return response.json()

    def sendDeviceInfos(self, session_id, connection_type, client_type, os, device, partner, device_uid, apikey=None):
        if not apikey:
            apikey = self.api_key
        if not session_id:
            session_id = self._session_id
            if not session_id:
                raise Exception("Need a session_id to send events")
        url = self.getUrl("SEND_DEVICE_INFOS")
        response = self.zaap_session.post(
            url,
            data={
                "session_id": session_id,
                "connection_type": connection_type,
                "client_type": client_type,
                "os": os,
                "device": device,
                "partner": partner,
                "device_uid": device_uid,
            },
            headers={"apikey": apikey},
            verify=self.verify_ssl,
        )
        # check if the response is ok
        if not response.ok:
            raise Exception(f"Error while sending device infos: {response.text}")

    def getCarouselForLauncher(self, site, lang, page, count):
        url = self.getUrl(
            "CAROUSEL_FORLAUNCHER",
            {
                "site": site,
                "lang": lang,
                "page": page,
                "count": count,
            },
        )
        response = self.zaap_session.get(url, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        return response.json()

    def getLegalsTou(self, game, lang, knowVersion):
        url = self.getUrl("GET_LEGALS_TOU", {"game": game, "lang": lang, "knowVersion": knowVersion})
        response = self.zaap_session.get(url, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)

    def getCmsById(self, site, lang, id):
        url = self.getUrl("GET_FROM_CMS_BYID", {"site": site, "lang": lang, "id": id})
        response = self.zaap_session.get(url, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        return response.json()

    def getFromCms(self, template_key, site, lang, page, count):
        url = self.getUrl(
            "GET_FROM_CMS",
            {
                "template_key": template_key,
                "site": site,
                "lang": lang,
                "page": page,
                "count": count,
            },
        )
        response = self.zaap_session.get(url, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        return response.json()

    def sendEvents(self, game: int, session_id: int, events: str):
        if not session_id:
            session_id = self._session_id
            if not session_id:
                raise Exception("Need a session_id to send events")
        url = self.getUrl("SEND_EVENTS")
        response = self.dofus_session.post(
            url, data={"game": game, "session_id": session_id, "events": json.dumps(events)},
            verify=self.verify_ssl
        )
        self.dofus_session.cookies.update(response.cookies)
        if not response.ok:
            raise Exception(f"Error while sending events: {response.text}")
        return response

    def sendEvent(self, game: int, session_id: int, event_id: int, data: str, date=None):
        if not session_id:
            session_id = self._session_id
            if not session_id:
                raise Exception("Need a session_id to send events")
        if not date:
            date = self.get_date()
        url = self.getUrl("SEND_EVENT_V4")
        response = self.dofus_session.post(
            url,
            data={
                "game": game,
                "session_id": session_id,
                "event_id": event_id,
                "data": json.dumps(data),
                "date": date,
            },
            verify=self.verify_ssl,
        )
        self.dofus_session.cookies.update(response.cookies)
        if not response.ok:
            raise Exception(f"Error while sending event: {response.text}")
        return response

    @property
    def api_key(self):
        if not self._api_key:
            raise HaapiException("No API key set")
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key

    def signOnWithApikey(self, game_id, apikey=None):
        if not apikey:
            apikey = self.api_key
        url = self.getUrl("SIGN_ON_WITH_APIKEY", {"game": game_id})
        response = self.zaap_session.post(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        body = response.json()
        print(body)
        if body["account"]["locked"] == ZAAP_CONFIG.USER_ACCOUNT_LOCKED.MAILNOVALID:
            Logger().error("[AUTH] Mail not confirmed by user")
            raise Exception(AUTH_STATES.USER_EMAIL_INVALID)
        self.zaap_session.cookies.update(response.cookies)
        self._curr_account = {
            "id": body["id"],
            "id_string": str(body["id_string"]),
            "account": self.parseAccount(body["account"]),
        }
        return self._curr_account

    def listWithApiKey(self, apikey=None):
        if not apikey:
            apikey = self.api_key
        url = self.getUrl("LIST_WITH_API_KEY")
        response = self.zaap_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        body = response.json()
        self.zaap_session.cookies.update(response.cookies)
        with open(f"{apikey}_tracking.json", "w") as f:
            f.write(response.text)

    def getAccountStatus(self, apikey=None):
        if not apikey:
            apikey = self.api_key
        url = self.getUrl("ANKAMA_ACCOUNT_STATUS")
        response = self.zaap_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        print(response.text)
        self.zaap_session.cookies.update(response.cookies)

    @staticmethod
    def get_date():
        timezone = pytz.timezone("UTC")
        now = datetime.now(timezone)
        # Correctly format the date with microseconds limited to three digits and a correctly formatted timezone
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
        formatted_date = formatted_date[:-2] + ":" + formatted_date[-2:]
        return formatted_date

    def startSessionWithApiKey(self, session_id, server_id="", character_id="", date="", apikey=None):
        if not apikey:
            apikey = self.api_key
        url = self.getUrl(
            "START_SESSION_WITH_API_KEY",
            {
                "session_id": session_id,
                "server_id": server_id,
                "character_id": character_id,
                "date": date,
            },
        )
        response = self.zaap_session.get(url, headers={"apikey": self.api_key}, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        self._session_id = response.json()
        return response.json()

    def endSessionWithApiKey(self, session_id, subscriber="", close_account_session=True, apikey=None):
        if not apikey:
            apikey = self.api_key
        url = self.getUrl(
            "END_SESSION_WITH_API_KEY",
            {
                "session_id": session_id,
                "subscriber": subscriber,
                "close_account_session": close_account_session,
            },
        )
        response = self.zaap_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        return response.text

    @classmethod
    def parseAccount(cls, body):
        return {
            "id": body["id"],
            "type": body["type"],
            "login": body["login"],
            "nickname": body["nickname"],
            "firstname": body["firstname"],
            "lastname": body["lastname"],
            "nicknameWithTag": f"{body['nickname']}#{body['tag']}",
            "tag": body["tag"],
            "security": body["security"],
            "addedDate": body["added_date"],
            "locked": body["locked"],
            "parentEmailStatus": body["parent_email_status"],
            "avatar": body["avatar_url"],
        }

    @classmethod
    def getZaapVersion(cls):
        import yaml

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
            raise Exception("Failed to download ZAAP version file")

        # Parse the YAML content
        try:
            data = yaml.safe_load(response.content)
        except yaml.YAMLError as e:
            raise Exception("Failed to parse Zaap version YAML file")

        # Save the file locally
        local_folder = os.path.dirname(os.path.abspath(__file__))
        local_file_path = os.path.join(local_folder, "latest.yml")
        with open(local_file_path, "wb") as file:
            file.write(response.content)

        # Extract the version
        version = data.get("version")
        if not version:
            raise Exception("Failed to extract ZAAP version from YAML file")

        return version

    def getLoginToken(self, game_id, certId="", certHash="", from_dofus=False, api_key=None):
        if api_key is None:
            api_key = self.api_key
        nbrtries = 0
        while nbrtries < 5:
            try:
                url = self.getUrl(
                    "GET_LOGIN_TOKEN",
                    {
                        "game": game_id,
                        "certificate_id": certId,
                        "certificate_hash": certHash,
                    },
                )
                Logger().debug("[HAAPI] Calling HAAPI to get Login Token, url: %s" % url)
                if from_dofus:
                    response = self.dofus_session.get(url, headers={"apikey": api_key}, verify=self.verify_ssl)
                else:
                    response = self.zaap_session.get(url, headers={"apikey": api_key}, verify=self.verify_ssl)
                if response.headers["content-type"] == "application/json":
                    token = response.json().get("token")
                    if token:
                        Logger().debug("[HAAPI] Login Token created")
                        return token
                    elif response.json().get("reason") == "Certificate control failed.":
                        Logger().error("Invalid certificate, please check your certificate")
                        return None
                    elif (
                        response.json().get("reason")
                        == f"Invalid security parameters. certificate_id : {certId}, certificate_hash: {certHash}"
                    ):
                        Logger().error("Invalid security parameters, please check your certificate")
                        return None
                    else:
                        Logger().error("Error while calling HAAPI to get Login Token : %s" % response.json())
                        return None
                else:
                    from lxml import html

                    root = html.fromstring(response.content.decode("UTF-8"))
                    error = root.xpath('//div[@id="what-happened-section"]//p/@text')
                    if error:
                        Logger().debug("Login Token creation failed, reason: %s" % error)
                    elif (
                        "The owner of this website (haapi.ankama.com) has banned you temporarily from accessing this website."
                        in response.text
                    ):
                        Logger().debug(
                            "Login Token creation failed, reason: haapi.ankama.com has banned you temporarily from accessing this website."
                        )
                    elif "Access denied | haapi.ankama.com used Cloudflare to restrict access" in response.text:
                        Logger().debug(
                            "Login Token creation failed, reason: haapi.ankama.com used Cloudflare to restrict access"
                        )
                    Logger().info("Login Token creation failed, retrying in 10 minutes")
                    sleep(60 * 10 + 3)
            except ssl.SSLError:
                Logger().debug("[HAAPI] SSL error while calling HAAPI to get Login Token")
                sleep(10)
            except ConnectionError:
                Logger().error("No internet connection will try again in some seconds")
                sleep(30)
            except Exception:
                Logger().error("No internet connection will try again in some seconds")
                sleep(30)
