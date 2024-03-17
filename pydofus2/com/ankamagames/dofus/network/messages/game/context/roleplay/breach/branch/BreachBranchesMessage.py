from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.breach.ExtendedBreachBranch import \
        ExtendedBreachBranch
    

class BreachBranchesMessage(NetworkMessage):
    branches: list['ExtendedBreachBranch']
    def init(self, branches_: list['ExtendedBreachBranch']):
        self.branches = branches_
        
        super().__init__()
    