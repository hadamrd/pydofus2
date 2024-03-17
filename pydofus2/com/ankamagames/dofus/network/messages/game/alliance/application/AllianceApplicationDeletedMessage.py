from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class AllianceApplicationDeletedMessage(NetworkMessage):
    deleted: bool
    def init(self, deleted_: bool):
        self.deleted = deleted_
        
        super().__init__()
    