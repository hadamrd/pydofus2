from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class CleanupCrewFrame(Frame):
    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.LOWEST

    def pushed(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:
        if msg.__class__.__name__ in [
            "ServerConnectionFailedMessage",
            "BasicAckMessage",
            "BasicNoOperationMessage",
            "CredentialsAcknowledgementMessage",
            "OnConnectionEventMessage",
            "ObjectJobAddedMessage",
            "AllUiXmlParsedMessage",
            "ConnectionResumedMessage",
            "GameStartingMessage",
            "BannerEmptySlotClickAction",
            "MapRenderProgressMessage",
            "GameEntitiesDispositionMessage",
            "GameFightShowFighterMessage",
            "TextureReadyMessage",
            "EntityReadyMessage",
            "MapRollOverMessage",
            "ChangeMessage",
            "SelectItemMessage",
            "MapMoveMessage",
            "TextClickMessage",
            "DropMessage",
            "MouseMiddleClickMessage",
            "MapsLoadingStartedMessage",
            "EntityMovementStartMessage",
            "MapContainerRollOverMessage",
            "MapContainerRollOutMessage",
            "GameContextDestroyMessage",
            "PlayerStatusUpdateMessage",
            "MapComplementaryInformationsDataMessage",
            "GameFightTurnReadyRequestMessage",
            "GameFightSynchronizeMessage",
            "CellClickMessage",
            "AdjacentMapClickMessage",
            "AdjacentMapOutMessage",
            "AdjacentMapOverMessage",
            "EntityMouseOverMessage",
            "InteractiveElementActivationMessage",
            "InteractiveElementMouseOverMessage",
            "InteractiveElementMouseOutMessage",
            "MouseOverMessage",
            "MouseOutMessage",
            "MouseDownMessage",
            "MouseUpMessage",
            "MouseClickMessage",
            "MouseDoubleClickMessage",
            "MouseRightClickMessage",
            "MouseRightClickOutsideMessage",
            "MouseRightDownMessage",
            "MouseRightReleaseOutsideMessage",
            "MouseRightUpMessage",
            "KeyboardKeyDownMessage",
            "KeyboardKeyUpMessage",
            "MouseRightClickOutsideMessage",
            "MouseRightClickMessage",
            "MouseReleaseOutsideMessage",
            "ItemRollOverMessage",
            "ItemRollOutMessage",
            "MouseWheelMessage",
            "CellOverMessage",
            "CellOutMessage",
            "EntityMouseOutMessage",
            "PlaySoundAction",
            "ShowEntitiesTooltipsAction",
            "SlaveSwitchContextMessage",
            "VideoBufferChangeMessage",
            "BrowserDomChange",
        ]:
            return True

        # Logger().warning(f"{msg.__class__.__name__} wasn't stopped by a frame.")
        return True

    def pulled(self) -> bool:
        return True
