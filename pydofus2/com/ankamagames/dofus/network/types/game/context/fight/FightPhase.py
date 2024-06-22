from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class FightPhase(NetworkMessage):
    phase: int
    phaseEndTimeStamp: int

    def init(self, phase_: int, phaseEndTimeStamp_: int):
        self.phase = phase_
        self.phaseEndTimeStamp = phaseEndTimeStamp_

        super().__init__()
