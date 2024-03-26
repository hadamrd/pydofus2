from abc import ABC, abstractmethod


class GraphicalElementData(ABC):

    def __init__(self, elementId: int, elementType: int):
        self.id = elementId
        self.type = elementType

    @abstractmethod
    def fromRaw(self, raw, version: int):
        pass
