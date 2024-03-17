from pydofus2.com.ankamagames.dofus.misc.utils import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages import Action


class DirectSelectionCharacterAction(AbstractAction, Action):
    serverId: int
    characterId: float
    
    def __init__(self, params=None):
        super().__init__(params)
        
    @staticmethod
    def create(serverId: int, characterId: float, *args) -> 'DirectSelectionCharacterAction':
        a = DirectSelectionCharacterAction(args)
        a.serverId = serverId
        a.characterId = characterId
        return a