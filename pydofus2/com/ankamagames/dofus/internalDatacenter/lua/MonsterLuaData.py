class MonsterLuaData:

    def __init__(
        self,
        pLevel: int,
        pXp: int,
        pHiddenLevel: int,
        pBonusFamily: float = 1.0,
        pBonusAlmanac: float = 1.0,
        pAlive: bool = True,
    ):
        self.level = pLevel
        self.xp = pXp
        self.hiddenLevel = pHiddenLevel
        self.bonusFamily = pBonusFamily
        self.bonusAlmanac = pBonusAlmanac
        self.alive = pAlive

    def __str__(self):
        return f"level={self.level};xp={self.xp};hiddenLevel={self.hiddenLevel};bonusFamily={self.bonusFamily};bonusAlmanach={self.bonusAlmanac};alive={self.alive};"
