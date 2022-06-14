import json
from time import sleep
import httpx
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton

logger = Logger("Haapi")


class Haapi(metaclass=Singleton):
    
    def __init__(self) -> None:
        self.url = "https://haapi.ankama.com"
        self.APIKEY = None

    def getUrl(self, request):
        return self.url + {
            "CREATE_API_KEY": "/json/Ankama/v5/Api/CreateApiKey",
            "GET_LOGIN_TOKEN": "/json/Ankama/v5/Account/CreateToken",
        }[request]

    def createAPIKEY(self, cert, login, password, game_id=102) -> str:
        logger.debug("Calling HAAPI to Create APIKEY")
        data = {
            "login": login,
            "password": password,
            "game_id": game_id,
            "long_life_token": True,
            "certificate_id": cert["id"],
            "certificate_hash": cert["hash"],
            "shop_key": "ZAAP",
            "payment_mode": "OK",
        }
        response = httpx.post(
            self.getUrl("CREATE_API_KEY"),
            data=data,
            headers={
                "User-Agent": "Zaap",
                "Content-Type": "multipart/form-data",
            },
        )
        self.APIKEY = response.json()["key"]
        logger.debug("APIKEY created")
        return self.APIKEY


    def getLoginToken(self, cert, login, password, game_id=1):
        logger.debug("Calling HAAPI to get Login Token")
        if not self.APIKEY:
            self.createAPIKEY(cert, login, password)
        nbrTries = 0
        while nbrTries < 3:
            response = httpx.get(
                self.getUrl("GET_LOGIN_TOKEN"),
                params={
                    "game": game_id,
                    "certificate_id": cert["id"],
                    "certificate_hash": cert["hash"],
                },
                headers={
                    "User-Agent": "Zaap1",
                    "Content-Type": "multipart/form-data",
                    "APIKEY": self.APIKEY,
                },
            )
            try:
                token = response.json()["token"]
                logger.debug("Login Token created")
                return token
            except json.decoder.JSONDecodeError as e:
                from bs4 import BeautifulSoup

                parsed_html = BeautifulSoup(response.content)
                reason = parsed_html.body.find("div", attrs={"id": "what-happened-section"}).find("p").text
                if (
                    reason
                    == "The owner of this website (haapi.ankama.com) has banned you temporarily from accessing this website."
                ):
                    logger.debug("Login Token creation failed, reason: %s" % reason)
                    logger.debug("Retrying in 60 seconds")
                    sleep(60)
