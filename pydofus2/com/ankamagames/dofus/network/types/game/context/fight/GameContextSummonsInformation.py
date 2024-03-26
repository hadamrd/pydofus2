from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameContextBasicSpawnInformation import \
        GameContextBasicSpawnInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacteristics import \
        GameFightCharacteristics
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.SpawnInformation import \
        SpawnInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook


class GameContextSummonsInformation(NetworkMessage):
    spawnInformation: "SpawnInformation"
    wave: int
    look: "EntityLook"
    stats: "GameFightCharacteristics"
    summons: list["GameContextBasicSpawnInformation"]

    def init(
        self,
        spawnInformation_: "SpawnInformation",
        wave_: int,
        look_: "EntityLook",
        stats_: "GameFightCharacteristics",
        summons_: list["GameContextBasicSpawnInformation"],
    ):
        self.spawnInformation = spawnInformation_
        self.wave = wave_
        self.look = look_
        self.stats = stats_
        self.summons = summons_

        super().__init__()
