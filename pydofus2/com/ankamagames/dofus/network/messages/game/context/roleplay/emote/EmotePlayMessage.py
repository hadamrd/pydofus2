from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.emote.EmotePlayAbstractMessage import (
    EmotePlayAbstractMessage,
)


class EmotePlayMessage(EmotePlayAbstractMessage):
    actorId: int
    accountId: int

    def init(self, actorId_: int, accountId_: int, emoteId_: int, emoteStartTime_: int):
        self.actorId = actorId_
        self.accountId = accountId_

        super().init(emoteId_, emoteStartTime_)
