from typing import List, Optional


class BoundScriptUsageData:

    def __init__(self):
        self.id: int = 0
        self.scriptId: int = 0
        self.spellLevels: List[int] = []
        self.criterion: Optional[str] = None
        self.casterMask: Optional[str] = None
        self.targetMask: Optional[str] = None
        self.targetZone: Optional[str] = None
        self.activationMask: Optional[str] = None
        self.activationZone: Optional[str] = None
        self.random: int = 0
        self.randomGroup: int = 0

    def toString(self) -> str:
        return f"BoundScriptUsageData id: {self.id}, scriptId: {self.scriptId}"
