from pydofus2.com.ankamagames.jerakine.messages.Message import Message

class ConnectionProcessCrashedMessage(Message):
    def __init__(self, err):
        super().__init__()
        self.err = err

    def __str__(self):
        return f"ConnectionProcessCrashedMessage(err={self.err})"