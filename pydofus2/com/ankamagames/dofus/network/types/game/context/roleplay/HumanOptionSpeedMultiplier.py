from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOption import HumanOption


class HumanOptionSpeedMultiplier(HumanOption):
    speedMultiplier: int

    def init(self, speedMultiplier_: int):
        self.speedMultiplier = speedMultiplier_

        super().init()
