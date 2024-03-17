from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.alignment.war.effort.AlignmentWarEffortInformation import \
        AlignmentWarEffortInformation
    

class AlignmentWarEffortProgressionMessage(NetworkMessage):
    effortProgressions: list['AlignmentWarEffortInformation']
    def init(self, effortProgressions_: list['AlignmentWarEffortInformation']):
        self.effortProgressions = effortProgressions_
        
        super().__init__()
    