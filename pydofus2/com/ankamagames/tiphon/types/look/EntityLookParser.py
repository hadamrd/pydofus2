from pydofus2.com.ankamagames.tiphon.types.look.TiphonEntityLook import TiphonEntityLook


class EntityLookParser:
    DEFAULT_NUMBER_BASE = 10

    def __init__(self):
        super().__init__()

    @staticmethod
    def fromString(s: str, pNumberBase=10, tiphonInstance=None):
        el = tiphonInstance if tiphonInstance else TiphonEntityLook()
        if not s:
            return el

        with el.lock:
            numberBase = EntityLookParser.DEFAULT_NUMBER_BASE
            if s[0] == "[":
                headersStr = s[1 : s.find("]")]
                if "," in headersStr:
                    headers = headersStr.split(",")
                    if len(headers) != 2:
                        raise Exception("Malformated headers in an Entity Look string.")
                    numberBase = EntityLookParser.getNumberBase(headers[1])
                s = s[s.find("]") + 1 :]

            if s[0] != "{" or s[-1] != "}":
                raise Exception("Malformed body in an Entity Look string : " + str(s))
            s = s[1:-1]
            body = s.split("|")
            el.setBone(int(body[0], numberBase))
            if len(body) > 1 and body[1]:
                skins = body[1].split(",")
                for skin in skins:
                    el.addSkin(int(skin, numberBase))

            if len(body) > 2 and body[2]:
                colors = body[2].split(",")
                for color in colors:
                    colorPair = color.split("=")
                    if len(colorPair) != 2:
                        raise Exception("Malformed color in an Entity Look string.")
                    colorIndex = int(colorPair[0], numberBase)
                    if colorPair[1][0] == "#":
                        colorValue = int(colorPair[1][1:], 16)
                    else:
                        colorValue = int(colorPair[1], numberBase)
                    el.setColor(colorIndex, colorValue)

            if len(body) > 3 and body[3]:
                scales = body[3].split(",")
                if len(scales) == 1:
                    commonScale = int(scales[0], numberBase) / 100
                    el.setScales(commonScale, commonScale)
                elif len(scales) == 2:
                    el.setScales(int(scales[0], numberBase) / 100, int(scales[1], numberBase) / 100)
                else:
                    raise Exception("Malformed scale in an Entity Look string.")

            if len(body) > 4 and body[4]:
                subEntitiesStr = ""
                for i in range(4, len(body)):
                    subEntitiesStr += body[i] + "|"
                subEntitiesStr = subEntitiesStr[:-1]
                subEntities = list[str]()
                while True:
                    subEnd = subEntitiesStr.find("}")
                    if subEnd == -1:
                        break
                    subEntities.append(subEntitiesStr[: subEnd + 1])
                    subEntitiesStr = subEntitiesStr[subEnd + 1 :]

                for subEntity in subEntities:
                    subEntityHeader = subEntity[: subEntity.find("=")]
                    subEntityBody = subEntity[subEntity.find("=") + 1 :]
                    subEntityBinding = subEntityHeader.split("@")
                    if len(subEntityBinding) != 2:
                        raise Exception("Malformed subentity binding in an Entity Look string.")
                    bindingCategory = int(subEntityBinding[0], numberBase)
                    bindingIndex = int(subEntityBinding[1], numberBase)
                    el.addSubEntity(
                        bindingCategory, bindingIndex, EntityLookParser.fromString(subEntityBody, numberBase)
                    )
        return el

    @staticmethod
    def getNumberBase(l):
        baseMapping = {"A": 10, "G": 16, "Z": 36}
        if l in baseMapping:
            return baseMapping[l]
        else:
            raise Exception(f"Unknown number base type '{l}' in an Entity Look string.")
