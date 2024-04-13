from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorPreset import TaxCollectorPreset


class TaxCollectorPresetsMessage(NetworkMessage):
    presets: list["TaxCollectorPreset"]

    def init(self, presets_: list["TaxCollectorPreset"]):
        self.presets = presets_

        super().__init__()
