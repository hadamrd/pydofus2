class PlayerDisconnectedMessage:

    def __init__(self, id, connType) -> None:
        self.instanceId = id
        self.connectionType = connType

    def __str__(self) -> str:
        return f"Disconnected({self.connectionType}:{self.instanceId})"
