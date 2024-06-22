from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.nuggets.NuggetsBeneficiary import NuggetsBeneficiary


class NuggetsDistributionMessage(NetworkMessage):
    beneficiaries: list["NuggetsBeneficiary"]

    def init(self, beneficiaries_: list["NuggetsBeneficiary"]):
        self.beneficiaries = beneficiaries_

        super().__init__()
