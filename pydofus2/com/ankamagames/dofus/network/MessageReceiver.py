import importlib
import json

import pydofus2.com.ankamagames.dofus.Constants as Constants
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import \
    ByteArray
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage
from pydofus2.com.ankamagames.jerakine.network.parser.ProtocolSpec import \
    ProtocolSpec
from pydofus2.com.ankamagames.jerakine.network.RawDataParser import \
    RawDataParser

with open(Constants.PROTOCOL_MSG_SHUFFLE_PATH, "r") as fp:
    msgShuffle: dict = json.load(fp)

class UnknownMessageId(Exception):
    pass

_messages_to_discard = {
    "AnomalyStateMessage",
    "AnomalyOpenedMessage",
    "ServerSettingsMessage",
    "SetCharacterRestrictionsMessage",
    "GameContextRefreshEntityLookMessage",
    "ChatServerMessage",
    "ChatServerWithObjectMessage",
    "UpdateMapPlayersAgressableStatusMessage",
    "BasicAckMessage",
    "BasicNoOperationMessage",
    "ListMapNpcsQuestStatusUpdateMessage",
    "GameMapChangeOrientationMessage",
    "HousePropertiesMessage",
    "GuildGetInformationsMessage",
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
    "EnabledChannelsMessage" "ServerSettingsMessage",
    "ServerOptionalFeaturesMessage",
    "ServerSessionConstantsMessage",
    "AccountCapabilitiesMessage",
    "GameRolePlayArenaUpdatePlayerInfosAllQueuesMessage",
    "FollowedQuestsMessage",
    "CharacterExperienceGainMessage",
    "AccountHouseMessage",
    "EnabledChannelsMessage",
    "PrismsListUpdateMessage",
    "NotificationListMessage",
    "ChallengeInfoMessage",
    "ChallengeTargetUpdateMessage",
    "ChallengeResultMessage",
    "ChallengeTargetsListMessage",
    "GameFightSpectateMessage",
    "GameFightSpectatorJoinMessage",
    "EmotePlayMessage",
    "PartyFollowStatusUpdateMessage",
    "PartyUpdateLightMessage",
    "PartyRestrictedMessage",
    "PartyLeaderUpdateMessage",
    "MapFightCountMessage",
    "PartyUpdateMessage",
    "CredentialsAcknowledgementMessage",
    "IdolFightPreparationUpdateMessage",
    "SubareaRewardRateMessage",
    "LifePointsRegenEndMessage",
    "LifePointsRegenBeginMessage",
    "TitlesAndOrnamentsListMessage",
    "GameRolePlayArenaRegistrationStatusMessage",
    "PrismAddOrUpdateMessage",
    "HavenBagPermissionsUpdateMessage",
    "HavenBagFurnituresMessage",
    "PaddockPropertiesMessage",
    "GameDataPaddockObjectListAddMessage",
    "GameRolePlayMonsterNotAngryAtPlayerMessage",
    "GameRolePlayMonsterAngryAtPlayerMessage",
    "MapFightStartPositionsUpdateMessage",
    "GameDataPaddockObjectAddMessage",
    "GameDataPlayFarmObjectAnimationMessage",
    "PrismRemoveMessage"
}

_mule_fight_messages_to_discard = {
    "GameActionFightDispellableEffectMessage",
    "GameActionUpdateEffectTriggerCountMessage",
    "GameEntitiesDispositionMessage",
    "GameFightPlacementPossiblePositionsMessage",
    "GameFightTurnListMessage",
    "SequenceEndMessage",
    "GameFightJoinMessage",
    "GameFightTurnStartMessage",
    "GameFightOptionStateUpdateMessage",
    "GameFightTurnEndMessage",
    "GameActionFightLifePointsLostMessage",
    "GameFightHumanReadyStateMessage",
    "GameFightNewRoundMessage",
    "CharacterStatsListMessage",
    "SequenceStartMessage",
    "GameFightStartMessage",
    "GameActionFightDeathMessage",
    "RefreshCharacterStatsMessage",
    "GameFightShowFighterMessage",
    "GameFightSynchronizeMessage",
    "GameActionFightPointsVariationMessage",
    "GameActionFightSpellCastMessage",
    "GameFightUpdateTeamMessage",
    "GameMapMovementMessage",
    "GameFightPlacementPossiblePositionsMessage",
    "GameFightShowFighterMessage",
    "CharacterStatsListMessage",
    "MapComplementaryInformationsDataMessage",
    "GameActionFightInvisibilityMessage",
    "GameFightRefreshFighterMessage",
    "GameActionFightDodgePointLossMessage",
    "GameActionFightLifePointsLostMessage",
    "ChatSmileyMessage",
}




