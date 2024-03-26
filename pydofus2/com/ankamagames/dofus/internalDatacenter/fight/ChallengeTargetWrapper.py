class ChallengeTargetWrapper:

    targetId: float = 0

    targetCell: int = 0

    targetName: str = ""

    targetLevel: int = 1

    attackers: list[float]

    def __init__(self) -> None:
        self.attackers = list()
