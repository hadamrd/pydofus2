from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BlockEvadeBuff import \
    BlockEvadeBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.CastingSpell import \
    CastingSpell
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import \
    StatBuff
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporaryBoostEffect import \
    FightTemporaryBoostEffect


class StatBuffFactory:
    def __init__(self):
        super().__init__()

    @classmethod
    def createStatBuff(
        cls,
        pEffect: FightTemporaryBoostEffect,
        pCastingSpell: CastingSpell,
        pActionId: int,
    ) -> StatBuff:
        buff: StatBuff = None
        if pActionId in [
            ActionIds.ACTION_CHARACTER_BOOST_TAKLE_EVADE,
            ActionIds.ACTION_CHARACTER_BOOST_TAKLE_BLOCK,
            ActionIds.ACTION_CHARACTER_DEBOOST_TAKLE_EVADE,
            ActionIds.ACTION_CHARACTER_DEBOOST_TAKLE_BLOCK,
        ]:
            buff = BlockEvadeBuff(pEffect, pCastingSpell, pActionId)
        else:
            buff = StatBuff(pEffect, pCastingSpell, pActionId)
        return buff
