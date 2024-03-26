from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class ForceAccountStatusMessage(NetworkMessage):
    force: bool
    forcedAccountId: int
    forcedNickname: str
    forcedTag: str

    def init(self, force_: bool, forcedAccountId_: int, forcedNickname_: str, forcedTag_: str):
        self.force = force_
        self.forcedAccountId = forcedAccountId_
        self.forcedNickname = forcedNickname_
        self.forcedTag = forcedTag_

        super().__init__()
