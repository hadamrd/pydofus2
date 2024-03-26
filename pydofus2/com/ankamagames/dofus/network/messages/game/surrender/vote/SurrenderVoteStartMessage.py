from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class SurrenderVoteStartMessage(NetworkMessage):
    alreadyCastedVote: bool
    numberOfParticipants: int
    castedVoteNumber: int
    voteDuration: int

    def init(self, alreadyCastedVote_: bool, numberOfParticipants_: int, castedVoteNumber_: int, voteDuration_: int):
        self.alreadyCastedVote = alreadyCastedVote_
        self.numberOfParticipants = numberOfParticipants_
        self.castedVoteNumber = castedVoteNumber_
        self.voteDuration = voteDuration_

        super().__init__()
