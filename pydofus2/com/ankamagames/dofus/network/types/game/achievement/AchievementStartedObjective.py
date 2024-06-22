from pydofus2.com.ankamagames.dofus.network.types.game.achievement.AchievementObjective import AchievementObjective


class AchievementStartedObjective(AchievementObjective):
    value: int

    def init(self, value_: int, id_: int, maxValue_: int):
        self.value = value_

        super().init(id_, maxValue_)
