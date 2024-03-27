from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import \
    EffectInstance
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class EffectZone(IDataCenter):

    id: int

    isDefaultPreviewZoneHidden: bool = False

    casterMask: str = None

    activationMask: str = None

    _activationZoneSize: int

    _activationZoneShape: int

    _activationZoneMinSize: int

    _activationZoneEfficiencyPercent: int

    _activationZoneMaxEfficiency: int

    _activationZoneStopAtTarget: int

    _displayEffect: EffectInstance = None

    _displayZoneSize: int

    _displayZoneShape: int

    _displayZoneMinSize: int

    _displayZoneEfficiencyPercent: int

    _displayZoneMaxEfficiency: int

    _displayZoneStopAtTarget: int

    def __init__(self):
        self._activationEffect = EffectInstance()
        self._rawDisplayZone: str = None
        self._rawActivationZone: str = None
        super().__init__()

    @property
    def rawDisplayZone(self) -> str:
        return self._rawDisplayZone

    @property
    def rawActivationZone(self) -> str:
        return self._rawActivationZone

    @rawDisplayZone.setter
    def rawDisplayZone(self, rawDisplayZone: str) -> None:
        self._rawDisplayZone = rawDisplayZone
        if self._rawDisplayZone is not None:
            self._displayEffect = EffectInstance()
            self._displayEffect.rawZone = rawDisplayZone
            self._displayZoneSize = self._displayEffect.zoneSize
            self._displayZoneShape = self._displayEffect.zoneShape
            self._displayZoneMinSize = self._displayEffect.zoneMinSize
            self._displayZoneEfficiencyPercent = self._displayEffect.zoneEfficiencyPercent
            self._displayZoneMaxEfficiency = self._displayEffect.zoneMaxEfficiency
            self._displayZoneStopAtTarget = self._displayEffect.zoneStopAtTarget

    @rawActivationZone.setter
    def rawActivationZone(self, rawActivationZone: str) -> None:
        self._rawActivationZone = rawActivationZone
        if self._rawActivationZone is not None:
            self._activationEffect.rawZone = self._rawActivationZone
            self._activationZoneSize = self._activationEffect.zoneSize
            self._activationZoneShape = self._activationEffect.zoneShape
            self._activationZoneMinSize = self._activationEffect.zoneMinSize
            self._activationZoneEfficiencyPercent = self._activationEffect.zoneEfficiencyPercent
            self._activationZoneMaxEfficiency = self._activationEffect.zoneMaxEfficiency
            self._activationZoneStopAtTarget = self._activationEffect.zoneStopAtTarget

    @property
    def isDisplayZone(self) -> bool:
        return self._displayEffect is not None

    @property
    def activationZoneSize(self) -> int:
        return self._activationZoneSize

    @property
    def activationZoneShape(self) -> int:
        return self._activationZoneShape

    @property
    def activationZoneMinSize(self) -> int:
        return self._activationZoneMinSize

    @property
    def activationZoneEfficiencyPercent(self) -> int:
        return self._activationZoneEfficiencyPercent

    @property
    def activationZoneMaxEfficiency(self) -> int:
        return self._activationZoneMaxEfficiency

    @property
    def activationZoneStopAtTarget(self) -> int:
        return self._activationZoneStopAtTarget

    @property
    def displayZoneSize(self) -> int:
        return self._displayZoneSize

    @property
    def displayZoneShape(self) -> int:
        return self._displayZoneShape

    @property
    def displayZoneMinSize(self) -> int:
        return self._displayZoneMinSize

    @property
    def displayZoneEfficiencyPercent(self) -> int:
        return self._displayZoneEfficiencyPercent

    @property
    def displayZoneMaxEfficiency(self) -> int:
        return self._displayZoneMaxEfficiency

    @property
    def displayZoneStopAtTarget(self) -> int:
        return self._displayZoneStopAtTarget

    @displayZoneMinSize.setter
    def displayZoneMinSize(self, displayZoneMinSize: int) -> None:
        self._displayZoneMinSize = displayZoneMinSize
