import datetime
import math
from urllib.parse import urlencode

import requests

from pydofus2.com.ankamagames.dofus.BuildInfos import BuildInfos
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig


class GameApi:
    BASE_URL = XmlConfig().getEntry("config.haapiUrlAnkama")

    # Event types
    event_admin_right_with_api_key = "admin_right_with_api_key"
    event_end_anonymous_session = "end_anonymous_session"
    event_end_session_with_api_key = "end_session_with_api_key"
    event_game_enemies = "game_enemies"
    event_game_friends = "game_friends"
    event_list_with_api_key = "list_with_api_key"
    event_send_event = "send_event"
    event_send_events = "send_events"
    event_start_anonymous_session = "start_anonymous_session"
    event_start_session_with_api_key = "start_session_with_api_key"

    # Game enums
    sendEvent_GameEnum_1 = "1"
    sendEvent_GameEnum_3 = "3"
    sendEvent_GameEnum_11 = "11"
    sendEvent_GameEnum_16 = "16"
    sendEvent_GameEnum_17 = "17"
    sendEvent_GameEnum_18 = "18"
    sendEvent_GameEnum_21 = "21"
    sendEvent_GameEnum_22 = "22"
    sendEvent_GameEnum_101 = "101"
    sendEvent_GameEnum_102 = "102"
    sendEvent_GameEnum_106 = "106"
    sendEvent_GameEnum_666 = "666"
    sendEvents_GameEnum_1 = "1"
    sendEvents_GameEnum_3 = "3"
    sendEvents_GameEnum_11 = "11"
    sendEvents_GameEnum_16 = "16"
    sendEvents_GameEnum_17 = "17"
    sendEvents_GameEnum_18 = "18"
    sendEvents_GameEnum_21 = "21"
    sendEvents_GameEnum_22 = "22"
    sendEvents_GameEnum_101 = "101"
    sendEvents_GameEnum_102 = "102"
    sendEvents_GameEnum_106 = "106"
    sendEvents_GameEnum_108 = "108"
    sendEvents_GameEnum_666 = "666"

    def __init__(self):
        self.BASE_URL = XmlConfig().getEntry("config.haapiUrlAnkama")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "x-flash-version": "31,1,1,889",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": f"Dofus {BuildInfos().VERSION}",
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate",
                "Connection": "keep-alive",
            }
        )

    @staticmethod
    def is_valid_param(param):
        if isinstance(param, (int, float)) and not isinstance(param, bool):
            return not math.isnan(param)
        return param is not None

    @classmethod
    def getUrl(cls, request, params={}):
        result = (
            cls.BASE_URL
            + {
                "START_SESSION_WITH_API_KEY": "/Ankama/v4/Game/StartSessionWithApiKey",
            }[request]
        )
        if params:
            result += "?" + urlencode(params)
        return result

    def format_date(date_obj: datetime.datetime):
        """
        Format a datetime object to a string in the format "yyyy-MM-dd'T'HH:mm:ss+00:00".

        :param date_obj: The datetime object to format.
        :return: A string representing the formatted date.
        """
        formatted_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        return formatted_date
