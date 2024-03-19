# pydofus2

This is a 100% python lightweight client of dofus. In its structure its very close to the original source code of the game.
Its used by the pyd2bot module, that adds extra frames to the worker process, these extra frames implement the bot logic.

## Use case for character creation

Full code is in the examples folder

### Main 
```python
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
    print(f"Token : {token}")
    if not token:
        raise Exception("Token is None")
    
    client = DofusClient(api_key)
    client.setApiKey(apikey)
    client.setCertificate(certid, certhash)
    client.start()

    eventsManager = KernelEventsManager.WaitThreadRegister(api_key, 25)

    Logger().info("Kernel event manager instance created")
        
    def onNewCharacterEnded(error, character: BasicCharacterWrapper):
        if character:
            client.shutdown(msg=f"Character {character.name} created successfully")
        else:
            client.crash(None, message=f"Character creation ended with error : {error}")
            
    def onCharactersList(event, characters: list[BasicCharacterWrapper]):
        Logger().info("Characters list received")
        characterCreator.run(breedId, callback=onNewCharacterEnded)
    
    eventsManager.once(KernelEvent.CharactersList, onCharactersList)

    client.join()
    
    if client._crashed:
        raise Exception(client._shutDownMessage)

    print(client._shutDownMessage)
```

### Character creator
```python
from pydofus2.com.ankamagames.berilia.managers.EventsHandler import Event
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.breeds.Breed import Breed
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.DofusClient import DofusClient


class CharacterCreator:

    def __init__(self) -> None:
        super().__init__()
        self.requestTimer = None

    def run(self, breedId, name=None, sex=False, callback=None) -> bool:
        self._name = name
        self._breedId = breedId
        self._breed = Breed.getBreedById(breedId)
        if not self._breed:
            return callback("Invalid breedId", None)
        self.sex = sex
        self.character = None
        self.get_name_suggestion_fails = 0
        self.callback = callback
        Logger().info(f"Create character called : breedId {breedId}, name {name}, sex {sex}.")
        if self._name is None:
            self.askNameSuggestion()
        else:
            self.requestNewCharacter()

    def onCharacterNameSuggestion(self, event: Event, suggestion):
        self._name = suggestion
        DofusClient().terminated.wait(5)  # wait 5 seconds before sending character creation request
        self.requestNewCharacter()

    def finish(self, err, character):
        KernelEventsManager().clearAllByOrigin(self)  # clear all listeners registered by this instance
        self.callback(err, character)

    def askNameSuggestion(self):
        self.once(KernelEvent.CharacterNameSuggestion, self.onCharacterNameSuggestion)
        self.once(KernelEvent.CharacterNameSuggestionFailed, self.onCharacterNameSuggestionFail)
        Kernel().gameServerApproachFrame.requestNameSuggestion()

    def onCharacterNameSuggestionFail(self, event: Event):
        self.get_name_suggestion_fails += 1
        if self.get_name_suggestion_fails > 3:
            return self.finish("failed to get character name suggestion", None)
        DofusClient().terminated.wait(5)  # wait 5 seconds before retrying
        self.once(KernelEvent.CharacterNameSuggestionFailed, self.onCharacterNameSuggestionFail)
        Kernel().gameServerApproachFrame.requestNameSuggestion()

    def onNewCharacterResult(self, event, result, reason, error_text):
        if result > 0:
            return self.finish(f"Create character error : {error_text}", None)
        self.once(KernelEvent.CharactersList, self.onCharacterList)

    def onCharacterList(self, event, charactersList):
        for ch in PlayerManager().charactersList:
            if ch.name == self._name:
                return self.finish(None, ch)
        self.finish("The created character is not found in characters list!", None)

    def requestNewCharacter(self):
        ssi = Kernel().serverSelectionFrame.getSelectedServerInformations()
        if ssi is None:
            return self.finish("No server selected", None)
        if ssi.charactersCount >= ssi.charactersSlots:
            return self.finish("No more character slots", None)
        self.once(
            KernelEvent.CharacterCreationResult,
            self.onNewCharacterResult,
            timeout=10,
            ontimeout=lambda: self.finish("Request character create timedout", None),
        )
        Kernel().gameServerApproachFrame.requestCharacterCreation(
            str(self._name), int(self._breedId), bool(self.sex), [12488553, 9163102, 4542781, 6921543, 12114595], 145
        )

    def once(self, event_id, callback, timeout=None, ontimeout=None):
        return KernelEventsManager().once(
            event_id, callback=callback, originator=self, timeout=timeout, ontimeout=ontimeout
        )

```