from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.authorized.AdminCommandMessage import \
    AdminCommandMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.Uuid import Uuid
    

class AdminQuietCommandMessage(AdminCommandMessage):
    def init(self, messageUuid_: 'Uuid', content_: str):
        
        super().init(messageUuid_, content_)
    