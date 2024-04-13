from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightLootObject import FightLootObject


class FightLoot(NetworkMessage):
    objects: list["FightLootObject"]
    kamas: int

    def init(self, objects_: list["FightLootObject"], kamas_: int):
        self.objects = objects_
        self.kamas = kamas_

        super().__init__()
