from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.shortcut.Shortcut import Shortcut


class ShortcutBarContentMessage(INetworkMessage):
    protocolId = 7910
    barType:int
    shortcuts:Shortcut
    
    
