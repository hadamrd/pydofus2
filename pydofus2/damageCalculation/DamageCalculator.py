class DamageCalculator:
    @staticmethod
    def create32BitHashSpellLevel(param1, param2):
        return (param2 << 24) | param1
