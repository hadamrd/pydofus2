from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class BreachInvitationAnswerMessage(NetworkMessage):
    accept: bool

    def init(self, accept_: bool):
        self.accept = accept_

        super().__init__()
