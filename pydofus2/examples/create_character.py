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
    api_key = "YOUR_API_KEY"
    certId = "YOUR_CERT_ID"
    certHash = "YOUR_CERT_HASH"
    
    serverId = 293 # Tylezia server id example
    breedId = 10 # Sadida breed id example
    DOFUS_GAMEID = 1 # Dofus 2
    
    characterCreator = CharacterCreator()
    token = Haapi.createToken(DOFUS_GAMEID, apiKey=api_key, certId=int(certId), certHash=certHash)
    
    print(f"Token : {token}")
    if not token:
        raise Exception("Token is None")
    
    client = DofusClient(api_key)
    client.setAutoServerSelection(serverId)
    client.setLoginToken(token)
    client.start()

    eventsManager = KernelEventsManager.waitThreadRegister(api_key, 25)

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
