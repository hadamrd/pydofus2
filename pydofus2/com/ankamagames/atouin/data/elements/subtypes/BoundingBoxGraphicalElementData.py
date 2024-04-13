from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import (
    NormalGraphicalElementData,
)


class BoundingBoxGraphicalElementData(NormalGraphicalElementData):

    def __init__(self, elementId: int, elementType: int):
        super().__init__(elementId, elementType)
