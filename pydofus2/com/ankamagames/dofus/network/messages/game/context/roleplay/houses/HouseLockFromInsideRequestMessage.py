from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.lockable.LockableChangeCodeMessage import (
    LockableChangeCodeMessage,
)


class HouseLockFromInsideRequestMessage(LockableChangeCodeMessage):
    def init(self, code_: str):

        super().init(code_)
