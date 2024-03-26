from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.map.ILosDetector import ILosDetector
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.mapTools import MapTools


class LosDetector(ILosDetector):
    _losToMp = dict[MapPoint, dict[MapPoint, bool]]()

    @classmethod
    def losBetween(
        cls, mapProvider: IDataMapProvider, refPos: MapPoint, targetPos: MapPoint, tested: dict[str, bool] = {}
    ) -> bool:
        if targetPos in tested:
            return tested[targetPos]
        line = MapTools.getMpLine(refPos.cellId, targetPos.cellId)
        if len(line) == 0:
            los = True
        else:
            los = True
            for j in range(len(line) - 1):
                if MapPoint.isInMap(line[j].x, line[j].y):
                    if j > 0 and Kernel().fightEntitiesFrame.isEntityOnCell(line[j - 1].cellId):
                        los = False
                    elif targetPos not in tested:
                        los = los and mapProvider.pointLos(line[j].x, line[j].y, False)
                    else:
                        los = los and tested[targetPos]
                    if not los:
                        break
        tested[targetPos] = los
        return los

    @classmethod
    def getCells(cls, spellrange: list[int], refCellId: int) -> set[int]:
        from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import \
            DataMapProvider

        refMp = MapPoint.fromCellId(refCellId)
        result = set[int]()
        for cell in spellrange:
            p = MapPoint.fromCellId(cell)
            if p not in result:
                line = MapTools.getMpLine(refMp.cellId, p.cellId)
                los = True
                if len(line) > 1:
                    for mp in line[:-1]:
                        if not DataMapProvider().pointLos(mp.x, mp.y, False):
                            los = False
                            break
                if los:
                    result.add(p.cellId)
        return result

    @classmethod
    def clearCache(cls):
        cls._losToMp.clear()
