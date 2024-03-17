from pydofus2.com.ankamagames.atouin.data.elements.GraphicalElementData import \
    GraphicalElementData
from pydofus2.com.ankamagames.atouin.data.elements.GraphicalElementTypes import \
    GraphicalElementTypes
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.AnimatedGraphicalElementData import \
    AnimatedGraphicalElementData
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.BlendedGraphicalElementData import \
    BlendedGraphicalElementData
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.BoundingBoxGraphicalElementData import \
    BoundingBoxGraphicalElementData
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.EntityGraphicalElementData import \
    EntityGraphicalElementData
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import \
    NormalGraphicalElementData
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.ParticlesGraphicalElementData import \
    ParticlesGraphicalElementData
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class GraphicalElementFactory:

    @staticmethod
    def getGraphicalElementData(elementId: int, elementType: int) -> 'GraphicalElementData':
        if elementType == GraphicalElementTypes.NORMAL:
            return NormalGraphicalElementData(elementId, elementType)
        elif elementType == GraphicalElementTypes.BOUNDING_BOX:
            return BoundingBoxGraphicalElementData(elementId, elementType)
        elif elementType == GraphicalElementTypes.ANIMATED:
            return AnimatedGraphicalElementData(elementId, elementType)
        elif elementType == GraphicalElementTypes.ENTITY:
            return EntityGraphicalElementData(elementId, elementType)
        elif elementType == GraphicalElementTypes.PARTICLES:
            return ParticlesGraphicalElementData(elementId, elementType)
        elif elementType == GraphicalElementTypes.BLENDED:
            return BlendedGraphicalElementData(elementId, elementType)
        else:
            Logger().error(f"Unknown graphical element data type {elementType} for element {elementId}!")
            return None
