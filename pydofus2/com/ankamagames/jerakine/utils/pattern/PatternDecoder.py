class PatternDecoder:

    def __init__(self):
        pass

    @classmethod
    def getDescription(cls, sText: str, aParams: list) -> str:
        return cls.decodeDescription(sText, aParams)

    @classmethod
    def combine(cls, str: str, gender: str, singular: bool, zero: bool = False) -> str:
        if not str:
            return ""
        oParams = {
            "m": gender == "m",
            "f": gender == "f",
            "n": gender == "n",
            "z": zero and "~z" in str,
            "p": not singular and not zero,
            "s": singular and not zero,
        }
        return cls.decodeCombine(str, oParams)

    @classmethod
    def decode(cls, str: str, params: dict = {}) -> str:
        if not str:
            return ""
        return cls.decodeCombine(str, params)

    def replace(self, sSrc: str, sPattern: str) -> str:
        aTmp2: list = None
        aTmp: list = sSrc.split("##")
        for i in range(len(aTmp)):
            aTmp2 = aTmp[i].split(",")
            aTmp[i] = self.getDescription(sPattern, aTmp2)
        return "".join()

    def replaceStr(self, sSrc: str, sSearchPattern: str, sReplaceStr: str) -> str:
        return sSrc.split(sSearchPattern).join(sReplaceStr)

    def findOptionnalDices(self, aStr: str, aParams: list) -> str:
        aStrCopyFirstPart: str = None
        aStrCopySecondPart: str = None
        nBlancDebut: int = 0
        nBlancFin: int = 0
        returnValue: str = aStr
        posAcc1: int = aStr.find("{")
        posAcc2: int = aStr.find("}")
        if posAcc1 >= 0 and posAcc2 > posAcc1:
            nBlancDebut = 0
            while aStr[posAcc1 - (nBlancDebut + 1)] == " ":
                nBlancDebut += 1
            nBlancFin = 0
            while aStr[posAcc2 + (nBlancFin + 1)] == " ":
                nBlancFin += 1
            aStrCopyFirstPart = aStr[0 : posAcc1 - (2 + nBlancDebut)]
            aStrCopySecondPart = aStr[
                posAcc2 - posAcc1 + 5 + nBlancFin + nBlancDebut : len(aStr) - (posAcc2 - posAcc1)
            ]
            if aStr[0] == "#" and aStr[len(aStr) - 2] == "#":
                if aParams[1] is None and aParams[2] is None and aParams[3] is None:
                    aStrCopyFirstPart += aParams[0]
                elif aParams[0] == 0 and aParams[1] == 0:
                    aStrCopyFirstPart += aParams[2]
                elif not aParams[2]:
                    aStr = (
                        aStr[0 : aStr.find("#")]
                        + aParams[0]
                        + aStr[aStr.find("{") + 5 : aStr.find("}")]
                        + aParams[1]
                        + aStr[aStr.find("#", aStr.find("}"))]
                    )
                    aStrCopyFirstPart += aStr
                else:
                    aStrCopyFirstPart += aStr
                returnValue = aStrCopyFirstPart + aStrCopySecondPart
        return returnValue

    @classmethod
    def decodeDescription(cls, aStr: str, aParams: list) -> str:
        nextSharp: int = 0
        nextTilde: int = 0
        nextBrace: int = 0
        nextBracket: int = 0
        n: float = None
        oldLength: float = None
        n1: float = None
        pos: int = 0
        rstr: str = None
        pos2: int = 0
        n2: float = None
        aStr = cls.findOptionnalDices(aStr, aParams)
        actualIndex: int = 0
        while True:
            nextSharp = aStr.find("#", actualIndex)
            nextTilde = aStr.find("~", actualIndex)
            nextBracket = aStr.find("[", actualIndex)
            if (
                nextSharp != -1
                and (nextTilde == -1 or nextSharp < nextTilde)
                and (nextBrace == -1 or nextSharp < nextBrace)
                and (nextBracket == -1 or nextSharp < nextBracket)
            ):
                n = int(aStr[nextSharp + 1])
                oldLength = len(aStr)
                if n is not None:
                    if aParams[n - 1] is not None:
                        aStr = aStr[0:nextSharp] + aParams[n - 1] + aStr[: nextSharp + 2]
                    else:
                        aStr = aStr[0:nextSharp] + aStr[: nextSharp + 2]
                actualIndex = nextSharp + len(aStr) - oldLength
            elif (
                nextTilde != -1
                and (nextBrace == -1 or nextTilde < nextBrace)
                and (nextBracket == -1 or nextTilde < nextBracket)
            ):
                n1 = int(aStr[nextTilde + 1])
                if n1 is not None:
                    break
                if aParams[n1 - 1] == None:
                    return aStr[0:nextTilde]
                aStr = aStr[0:nextTilde] + aStr[: nextTilde + 2]
                actualIndex = nextTilde
            elif nextBrace != -1 and (nextBracket == -1 or nextBrace < nextBracket):
                rstr = cls.decodeDescription(aStr[nextBrace + 1 : pos], aParams)
                aStr = aStr[0:nextBrace] + rstr + aStr[: pos + 1]
                actualIndex = nextBrace
            elif nextBracket != -1:
                pos2 = aStr.find("]", nextBracket)
                n2 = float(aStr[nextBracket + 1 : pos2])
                if n2 is not None:
                    aStr = aStr[0:nextBracket] + aParams[n2] + " " + aStr[: pos2 + 1]
                actualIndex = nextBracket
            if not (nextSharp != -1 or nextTilde != -1 or nextBrace != -1 or nextBracket != -1):
                return aStr
        if len(aParams) > 5:
            return cls.combine(aStr, aParams[5], aParams[6], aParams[7])
        return ""

    @classmethod
    def decodeCombine(cls, aStr: str, oParams: dict) -> str:
        nextTilde: int = 0
        nextBrace: int = 0
        key: str = None
        pos: int = 0
        content: str = None
        twoDotsPos: int = 0
        rstr: str = None
        actualIndex: int = 0
        while True:
            nextTilde = aStr.find("~", actualIndex)
            nextBrace = aStr.find("{", actualIndex)
            if nextTilde != -1 and (nextBrace == -1 or nextTilde < nextBrace):
                key = aStr[nextTilde + 1]
                if not oParams[key]:
                    break
                aStr = aStr[0:nextTilde] + aStr[: nextTilde + 2]
                actualIndex = nextTilde
            elif nextBrace != -1:
                content = aStr[nextBrace + 1 : pos]
                twoDotsPos = -1
                if pos > -1:
                    twoDotsPos = content.find(":")
                if (
                    twoDotsPos == -1 or twoDotsPos + 1 > len(content) or content[twoDotsPos + 1] != ":"
                ) and "~" in content:
                    rstr = cls.decodeCombine(content, oParams)
                    if content != rstr:
                        aStr = aStr[0:nextBrace] + rstr + aStr[: pos + 1]
                    actualIndex = nextBrace
                else:
                    actualIndex = pos
            if not (nextTilde != -1 or nextBrace != -1):
                return aStr
        return aStr[0:nextTilde]
