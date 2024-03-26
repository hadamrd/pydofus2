from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.npc.TaxCollectorDialogQuestionBasicMessage import \
    TaxCollectorDialogQuestionBasicMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicAllianceInformations import \
        BasicAllianceInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicNamedAllianceInformations import \
        BasicNamedAllianceInformations


class TaxCollectorDialogQuestionExtendedMessage(TaxCollectorDialogQuestionBasicMessage):
    maxPods: int
    prospecting: int
    alliance: "BasicNamedAllianceInformations"
    taxCollectorsCount: int
    taxCollectorAttack: int
    pods: int
    itemsValue: int

    def init(
        self,
        maxPods_: int,
        prospecting_: int,
        alliance_: "BasicNamedAllianceInformations",
        taxCollectorsCount_: int,
        taxCollectorAttack_: int,
        pods_: int,
        itemsValue_: int,
        allianceInfo_: "BasicAllianceInformations",
    ):
        self.maxPods = maxPods_
        self.prospecting = prospecting_
        self.alliance = alliance_
        self.taxCollectorsCount = taxCollectorsCount_
        self.taxCollectorAttack = taxCollectorAttack_
        self.pods = pods_
        self.itemsValue = itemsValue_

        super().init(allianceInfo_)
