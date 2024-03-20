import json
import sys
import ssl
from datetime import datetime
from time import sleep
import traceback
from urllib.parse import urlencode
import functools

import pytz
import requests
from urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.BuildInfos import BuildInfos
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class HaapiException(Exception):
    pass

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def sendTrace(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _, exc_value, exc_traceback = sys.exc_info()
            traceback_in_var = traceback.format_tb(exc_traceback)
            error_trace = "\n".join(traceback_in_var) + "\n" + str(exc_value)
            cause = e.__cause__
            while cause:
                cause_traceback = traceback.format_tb(cause.__traceback__)
                error_trace += "\n\n-- Chained Exception --\n"
                error_trace += "\n".join(cause_traceback) + "\n" + str(cause)
                cause = cause.__cause__
            KernelEventsManager().send(KernelEvent.ClientCrashed, error_trace)
    return wrapped

class Haapi(metaclass=Singleton):
    MAX_CREATE_API_KEY_RETRIES = 5

    def __init__(self):
        self.BASE_URL = f"https://{XmlConfig().getEntry('config.haapiUrlAnkama')}"
        self.dofus_session = requests.Session()
        self.game_sessionId = None
        self.account_apikey = None
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
        retry_strategy = Retry(
            total=3,
            read=3,
            connect=3,
            backoff_factor=0.3,
            status_forcelist=(502,),
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.dofus_session.mount("http://", adapter)
        self.dofus_session.mount("https://", adapter)
        self.dofus_session.headers.update(self.dofus_headers)
        self.dofus_session.proxies.update(
            {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080",
            }
        )
        self.verify_ssl = False

    @sendTrace
    def getUrl(self, request, params={}):
        result = (
            self.BASE_URL
            + {
                "CREATE_API_KEY": "/Ankama/v4/Api/CreateApiKey",
                "CREATE_TOKEN": "/Ankama/v4/Account/CreateToken",
                "GET_ACCESS_TOKEN": "/Ankama/v4/Account/GetAccessToken",
                "SEND_EVENTS": "/Ankama/v4/Game/SendEvents",
                "SEND_EVENT": "/Ankama/v4/Game/SendEvent",
                "GET_ALMANAX_EVENT": "/Ankama/v4/Almanax/GetEvent",
                "GET_LOADING_SCREEN": "/Ankama/v4/Cms/Items/Loadingscreen/Get",
                "GET_CMS_FEEDS": "/Ankama/v4/Cms/Items/GetFeeds",
                "POLLIN_GAME_GET": "/Ankama/v4/Cms/PollInGame/Get",
            }[request]
        )
        if params:
            result += "?" + urlencode(params)
        return result

    @sendTrace
    def getLoadingScreen(self, page, accountId, lang, count):
        url = self.getUrl("GET_LOADING_SCREEN", {"page": page, "accountId": accountId, "lang": lang, "count": count})
        Logger().debug("[HAAPI] GET url: %s" % url)
        response = self.dofus_session.get(url, verify=self.verify_ssl)
        self.dofus_session.cookies.update(response.cookies)
        return response.json()

    @sendTrace
    def pollInGameGet(self, count, site, lang, page, apikey=None):
        if not apikey:
            apikey = self.account_apikey
        url = self.getUrl("POLLIN_GAME_GET", {"count": count, "site": site, "lang": lang, "page": page})
        Logger().debug("[HAAPI] GET url: %s" % url)
        response = self.dofus_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        self.dofus_session.cookies.update(response.cookies)
        return response.json()

    @sendTrace
    def getCmsFeeds(self, site, page, lang, count, apikey=None):
        if not apikey:
            apikey = self.account_apikey
        url = self.getUrl(
            "GET_CMS_FEEDS",
            {
                "site": site,
                "lang": lang,
                "page": page,
                "count": count,
            },
        )
        Logger().debug("[HAAPI] GET url: %s" % url)
        response = self.dofus_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
        self.dofus_session.cookies.update(response.cookies)
        return response.json()
    
    @sendTrace
    def getAlmanaxEvent(self, lang):
        url = self.getUrl("GET_ALMANAX_EVENT", {"lang": lang, "date": self.get_date()})
        Logger().debug("[HAAPI] GET url: %s" % url)
        response = self.dofus_session.get(url, verify=self.verify_ssl)
        self.dofus_session.cookies.update(response.cookies)
        return response.json()

    @sendTrace
    def sendEvents(self, game: int, session_id: int, events: str):
        if not session_id:
            session_id = self.game_sessionId
            if not session_id:
                raise Exception("Need a session_id to send events")
        url = self.getUrl("SEND_EVENTS")
        response = self.dofus_session.post(
            url, 
            data={"game": game, "session_id": session_id, "events": json.dumps(events)},
            verify=self.verify_ssl
        )
        self.dofus_session.cookies.update(response.cookies)
        if not response.ok:
            raise Exception(f"Error while sending events: {response.text}")
        return response

    @sendTrace
    def sendEvent(self, game: int, session_id: int, event_id: int, data: str, date=None):
        if not session_id:
            session_id = self.game_sessionId
            if not session_id:
                raise Exception("Need a session_id to send events")
        if not date:
            date = self.get_date()
        url = self.getUrl("SEND_EVENT")
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
    def account_apikey(self):
        if not self._account_apikey:
            raise HaapiException("No Account API key set")
        return self._account_apikey
    
    @account_apikey.setter
    def account_apikey(self, api_key):
        self._account_apikey = api_key

    @staticmethod
    @sendTrace
    def get_date():
        timezone = pytz.timezone("UTC")
        now = datetime.now(timezone)
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
        formatted_date = formatted_date[:-2] + ":" + formatted_date[-2:]
        return formatted_date

    @sendTrace
    def createToken(self, game_id, certId="", certHash="", apikey=None):
        nbrtries = 0
        while nbrtries < 5:
            try:
                if apikey is None:
                    apikey = self.account_apikey
                url = self.getUrl(
                    "CREATE_TOKEN",
                    {
                        "game": game_id,
                        "certificate_id": certId,
                        "certificate_hash": certHash,
                    },
                )
                Logger().debug("[HAAPI] GET url: %s" % url)
                response = self.dofus_session.get(url, headers={"apikey": apikey}, verify=self.verify_ssl)
                self.dofus_session.cookies.update(response.cookies)
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