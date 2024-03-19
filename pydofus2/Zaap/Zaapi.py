import json
import ssl
from datetime import datetime
from time import sleep
from urllib.parse import urlencode

import pytz
import requests
from urllib3.exceptions import InsecureRequestWarning

from pydofus2.com.ankamagames.atouin.HappiConfig import (AUTH_STATES,
                                                         ZAAP_CONFIG)
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class HaapiException(Exception):
    pass

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Zaapi(metaclass=Singleton):
    MAX_CREATE_API_KEY_RETRIES = 5

    def __init__(self, zaap_version: str):
        Logger().debug(f"Zaap version: {zaap_version}")
        self.BASE_URL = f"https://{XmlConfig().getEntry('config.haapiUrlAnkama')}"
        self.zaap_session = requests.Session()
        self._curr_account = None
        self.session_id = None
        self._zaap_apikey = None
        self.zaap_headers = {
            "if-none-match": "null",
            "user-Agent": f"Zaap {zaap_version}",
            "accept": "*/*",
            "accept-encoding": "gzip,deflate",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-dest": "empty",
            "accept-language": "en-US",
        }
        self.zaap_session.headers.update(self.zaap_headers)
        self.zaap_session.proxies.update(
            {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080",
            }
        )
        self.verify_ssl = False

    def getUrl(self, request, params={}):
        queries = {
                "SIGN_ON_WITH_APIKEY": "/Ankama/v5/Account/SignOnWithApiKey",
                "SET_NICKNAME": "/Ankama/v5/Account/SetNicknameWithApiKey",
                "START_SESSION_WITH_API_KEY": "/Ankama/v5/Game/StartSessionWithApiKey",
                "LIST_WITH_API_KEY": "/Ankama/v5/Game/ListWithApiKey",
                "SEND_MAIL_VALIDATION": "/Ankama/v5/Account/SendMailValidation",
                "SECURITY_CODE": "/Ankama/v5/Shield/SecurityCode",
                "VALIDATE_CODE": "/Ankama/v5/Shield/ValidateCode",
                "DELETE_API_KEY": "/Ankama/v5/Api/DeleteApiKey",
                "CREATE_GUEST": "/Ankama/v2/Account/CreateGuest",
                "CREATE_TOKEN": "/Ankama/v5/Account/CreateToken",
                "SEND_EVENTS": "/Ankama/v5/Game/SendEvents",
                "SEND_EVENT": "/Ankama/v5/Game/SendEvent",
                "END_SESSION_WITH_API_KEY": "/Ankama/v5/Game/EndSessionWithApiKey",
                "ANKAMA_ACCOUNT_STATUS": "/Ankama/v5/Account/Status",
                "GET_FROM_CMS": "/Ankama/v5/Cms/Items/Get",
                "GET_FROM_CMS_BYID": "/Ankama/v5/Cms/Items/GetById",
                "GET_LEGALS_TOU": "/Ankama/v5/Legals/Tou",
                "SEND_DEVICE_INFOS": "/Ankama/v5/Account/SendDeviceInfos",
                "CAROUSEL_FORLAUNCHER": "/Ankama/v5/Cms/Items/Carousel/GetForLauncher",
            }
        if request not in queries:
            raise HaapiException(f"Unknown request: {request}")
        result = self.BASE_URL + queries[request]
        if params:
            result += "?" + urlencode(params)
        return result

    def sendDeviceInfos(self, session_id, connection_type, client_type, os, device, partner, device_uid, apikey=None):
        if not apikey:
            apikey = self.zaap_apikey
        if not session_id:
            session_id = self.session_id
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

    def sendEvents(self, game: int, sessionId: int, events: str):
        if not sessionId:
            sessionId = self.session_id
            if not sessionId:
                raise Exception("Need a session_id to send events")
        url = self.getUrl("SEND_EVENTS")
        response = self.zaap_session.post(
            url, data={"game": game, "session_id": sessionId, "events": json.dumps(events)},
            verify=self.verify_ssl
        )
        self.zaap_session.cookies.update(response.cookies)
        if not response.ok:
            raise Exception(f"Error while sending events: {response.text}")
        return response

    @property
    def zaap_apikey(self):
        if not self._zaap_apikey:
            raise HaapiException("No API key set")
        return self._zaap_apikey

    @zaap_apikey.setter
    def zaap_apikey(self, api_key):
        self._zaap_apikey = api_key

    def signOnWithApikey(self, game_id, apikey=None):
        if not apikey:
            apikey = self.zaap_apikey
        url = self.getUrl("SIGN_ON_WITH_APIKEY", {"game": game_id})
        response = self.zaap_session.post(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        body = response.json()
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
            apikey = self.zaap_apikey
        url = self.getUrl("LIST_WITH_API_KEY")
        response = self.zaap_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        with open(f"tracking.json", "w") as f:
            f.write(response.text)

    def getAccountStatus(self, apikey=None):
        if not apikey:
            apikey = self.zaap_apikey
        url = self.getUrl("ANKAMA_ACCOUNT_STATUS")
        response = self.zaap_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)

    @staticmethod
    def get_date():
        timezone = pytz.timezone("UTC")
        now = datetime.now(timezone)
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
        formatted_date = formatted_date[:-2] + ":" + formatted_date[-2:]
        return formatted_date

    def startSessionWithApiKey(self, session_id, server_id="", character_id="", date="", apikey=None):
        if not apikey:
            apikey = self.zaap_apikey
        url = self.getUrl(
            "START_SESSION_WITH_API_KEY",
            {
                "session_id": session_id,
                "server_id": server_id,
                "character_id": character_id,
                "date": date,
            },
        )
        response = self.zaap_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        self.zaap_session.cookies.update(response.cookies)
        self.session_id = response.json()
        return response.json()

    def endSessionWithApiKey(self, session_id, subscriber="", close_account_session=True, apikey=None):
        if not apikey:
            apikey = self.zaap_apikey
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

    def createToken(self, game, certId="", certHash="", apikey=None):
        nbrtries = 0
        while nbrtries < 5:
            try:
                if apikey is None:
                    apikey = self.zaap_apikey
                url = self.getUrl(
                    "CREATE_TOKEN",
                    {
                        "game": game,
                        "certificate_id": certId,
                        "certificate_hash": certHash,
                    },
                )
                Logger().debug("[HAAPI] Calling HAAPI to get Login Token, url: %s" % url)
                response = self.zaap_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
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
            except ConnectionError as exc:
                Logger().error("1) No internet connection will try again in some seconds: %s" % exc)
                sleep(30)
