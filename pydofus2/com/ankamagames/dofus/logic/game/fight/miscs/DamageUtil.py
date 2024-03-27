import logging

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.FighterTranslator import FighterTranslator
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.MapTranslator import MapTranslator
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.SpellEffectTranslator import SpellEffectTranslator
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.castSpellManager.SpellManager import SpellManager
from pydofus2.damageCalculation.FightContext import FightContext

class DamageUtil:
    HEALING_EFFECTS_IDS = [81, 108, 1109, 90]
    HP_BASED_DAMAGE_EFFECTS_IDS = [672, 85, 86, 87, 88, 89, 90]

    @staticmethod
    def verifySpellEffectMask(pCasterId, pTargetId, pEffect, pSpellImpactCell, pTriggeringSpellCasterId=0):
        fcf = Kernel().fightContextFrame
        if not pEffect.targetMask:
            return True
        if not pEffect or pEffect.delay > 0:
            return False
        infos = fcf.entitiesFrame.getEntityInfos(pCasterId)
        if infos:
            caster = FighterTranslator(infos, pCasterId)
            gameTurn = CurrentPlayedFighterManager().getSpellCastManager().currentTurn
            fightContext = FightContext(gameTurn, MapTranslator(fcf), pSpellImpactCell, caster)
            target = fightContext.getFighterById(pTargetId)
            effect = SpellEffectTranslator.fromSpell(pEffect, 1, False)
            triggeringFighter = fightContext.getFighterById(pTriggeringSpellCasterId)
            return SpellManager.isSelectedByMask(caster, effect.masks, target, triggeringFighter, fightContext)
        return False
