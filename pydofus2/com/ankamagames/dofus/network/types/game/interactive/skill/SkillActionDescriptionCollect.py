from pydofus2.com.ankamagames.dofus.network.types.game.interactive.skill.SkillActionDescriptionTimed import (
    SkillActionDescriptionTimed,
)


class SkillActionDescriptionCollect(SkillActionDescriptionTimed):
    min: int
    max: int

    def init(self, min_: int, max_: int, time_: int, skillId_: int):
        self.min = min_
        self.max = max_

        super().init(time_, skillId_)
