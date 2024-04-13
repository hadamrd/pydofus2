# File: tests/test_integration.py
import json
import os
import uuid

import pydantic
from pyd2bot.data.models import Character, Credentials, Path, Session
from pyd2bot.Pyd2Bot import Pyd2Bot


class Secret(pydantic.Basemodel):
    character: Character
    credentials: Credentials


class BotFightTester(Pyd2Bot):
    def __init__(
        self,
        decoded_git_secret: Secret,
        test_path,
        monster_lvl_coef_diff: float,
        fights_per_minute: float,
        test_session_timeout: int = 30,
    ):
        session = Session(
            {
                "id": uuid.uuid4(),
                "character": decoded_git_secret.character,
                "type": "SOLO_FIGHT",
                "credentials": decoded_git_secret.credentials,
                "unloadType": "BANK",
                "path": test_path,
                "monsterLvlCoefDiff": monster_lvl_coef_diff,
                "fightsPerMinute": fights_per_minute,
                "sessionTimeout": test_session_timeout,
            }
        )
        super().__init__(session)

    def startSessionMainBehavior(self):
        BotFightBehavior(self.session).start(self.onMainBehaviorFinish)


def test_fight():
    bot_creds = os.getenv("BOT_CREDENTIALS")
    fightsPerMinute = os.getenv("FIGHTS_PER_MINUTE")
    monsterLvlCoefDiff = os.getenv("MONSTER_LVL_COEF_DIFF")
    testPath = Path(**json.loads(os.getenv("TEST_PATH")))
    testDuration = os.getenv("TEST_DURATION")
    decoded_git_secret = Secret(**json.loads(bot_creds))
    bot_tester = BotFightTester(decoded_git_secret, testPath, monsterLvlCoefDiff, fightsPerMinute, testDuration)
    test_result = True
    fail_error = None

    def onShutdown(reason, message):
        nonlocal test_result
        nonlocal fail_error
        if reason != "WANTED_SHUTDOWN":
            test_result = False

    bot_tester.addShutDownListener(onShutdown)
    bot_tester.start()
    bot_tester.join()
    assert test_result, fail_error
