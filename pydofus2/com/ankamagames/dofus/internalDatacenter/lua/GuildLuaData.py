class GuildLuaData:

    def __init__(self, pLevel: int = 1, pCoefficient: float = 0.0):
        self.level = pLevel
        self.coefficient = pCoefficient

    def __str__(self):
        return f"level={self.level};coefficient={self.coefficient};"
