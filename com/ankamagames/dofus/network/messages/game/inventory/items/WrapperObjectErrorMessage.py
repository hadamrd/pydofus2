from com.ankamagames.dofus.network.messages.game.inventory.items.SymbioticObjectErrorMessage import SymbioticObjectErrorMessage


class WrapperObjectErrorMessage(SymbioticObjectErrorMessage):
    

    def init(self, errorCode:int, reason:int):
        
        super().__init__(errorCode, reason)
    
    