class MessageReceiver(RawDataParser, metaclass=Singleton):

    def __init__(self, optimise=True):
        self.infight = False
        self.discard = optimise
        self.msgLenLen = None
        self.msgLen = None
        self.msgId = None
        self.msgCount = None
        self.messagesTypes = dict[int, type[NetworkMessage]]()
        for cls_name, cls_infos in msgShuffle.items():
            if not self.discard or cls_name not in _messages_to_discard:
                cls = self.getMessageClass(cls_infos["module"], cls_name)
                self.messagesTypes[cls_infos["id"]] = cls
        super().__init__()

    def getMessageClass(self, modulePath, clsName) -> type[NetworkMessage]:
        try:
            clsModule = globals()[modulePath]
        except:
            clsModule = importlib.import_module(modulePath)
        return getattr(clsModule, clsName)
        
    def parseMessage(self, input: ByteArray, messageId: int, messageLength: int, from_client=False, msgCount=None) -> NetworkMessage:
        if not from_client:
            messageType = self.messagesTypes.get(messageId)
        else:
            try:
                clsSpec = ProtocolSpec.getClassSpecById(messageId)
            except:
                raise UnknownMessageId(f"Message {messageId}, from client {from_client} : not found in known message Ids!")
            messageType = clsSpec.cls
        if self.discard:
            if not messageType or (
                Kernel().isMule
                and self.infight
                and messageType.__name__ in _mule_fight_messages_to_discard
            ):
                message = NetworkMessage()
                message.unpacked = False
                input.position += messageLength
                return message
        if messageType is None:
            raise UnknownMessageId(f"Message {messageId}, from client {from_client} : not found in known message Ids!")
        if messageType.__name__ == "GameFightJoinMessage":
            self.infight = True
            Logger().separator("Fight started", "+")
        elif messageType.__name__ == "GameFightEndMessage":
            self.infight = False
            Logger().separator("Fight ended", "-")
        message = messageType.unpack(input, messageLength)
        message.unpacked = True
        if from_client:
            message._instance_id = msgCount
        return message

    def parse(self, buffer: ByteArray, callback, from_client=False, from_dataContainer=False) -> None:
        while buffer.remaining():
            if self.msgLenLen is None:
                if buffer.remaining() < 2:
                    break
                staticHeader = buffer.readUnsignedShort()
                self.msgId = staticHeader >> NetworkMessage.PACKET_ID_RIGHT_SHIFT
                if from_dataContainer:
                    Logger().debug(f"Found msg with id {self.msgId} inside data container")
                self.msgLenLen = staticHeader & NetworkMessage.BIT_MASK
            if from_client and self.msgCount is None:
                if buffer.remaining() < 4:
                    break
                self.msgCount = buffer.readUnsignedInt()
            if self.msgLen is None:
                if buffer.remaining() < self.msgLenLen:
                    break
                self.msgLen = int.from_bytes(buffer.read(self.msgLenLen), "big")
            if buffer.remaining() < self.msgLen:
                break
            msg_bytes = buffer.read(self.msgLen)
            try:     
                msg = self.parseMessage(msg_bytes, self.msgId, self.msgLen, from_client, self.msgCount)
            except:
                Logger().error(f"Error while parsing message {self.msgId} from client {from_client}")
                msg = NetworkMessage()
                msg.unpacked = False
            if from_dataContainer:
                Logger().debug(f"Received {msg} from data container")
            self.msgId = None
            self.msgLenLen = None
            self.msgLen = None
            self.msgCount = None
            callback(msg, from_client)
        buffer.trim()

    def getMsgNameById(self, messageId: int) -> str:
        messageType = self.messagesTypes.get(messageId)
        if not messageType:
            Logger().warning(f"Unknown packet ID {messageId}")
            return None
        return messageType.__name__
