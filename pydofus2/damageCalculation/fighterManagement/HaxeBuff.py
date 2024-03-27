class HaxeBuff:
    DAMAGE_TRIGGERS = ["D", "DN", "DE", "DF", "DW", "DA", "DG", "DT", "DI", "DBA", "DBE", "DM", "DR", "DCAC", "DS", "PD", "PMD", "PPD", "DV"]

    def __init__(self, caster_id: float, spell, effect, trigger_count: int = 0):
        self._starting_trigger_count = 0
        self._trigger_count = 0
        self.spell_state = None
        self.has_been_triggered_on = []
        self.spell = spell
        self.caster_id = caster_id
        self.effect = effect
        self._trigger_count = self._starting_trigger_count = trigger_count
        
        if effect.action_id == 950:
            self.spell_state = DamageCalculator.dataInterface.createStateFromId(effect.param3)

    @property
    def trigger_count(self):
        return self._trigger_count

    @trigger_count.setter
    def trigger_count(self, value):
        self._trigger_count = value
