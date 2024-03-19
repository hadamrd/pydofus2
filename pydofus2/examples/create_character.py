import threading

from pydofus2.com.ankamagames.atouin.Haapi import Haapi
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.connection.BasicCharacterWrapper import \
    BasicCharacterWrapper
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.DofusClient import DofusClient
from pydofus2.examples.CharacterCreator import CharacterCreator

if __name__ == "__main__":
    account_login = "YOUR_LOGIN"
    
    serverId = 293 # Tylezia server id example
    breedId = 10 # Sadida breed id example
    DOFUS_GAMEID = 1 # Dofus 2
    
    characterCreator = CharacterCreator()
    client = DofusClient(account_login)
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

    print(client._shutDownMessage)
