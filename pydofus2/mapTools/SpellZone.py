class SpellZone:
    
    @classmethod
    def fromRawZone(cls, param1: str) -> 'SpellZone':
        if param1 is None:
            param1 = "P"
        spellZone = SpellZone()
        spellZone.shape = param1[0]
        params = [p for p in param1[1:].split(",") if p]
        _loc4_ = False

        if spellZone.shape == ";":
            cells = [int(p) for p in params]
            spellZone.getCells = lambda x, y: cells
            spellZone.isCellInZone = lambda cell, x, y: cell in cells
            return spellZone

        if spellZone.shape == "l":
            params[0], params[1] = params[1], params[0]

        if len(params) > 0:
            spellZone.radius = int(params[0])
        
        if SpellZone.hasMinSize(spellZone.shape):
            if len(params) > 1:
                spellZone.minRadius = int(params[1])
            if len(params) > 2:
                spellZone.degression = int(params[2])
        else:
            if len(params) > 1:
                spellZone.degression = int(params[1])
            if len(params) > 2:
                spellZone.maxDegressionTicks = int(params[2])
        
        if len(params) > 3:
            spellZone.maxDegressionTicks = int(params[3])
        if len(params) > 4:
            _loc4_ = int(params[4]) != 0

    @staticmethod
    def hasMinSize(rawZone: str) -> bool:
        return rawZone in ["#", "+", "C", "Q", "R", "X", "l"]