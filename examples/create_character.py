from examples.CharacterCreator import CharacterCreator
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.connection.BasicCharacterWrapper import \
    BasicCharacterWrapper
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.DofusClient import DofusClient

if __name__ == "__main__":
    Logger.logToConsole = True

    account_login = "YOUR_LOGIN"
    serverId = 293  # Tylezia server id example
    breedId = 10  # Sadida breed id example
    DOFUS_GAMEID = 1  # Dofus 2
    APIKEY = "YOUR API KEY"
    CERTID = "YOUR CERT ID"
    CERTHASH = "YOUR CERT HASH"

    characterCreator = CharacterCreator()
    client = DofusClient(account_login)
    client.setApiKey(APIKEY)
    client.setCertificate(CERTID, CERTHASH)
    client.setAutoServerSelection(serverId)
    eventsManager = KernelEventsManager.waitThreadRegister(account_login, 25)

    Logger().info("Kernel event manager instance created")

    def onNewCharacterEnded(error, character: BasicCharacterWrapper):
        if character:
            client.shutdown(message=f"Character {character.name} created successfully")
        else:
            client.crash(None, message=f"Character creation ended with error : {error}")

    def onCharactersList(event, characters: list[BasicCharacterWrapper]):
        Logger().info("Characters list received")
        characterCreator.run(breedId, callback=onNewCharacterEnded)

    eventsManager.once(KernelEvent.CharactersList, onCharactersList)

    client.join()
