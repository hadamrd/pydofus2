class FighterStatus:
    cantUseSpells: bool = None
    cantUseCloseQuarterAttack: bool = None
    cantDealDamage: bool = None
    invulnerable: bool = None
    incurable: bool = None
    cantBeMoved: bool = None
    cantBePushed: bool = None
    cantSwitchPosition: bool = None
    invulnerableMelee: bool = None
    invulnerableRange: bool = None
    cantTackle: bool = None
    cantBeTackled: bool = None

    def __init__(self) -> None:
        pass

    def getActiveStatuses(self):
        active_statuses = []
        for attribute, value in self.__dict__.items():
            if value is True:
                active_statuses.append(attribute)
        return ", ".join(active_statuses)
