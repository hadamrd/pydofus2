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
