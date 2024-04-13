from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyUpdateLightMessage import (
    PartyUpdateLightMessage,
)


class PartyEntityUpdateLightMessage(PartyUpdateLightMessage):
    indexId: int

    def init(
        self,
        indexId_: int,
        id_: int,
        lifePoints_: int,
        maxLifePoints_: int,
        prospecting_: int,
        regenRate_: int,
        partyId_: int,
    ):
        self.indexId = indexId_

        super().init(id_, lifePoints_, maxLifePoints_, prospecting_, regenRate_, partyId_)
