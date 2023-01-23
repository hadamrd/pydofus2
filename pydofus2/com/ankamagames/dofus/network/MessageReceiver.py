import importlib
import json
import sys
from types import FunctionType
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from pydofus2.com.ankamagames.jerakine.network.RawDataParser import RawDataParser
from pydofus2.com.ankamagames.jerakine.network.UnpackMode import UnpackMode
import pydofus2.com.ankamagames.dofus.Constants as Constants

logger = Logger("Dofus2")
with open(Constants.PROTOCOL_MSG_SHUFFLE_PATH, "r") as fp:
    msgShuffle = json.load(fp)


class MessageReceiver(RawDataParser):
    logger = Logger("Dofus2")
    _messagesTypes = dict[int, type[NetworkMessage]]()
    _unpackModes: dict = dict()
    _messages_to_discard: set = {
        "SetCharacterRestrictionsMessage", 
        "GameContextRefreshEntityLookMessage", 
        "ChatServerMessage", 
        "ChatServerWithObjectMessage",
        "UpdateMapPlayersAgressableStatusMessage",
        "GameContextRemoveElementMessage",
        "BasicAckMessage",
        "BasicNoOperationMessage",
        "ListMapNpcsQuestStatusUpdateMessage",
        "GameMapChangeOrientationMessage",
        "HousePropertiesMessage",
        "KnownZaapListMessage"
        "GuildGetInformationsMessage",
        "KnownZaapListMessage",
        "PrismsListMessage",
        "ChatCommunityChannelCommunityMessage",
        "FriendWarnOnConnectionStateMessage",
        "FriendWarnOnLevelGainStateMessage",
        "FriendGuildWarnOnAchievementCompleteStateMessage",
        "WarnOnPermaDeathStateMessage",
        "FriendStatusShareStateMessage",
        "GuildMemberWarnOnConnectionStateMessage",
        "ServerExperienceModificatorMessage",
        "SpouseStatusMessage",
        "IdolListMessage",
        "AlmanachCalendarDateMessage",
        "CharacterCapabilitiesMessage",
        "ShortcutBarContentMessage",
        "AlterationsMessage",
        "HavenBagRoomUpdateMessage",
        "HavenBagPackListMessage",
        "StartupActionsListMessage",
        "EmoteListMessage",
        "JobCrafterDirectorySettingsMessage",
        "EnabledChannelsMessage"
        "ServerSettingsMessage",
        "ServerOptionalFeaturesMessage",
        "ServerSessionConstantsMessage",
        "AccountCapabilitiesMessage",
        "AlignmentRankUpdateMessage",
        "GameRolePlayArenaUpdatePlayerInfosAllQueuesMessage",
        "FollowedQuestsMessage",
        "CharacterExperienceGainMessage",
        "AccountHouseMessage",
        "EnabledChannelsMessage",
        "PrismsListUpdateMessage",
        "TrustStatusMessage"
    }
    for cls_name, cls_infos in msgShuffle.items():
        modulePath = cls_infos["module"]
        try:
            clsModule = sys.modules[modulePath]
        except:
            clsModule = importlib.import_module(modulePath)
        cls = getattr(clsModule, cls_name)
        _messagesTypes[cls_infos["id"]] = cls
    _unpackModes[2180] = UnpackMode.ASYNC

    def __init__(self):
        super().__init__()

    def register(self) -> None:
        for cls in self._messagesTypes.values():
            StoreDataManager().registerClass(cls(), True, True)

    def parse(self, input: ByteArray, messageId: int, messageLength: int) -> INetworkMessage:
        messageType = self._messagesTypes.get(messageId)
        if not messageType:
            logger.warn(f"Unknown packet ID {messageId}")
            return None
        if messageType.__qualname__ in self._messages_to_discard:
            message = messageType()
            message.unpacked = False
            input.position += messageLength
            return message
        message = messageType.unpack(input, messageLength)
        message.unpacked = True
        return message

    def parseAsync(
        self,
        input: ByteArray,
        messageId: int,
        messageLength: int,
        callback: FunctionType,
    ) -> INetworkMessage:
        messageType = self._messagesTypes.get(messageId)
        if not messageType:
            logger.warn("Unknown packet received (ID " + messageId + ", length " + messageLength + ")")
            return None
        message: INetworkMessage = messageType()
        message.unpacked = False
        callback(message, message.unpackAsync(input, messageLength))
        return message

    def getUnpackMode(self, messageId: int) -> int:
        return self._unpackModes[messageId] if messageId in self._unpackModes else UnpackMode.DEFAULT

    @classmethod
    def getMsgNameById(cls, messageId: int) -> str:
        messageType = cls._messagesTypes.get(messageId)
        if not messageType:
            raise Exception(f"Unknown packet ID {messageId}")
        return messageType.__name__