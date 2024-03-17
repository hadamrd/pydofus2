from typing import Any


class PropertyChangeEvent:

    PROPERTY_CHANGED = "watchPropertyChanged"

    _watchedClassInstance: Any

    _propertyName: str

    _propertyValue: Any

    _propertyOldValue: Any

    def __init__(self, watchedClassInstance, propertyName, propertyValue, propertyOldValue):
        super().__init__()
        self._watchedClassInstance = watchedClassInstance
        self._propertyName = propertyName
        self._propertyValue = propertyValue
        self._propertyOldValue = propertyOldValue

    @property
    def watchedClassInstance(self) -> Any:
        return self._watchedClassInstance

    @property
    def propertyName(self) -> str:
        return self._propertyName

    @property
    def propertyValue(self) -> Any:
        return self._propertyValue

    @property
    def propertyOldValue(self) -> Any:
        return self._propertyOldValue
