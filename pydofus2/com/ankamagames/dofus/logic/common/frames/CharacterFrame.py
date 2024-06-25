from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.actions.ChangeServerAction import ChangeServerAction
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthenticationManager import AuthenticationManager
from pydofus2.com.ankamagames.dofus.network.enums.CharacterCreationResultEnum import CharacterCreationResultEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.ReloginTokenRequestMessage import (
    ReloginTokenRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.ReloginTokenStatusMessage import (
    ReloginTokenStatusMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.creation.CharacterCreationResultMessage import (
    CharacterCreationResultMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.creation.CharacterNameSuggestionFailureMessage import (
    CharacterNameSuggestionFailureMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.creation.CharacterNameSuggestionSuccessMessage import (
    CharacterNameSuggestionSuccessMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.deletion.CharacterDeletionPrepareMessage import (
    CharacterDeletionPrepareMessage,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class CharacterFrame(Frame):
    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        self._changeToServerId = None
        return True

    def pulled(sef):
        return True

    def process(self, msg) -> bool:

        if isinstance(msg, ReloginTokenStatusMessage):
            if self._changeToServerId:
                AuthenticationManager()._lva.serverId = self._changeToServerId
                AuthenticationManager().setToken(msg.token)
                ConnectionsHandler().closeConnection(DisconnectionReasonEnum.CHANGING_SERVER)
                self._changeToServerId = None
            KernelEventsManager().send(KernelEvent.ReloginToken, msg.validToken, msg.token)
            return True

        elif isinstance(msg, CharacterCreationResultMessage):
            result = msg.result
            error_text = None
            if result > 0:
                if result == CharacterCreationResultEnum.ERR_INVALID_NAME:
                    error_text = I18n.getUiText("ui.charcrea.invalidNameReason" + str(msg.reason))
                elif result == CharacterCreationResultEnum.ERR_NOT_ALLOWED:
                    error_text = I18n.getUiText("ui.popup.charcrea.notSubscriber")
                elif result == CharacterCreationResultEnum.ERR_TOO_MANY_CHARACTERS:
                    error_text = I18n.getUiText("ui.popup.charcrea.tooManyCharacters")
                elif result == CharacterCreationResultEnum.ERR_NO_REASON:
                    error_text = I18n.getUiText("ui.popup.charcrea.noReason")
                elif result == CharacterCreationResultEnum.ERR_RESTRICTED_ZONE:
                    error_text = I18n.getUiText("ui.charSel.deletionErrorUnsecureMode")
            KernelEventsManager().send(KernelEvent.CharacterCreationResult, msg.result, msg.reason, error_text)
            return True

        elif isinstance(msg, CharacterNameSuggestionSuccessMessage):
            KernelEventsManager().send(KernelEvent.CharacterNameSuggestion, msg.suggestion)
            return True

        elif isinstance(msg, CharacterNameSuggestionFailureMessage):
            KernelEventsManager().send(KernelEvent.CharacterNameSuggestionFailed)
            return True

        elif isinstance(msg, ChangeServerAction):
            self.changeToServer(msg.serverId)
            return True

        elif isinstance(msg, CharacterDeletionPrepareMessage):
            KernelEventsManager().send(KernelEvent.CharacterDelPrepare, msg)
            return True

    def changeToServer(self, serverId):
        self._changeToServerId = serverId
        rtrccmsg = ReloginTokenRequestMessage()
        rtrccmsg.init()
        ConnectionsHandler().send(rtrccmsg)
