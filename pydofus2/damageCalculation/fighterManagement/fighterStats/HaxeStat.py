from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import ActionIdHelper


class HaxeStat:
    def __init__(self, stat_id: int):
        self.total = 0
        self.id = stat_id

    def updateStatWithValue(self, value: int, is_flat: bool) -> None: ...

    def updateStatFromEffect(self, effect, is_flat: bool) -> None:
        if ActionIdHelper.isFlatStatBoostActionId(effect.actionId) or ActionIdHelper.isPercentStatBoostActionId(
            effect.actionId
        ):
            self.updateStatWithValue(effect.getMinRoll(), is_flat)

    @property
    def get_total(self) -> int:
        return self.total

    @property
    def get_id(self) -> int:
        return self.id
