class HaxeBuff:
    DAMAGE_TRIGGERS = [
        "D",
        "DN",
        "DE",
        "DF",
        "DW",
        "DA",
        "DG",
        "DT",
        "DI",
        "DBA",
        "DBE",
        "DM",
        "DR",
        "DCAC",
        "DS",
        "PD",
        "PMD",
        "PPD",
        "DV",
    ]

    def __init__(self, caster_id: float, spell, effect, triggerCount: int = 0):
        self._startingTriggerCount = 0
        self._triggerCount = 0
        self.spellState = None
        self.hasBeenTriggeredOn = []
        self.spell = spell
        self.caster_id = caster_id
        self.effect = effect
        self._triggerCount = self._startingTriggerCount = triggerCount

        # if effect.actionId == 950:
        #     self.spellState = DamageCalculator.dataInterface.createStateFromId(effect.param3)

    @property
    def trigger_count(self):
        return self._triggerCount

    @trigger_count.setter
    def trigger_count(self, value):
        self._triggerCount = value
