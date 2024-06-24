from functools import cmp_to_key

from pydofus2.com.ankamagames.dofus.logic.game.fight.types.castSpellManager.SpellManager import SpellManager


class HaxeSpellEffect:
    INVALID_ACTION_ID = -1
    EMPTY = None

    def __init__(
        self,
        id: int,
        level: int,
        order: int,
        actionId: int,
        param1: int,
        param2: int,
        param3: int,
        duration: int,
        isCritical: bool,
        trigger: str,
        rawZone: str,
        mask: str,
        randomWeight: float,
        randomGroup: int,
        isDispellable: bool,
        delay: int,
        category: int,
    ):
        self._useCount = 0
        self.id = id
        self.level = level
        self.order = order
        self.actionId = actionId
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.duration = duration
        self.isCritical = isCritical
        self.triggers = SpellManager.splitTriggers(trigger)
        self.rawZone = rawZone
        self.masks = SpellManager.splitMasks(mask)
        self.masks.sort(key=cmp_to_key(HaxeSpellEffect.sortMasks))
        self.randomWeight = randomWeight
        self.randomGroup = randomGroup
        self.isDispellable = isDispellable
        self.delay = delay
        self.category = category
        # self.zone = SpellZone.fromRawZone(rawZone)
        self.zone = None

    @staticmethod
    def sortMasks(param1: str, param2: str) -> int:
        order = "*bBeEfFzZKoOPpTWUvVrRQq"
        if param1[0] in order:
            if param2[0] in order:
                if param1[0] == "*" and param2[0] != "*":
                    return -1
                if param2[0] == "*" and param1[0] != "*":
                    return 1
                # Compare based on their order in the string
                return order.index(param1[0]) - order.index(param2[0])
            return -1
        if param2[0] in order:
            return 1
        return 0


# Placeholder for HaxeSpellEffect.EMPTY initialization
HaxeSpellEffect.EMPTY = HaxeSpellEffect(0, 1, 0, 666, 0, 0, 0, 0, False, "I", "", "", 0, 0, False, 0, 0)
