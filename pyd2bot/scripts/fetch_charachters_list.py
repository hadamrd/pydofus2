from time import sleep
from pydofus2.com.DofusClient import DofusClient
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from launcher.AccountCredsManager import AccountCredsManager
from pyd2bot.logic.managers.BotCredsManager import BotCredsManager

logger = Logger("Dofus2")

if __name__ == "__main__":
    accountId = "aloone-100"
    serverId = 210
    username = "aloone-100"
    password = "rmrtxha1"
    AccountCredsManager.addEntry(accountId, username, password)
    dofus2 = DofusClient()
    dofus2.login(accountId, serverId)
    while not PlayerManager().charactersList:
        sleep(0.2)
    for char in PlayerManager().charactersList:
        BotCredsManager.addEntry(f"{char.name}({serverId})", accountId, char.id, serverId)
    dofus2.shutdown()
