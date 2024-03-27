class Mark:
    def __init__(self):
        self.associatedSpell = None
        self.markType = 0
        self.teamId = None
        self.markId = None
        self.mainCell = None
        self.cells = None
        self.casterId = None
        self.active = None

    def stopDrag(self):
        if self.markType in [2, 3]:
            return True
        return False

    def setMarkType(self, markType):
        self.markType = markType
        if self.markType != 0 and self.associatedSpell is not None:
            if self.markType == 1:
                self.associatedSpell.isGlyph = True
                self.associatedSpell.isTrap = False
                self.associatedSpell.isRune = False
            elif self.markType == 2:
                self.associatedSpell.isTrap = True
                self.associatedSpell.isGlyph = False
                self.associatedSpell.isRune = False
            elif self.markType == 5:
                self.associatedSpell.isRune = True
                self.associatedSpell.isTrap = False
                self.associatedSpell.isGlyph = False

    def setAssociatedSpell(self, associatedSpell):
        self.associatedSpell = associatedSpell
        self.adaptSpellToType()

    def adaptSpellToType(self):
        if self.markType != 0 and self.associatedSpell is not None:
            if self.markType == 1:
                self.associatedSpell.isGlyph = True
                self.associatedSpell.isTrap = False
                self.associatedSpell.isRune = False
            elif self.markType == 2:
                self.associatedSpell.isTrap = True
                self.associatedSpell.isGlyph = False
                self.associatedSpell.isRune = False
            elif self.markType == 5:
                self.associatedSpell.isRune = True
                self.associatedSpell.isTrap = False
                self.associatedSpell.isGlyph = False
