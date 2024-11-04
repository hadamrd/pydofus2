from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastSequenceContext import SpellCastSequenceContext
from pydofus2.com.ankamagames.dofus.network.Metadata import Metadata
from pydofus2.com.ankamagames.dofus.types.enums.LanguageEnum import LanguageEnum
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.network.messages.Worker import Worker

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.common.frames.AlignmentFrame import AlignmentFrame
    from pydofus2.com.ankamagames.dofus.logic.common.frames.BidHouseManagementFrame import BidHouseManagementFrame
    from pydofus2.com.ankamagames.dofus.logic.common.frames.CharacterFrame import CharacterFrame
    from pydofus2.com.ankamagames.dofus.logic.common.frames.ChatFrame import ChatFrame
    from pydofus2.com.ankamagames.dofus.logic.common.frames.ExternalGameFrame import ExternalGameFrame
    from pydofus2.com.ankamagames.dofus.logic.common.frames.MarketFrame import MarketFrame
    from pydofus2.com.ankamagames.dofus.logic.common.frames.MountDialogFrame import MountDialogFrame
    from pydofus2.com.ankamagames.dofus.logic.common.frames.QuestFrame import QuestFrame
    from pydofus2.com.ankamagames.dofus.logic.connection.frames.AuthenticationFrame import AuthenticationFrame
    from pydofus2.com.ankamagames.dofus.logic.connection.frames.ServerSelectionFrame import ServerSelectionFrame
    from pydofus2.com.ankamagames.dofus.logic.game.approach.frames.GameServerApproachFrame import (
        GameServerApproachFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.AveragePricesFrame import AveragePricesFrame
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.CommonExchangeManagementFrame import (
        CommonExchangeManagementFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.ExchangeManagementFrame import ExchangeManagementFrame
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.GuildDialogFrame import GuildDialogFrame
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.InventoryManagementFrame import (
        InventoryManagementFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.MountFrame import MountFrame
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.PlayedCharacterUpdatesFrame import (
        PlayedCharacterUpdatesFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SocialFrame import SocialFrame
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SpellInventoryManagementFrame import (
        SpellInventoryManagementFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightBattleFrame import FightBattleFrame
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import FightContextFrame
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import FightEntitiesFrame
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightTurnFrame import FightTurnFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.PartyFrame import PartyFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayContextFrame import RoleplayContextFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayEntitiesFrame import RoleplayEntitiesFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayInteractivesFrame import (
        RoleplayInteractivesFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayMovementFrame import RoleplayMovementFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayWorldFrame import RoleplayWorldFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.ZaapFrame import ZaapFrame


class Kernel(metaclass=Singleton):
    def __init__(self) -> None:
        self._worker: Worker = Worker()
        self.beingInReconnection: bool = False
        self._reset = True
        self.isMule = False
        self.restart_on_unexpected_conn_close = False

    @property
    def worker(self) -> Worker:
        return self._worker

    @property
    def reset(self) -> bool:
        return self._reset

    def init(self) -> None:
        if self._reset:
            Logger().info("Initializing ...")
            self._worker.reset()
            self.addInitialFrames()
            self._reset = False
            Logger().info(f"Using protocol #{Metadata.PROTOCOL_BUILD}, built on {Metadata.PROTOCOL_DATE}")
            Logger().info("Initialized")

    def reset(
        self,
        reloadData: bool = False,
    ) -> None:
        pass

        from pydofus2.com.ankamagames.atouin.HaapiEventsManager import HaapiEventsManager
        from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
        from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
        from pydofus2.com.ankamagames.dofus.logic.common.managers.InterClientManager import InterClientManager
        from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
        from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
        from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InactivityManager import InactivityManager
        from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
            PlayedCharacterManager,
        )
        from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
        from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
            CurrentPlayedFighterManager,
        )
        from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import FightersStateManager
        from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import (
            SpellModifiersManager,
        )
        from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer

        Logger().debug("Resetting ...")
        BenchmarkTimer.reset()
        KernelEventsManager().reset()
        FightersStateManager.clear()
        CurrentPlayedFighterManager.clear()
        DofusEntities.clear()
        ItemWrapper.clearCache()
        PlayedCharacterManager.clear()
        StatsManager.clear()
        PlayerManager.clear()
        DataMapProvider.clear()
        SpellModifiersManager.clear()
        HaapiEventsManager.clear()
        InactivityManager().stop()
        InactivityManager.clear()
        InterClientManager().freeFlashKey()
        SpellCastSequenceContext.reset()

        if not reloadData:
            self._worker.terminate()
        else:
            disconnectionHandlerFrame = self._worker.getFrameByName("DisconnectionHandlerFrame")
            self._worker.reset()
            self._worker.addFrame(disconnectionHandlerFrame)
        if ConnectionsHandler().conn and not ConnectionsHandler().conn.closed:
            ConnectionsHandler().closeConnection(DisconnectionReasonEnum.DISCONNECTED_BY_USER)
        self.beingInReconnection = False
        if reloadData:
            self.beingInReconnection = True
            self.addInitialFrames()
        else:
            Singleton.clearAll()
            self._reset = True
        Logger().debug("Reset")

    def getLocaleLang(self):
        current_lang = XmlConfig().getEntry("config.lang.current")
        binds = XmlConfig().getEntry("config.binds.current")
        switcher = {
            LanguageEnum.LANG_FR: "fr_FR" if binds == "frFR" else "fr_CA",
            LanguageEnum.LANG_EN: "en_US" if binds == "enUS" else "en_GB",
            LanguageEnum.LANG_ES: "es_ES",
            LanguageEnum.LANG_DE: "de_DE",
            LanguageEnum.LANG_IT: "it_IT",
            LanguageEnum.LANG_JA: "ja_JP",
            LanguageEnum.LANG_PT: "pt_PT" if binds == "ptPT" else "pt_BR",
            LanguageEnum.LANG_RU: "ru_RU",
            LanguageEnum.LANG_NL: "nl_NL",
        }
        return switcher.get(current_lang, "fr_FR")

    def addInitialFrames(self) -> None:
        from pydofus2.com.ankamagames.dofus.logic.common.frames.ChatFrame import ChatFrame
        from pydofus2.com.ankamagames.dofus.logic.common.frames.CleanupCrewFrame import CleanupCrewFrame
        from pydofus2.com.ankamagames.dofus.logic.common.frames.ExternalGameFrame import ExternalGameFrame
        from pydofus2.com.ankamagames.dofus.logic.common.frames.LatencyFrame import LatencyFrame
        from pydofus2.com.ankamagames.dofus.logic.common.frames.QueueFrame import QueueFrame
        from pydofus2.com.ankamagames.dofus.logic.connection.frames.AuthenticationFrame import AuthenticationFrame
        from pydofus2.com.ankamagames.dofus.logic.connection.frames.DisconnectionHandlerFrame import (
            DisconnectionHandlerFrame,
        )

        Logger().info("Adding initial frames ...")
        self._worker.addFrame(LatencyFrame())
        self._worker.addFrame(AuthenticationFrame())
        self._worker.addFrame(QueueFrame())
        self._worker.addFrame(DisconnectionHandlerFrame())
        self._worker.addFrame(CleanupCrewFrame())
        self._worker.addFrame(ChatFrame())
        self._worker.addFrame(ExternalGameFrame())
        Logger().info("Initial frames added.")

    @property
    def externalGameFrame(self) -> "ExternalGameFrame":
        return self._worker.getFrameByName("ExternalGameFrame")

    @property
    def serverSelectionFrame(self) -> "ServerSelectionFrame":
        return self._worker.getFrameByName("ServerSelectionFrame")

    @property
    def movementFrame(self) -> "RoleplayMovementFrame":
        return self._worker.getFrameByName("RoleplayMovementFrame")

    @property
    def roleplayEntitiesFrame(self) -> "RoleplayEntitiesFrame":
        return self._worker.getFrameByName("RoleplayEntitiesFrame")

    @property
    def partyFrame(self) -> "PartyFrame":
        return self._worker.getFrameByName("PartyFrame")

    @property
    def interactiveFrame(self) -> "RoleplayInteractivesFrame":
        return self._worker.getFrameByName("RoleplayInteractivesFrame")

    @property
    def worldFrame(self) -> "RoleplayWorldFrame":
        return self._worker.getFrameByName("RoleplayWorldFrame")

    @property
    def fightEntitiesFrame(self) -> "FightEntitiesFrame":
        return self._worker.getFrameByName("FightEntitiesFrame")

    @property
    def battleFrame(self) -> "FightBattleFrame":
        return self._worker.getFrameByName("FightBattleFrame")

    @property
    def turnFrame(self) -> "FightTurnFrame":
        return self._worker.getFrameByName("FightTurnFrame")

    @property
    def fightContextFrame(self) -> "FightContextFrame":
        return self._worker.getFrameByName("FightContextFrame")

    @property
    def roleplayContextFrame(self) -> "RoleplayContextFrame":
        return self._worker.getFrameByName("RoleplayContextFrame")

    @property
    def authFrame(self) -> "AuthenticationFrame":
        return self._worker.getFrameByName("AuthentificationFrame")

    @property
    def commonExchangeManagementFrame(self) -> "CommonExchangeManagementFrame":
        return self._worker.getFrameByName("CommonExchangeManagementFrame")

    @property
    def craftFrame(self):
        return self._worker.getFrameByName("CraftFrame")

    @property
    def exchangeManagementFrame(self) -> "ExchangeManagementFrame":
        return self.roleplayContextFrame._exchangeManagementFrame

    @property
    def zaapFrame(self) -> "ZaapFrame":
        return self.roleplayContextFrame._zaapFrame

    @property
    def questFrame(self) -> "QuestFrame":
        return self._worker.getFrameByName("QuestFrame")

    @property
    def marketFrame(self) -> "MarketFrame":
        return self._worker.getFrameByName("MarketFrame")

    @property
    def alignmentFrame(self) -> "AlignmentFrame":
        return self._worker.getFrameByName("AlignmentFrame")

    @property
    def chatFrame(self) -> "ChatFrame":
        return self._worker.getFrameByName("ChatFrame")

    @property
    def playedCharacterUpdatesFrame(self) -> "PlayedCharacterUpdatesFrame":
        return self._worker.getFrameByName("PlayedCharacterUpdatesFrame")

    @property
    def inventoryManagementFrame(self) -> "InventoryManagementFrame":
        return self._worker.getFrameByName("InventoryManagementFrame")

    @property
    def averagePricesFrame(self) -> "AveragePricesFrame":
        return self._worker.getFrameByName("AveragePricesFrame")

    @property
    def spellInventoryManagementFrame(self) -> "SpellInventoryManagementFrame":
        return self._worker.getFrameByName("SpellInventoryManagementFrame")

    @property
    def bidHouseManagementFrame(self) -> "BidHouseManagementFrame":
        return self._worker.getFrameByName("BidHouseManagementFrame")

    @property
    def mountFrame(self) -> "MountFrame":
        return self._worker.getFrameByName("MountFrame")

    @property
    def mountDialogFrame(self) -> "MountDialogFrame":
        return self._worker.getFrameByName("MountDialogFrame")

    @property
    def socialFrame(self) -> "SocialFrame":
        return self._worker.getFrameByName("SocialFrame")

    @property
    def guildDialogFrame(self) -> "GuildDialogFrame":
        return self._worker.getFrameByName("GuildDialogFrame")

    @property
    def gameServerApproachFrame(self) -> "GameServerApproachFrame":
        return self._worker.getFrameByName("GameServerApproachFrame")

    @property
    def characterFrame(self) -> "CharacterFrame":
        return self._worker.getFrameByName("CharacterFrame")
