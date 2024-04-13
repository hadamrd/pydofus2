from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action
from pydofus2.com.ankamagames.jerakine.messages.IDontLogThisMessage import IDontLogThisMessage


class LoginValidationAction(AbstractAction, Action, IDontLogThisMessage):

    username: str

    password: str

    autoSelectServer: bool

    serverId: int

    host: str

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(
        cls, username: str, password: str, autoSelectServer: bool, serverId: int = 0, host: str = None, *args
    ) -> "LoginValidationAction":
        a: LoginValidationAction = LoginValidationAction(args)
        a.password = password
        a.username = username
        a.autoSelectServer = autoSelectServer
        a.serverId = serverId
        a.host = host
        return a
