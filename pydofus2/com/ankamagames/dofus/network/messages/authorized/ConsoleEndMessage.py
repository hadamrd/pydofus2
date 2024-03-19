from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.uuid import Uuid
    

class ConsoleEndMessage(NetworkMessage):
    consoleUuid: 'Uuid'
    isSuccess: bool
    def init(self, consoleUuid_: 'Uuid', isSuccess_: bool):
        self.consoleUuid = consoleUuid_
        self.isSuccess = isSuccess_
        
        super().__init__()
    