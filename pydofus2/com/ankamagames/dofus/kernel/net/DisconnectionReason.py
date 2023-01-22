class DisconnectionReason:

    def __init__(self, expected: bool, reason: int, msg: str=""):
        super().__init__()
        self._expected = expected
        self._reason = reason
        self._msg = msg

    @property
    def expected(self) -> bool:
        return self._expected

    @property
    def reason(self) -> int:
        return self._reason
    
    @property
    def message(self) -> str:
        return self._msg
    
    @property
    def exception(self) -> Exception:
        return self._exception

    def __str__(self) -> str:
        return f"DisconnectionReason(expected={self.expected}, reason={self.reason}, msg={self.message})"