import re


class StringUtils:
    accents: str = "ŠŒŽšœžÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜŸÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýÿþ"
    pattern = None

    def fill(str: str, len: int, char: str, before: bool = True) -> str:
        if not char or not len(char):
            return str
        while len(str) != len:
            if before:
                str = char + str
            else:
                str += char
        return str

    def initPatterns():
        StringUtils.pattern = {
            "Š": "S",
            "Œ": "Oe",
            "Ž": "Z",
            "š": "s",
            "œ": "oe",
            "ž": "z",
            "À": "A",
            "Á": "A",
            "Â": "A",
            "Ã": "A",
            "Ä": "A",
            "Å": "A",
            "Æ": "Ae",
            "Ç": "C",
            "È": "E",
            "É": "E",
            "Ê": "E",
            "Ë": "E",
            "Ì": "I",
            "Í": "I",
            "Î": "I",
            "Ï": "I",
            "Ð": "D",
            "Ñ": "N",
            "Ò": "O",
            "Ó": "O",
            "Ô": "O",
            "Õ": "O",
            "Ö": "O",
            "Ø": "O",
            "Ù": "U",
            "Ú": "U",
            "Û": "U",
            "Ü": "U",
            "Ÿ": "Y",
            "Ý": "Y",
            "Þ": "Th",
            "ß": "ss",
            "à": "a",
            "á": "a",
            "â": "a",
            "ã": "a",
            "ä": "a",
            "å": "a",
            "æ": "ae",
            "ç": "c",
            "è": "e",
            "é": "e",
            "ê": "e",
            "ë": "e",
            "ì": "i",
            "í": "i",
            "î": "i",
            "ï": "i",
            "ð": "d",
            "ñ": "n",
            "ò": "o",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ö": "o",
            "ø": "o",
            "ù": "u",
            "ú": "u",
            "û": "u",
            "ü": "u",
            "ý": "y",
            "ÿ": "y",
            "þ": "th",
        }

    def concatSamestr(pstr: str, pstrToConcat: str) -> str:
        firstIndex: int = pstr.find(pstrToConcat)
        previousIndex: int = 0
        currentIndex: int = firstIndex
        while currentIndex != -1:
            previousIndex = currentIndex
            currentIndex = pstr.find(pstrToConcat, previousIndex + 1)
            if currentIndex == firstIndex:
                break
            if currentIndex == previousIndex + len(pstrToConcat):
                pstr = pstr[0:currentIndex] + pstr[currentIndex + len(pstrToConcat) :]
                currentIndex -= len(pstrToConcat)
        return pstr

    def noAccent(src: str) -> str:
        if StringUtils.pattern is None:
            StringUtils.initPatterns()
        return StringUtils.decomposeUnicode(src)

    def decomposeUnicode(src: str) -> str:
        toCheck: str = src if len(StringUtils.accents) < len(src) else StringUtils.accents
        toLoop: str = StringUtils.accents if len(StringUtils.accents) < len(src) else src
        for c in toLoop:
            if c in toCheck:
                src = re.sub(c, StringUtils.pattern[c], src)
        return src

    def getDelimitedText(pText, pFirstDelimiter, pSecondDelimiter, pIncludeDelimiter=False):
        returnedArray = []
        text = pText

        while True:
            delimitedText = StringUtils.getSingleDelimitedText(
                text, pFirstDelimiter, pSecondDelimiter, pIncludeDelimiter
            )
            if delimitedText == "":
                break
            else:
                returnedArray.append(delimitedText)

                if not pIncludeDelimiter:
                    delimitedText = pFirstDelimiter + delimitedText + pSecondDelimiter

                firstPartIndex = text.find(delimitedText)
                firstPart = text[:firstPartIndex]
                secondPart = text[firstPartIndex + len(delimitedText) :]

                # Replace occurrences of the first delimiter in the first part
                firstPart = firstPart.replace(pFirstDelimiter, "")
                text = firstPart + secondPart

        return returnedArray

    def getSingleDelimitedText(pStringEntry, pFirstDelimiter, pSecondDelimiter, pIncludeDelimiter=False):
        firstDelimiterIndex = pStringEntry.find(pFirstDelimiter)
        if firstDelimiterIndex == -1:
            return ""

        delimiterDepth = 1  # Start with a depth of 1 for the first found delimiter
        currentIndex = firstDelimiterIndex + len(pFirstDelimiter)
        delimitedContent = ""

        while currentIndex < len(pStringEntry) and delimiterDepth > 0:
            nextFirstDelimiterIndex = pStringEntry.find(pFirstDelimiter, currentIndex)
            nextSecondDelimiterIndex = pStringEntry.find(pSecondDelimiter, currentIndex)

            if nextSecondDelimiterIndex == -1:
                break  # No closing delimiter found

            if nextFirstDelimiterIndex != -1 and nextFirstDelimiterIndex < nextSecondDelimiterIndex:
                # Found another opening delimiter before the closing one
                delimiterDepth += 1
                currentIndex = nextFirstDelimiterIndex + len(pFirstDelimiter)
            else:
                # Found a closing delimiter
                delimiterDepth -= 1
                if delimiterDepth == 0:
                    # Found the matching closing delimiter
                    delimitedContent = pStringEntry[
                        firstDelimiterIndex : nextSecondDelimiterIndex + len(pSecondDelimiter)
                    ]
                else:
                    currentIndex = nextSecondDelimiterIndex + len(pSecondDelimiter)

        if delimitedContent and not pIncludeDelimiter:
            delimitedContent = delimitedContent[len(pFirstDelimiter) : len(delimitedContent) - len(pSecondDelimiter)]

        return delimitedContent

    def getAllIndexOf(pStringLookFor, pWholeString):
        nextIndex = 0
        returnedArray = []
        currentIndex = 0

        while True:
            nextIndex = pWholeString.find(pStringLookFor, currentIndex)
            if nextIndex < currentIndex:
                break
            else:
                returnedArray.append(nextIndex)
                currentIndex = nextIndex + len(pStringLookFor)

        return returnedArray

    def getAllIndexOf(pStringLookFor: str, pWholeString: str) -> list:
        index = pWholeString.find(pStringLookFor)
        indices = []
        while index != -1:
            indices.append(index)
            index = pWholeString.find(pStringLookFor, index + 1)
        return indices


if __name__ == "__main__":

    def testGetDelimitedText():
        string = "(((Qa=1940&Qo>13584)|Qf=1940)&PO>9935,0)"
        res = StringUtils.getDelimitedText(string, "(", ")")
        print(res)

    def testGetAllIndexOf():
        test_cases = [
            ("test", "this is a test string with test cases"),
            ("a", "banana"),
            ("xyz", "this has no match"),
            (" ", "spaces should be counted too"),
        ]

        for substring, string in test_cases:
            result = StringUtils.getAllIndexOf(substring, string)
            print(f"Indices of '{substring}' in '{string}': {result}")

    def testGetSingleDelimitedText():
        # Updated Test Cases
        test_cases = [
            ("Hello [World]!", "[", "]", False, "World"),
            ("Hello [World]!", "[", "]", True, "[World]"),
            ("[Start] and [End]", "[", "]", False, "Start"),
            ("No delimiters here", "{", "}", False, ""),
            ("Empty delimiters []", "[", "]", False, ""),
            ("Nested [delimiters [like] this]", "[", "]", False, "delimiters [like] this"),
            (
                "Deeply [nested [delimiters [like] this] example]",
                "[",
                "]",
                False,
                "nested [delimiters [like] this] example",
            ),
            ("Mismatched delimiters", "[", "}", False, ""),
            ("Delimiters at [the] start", "[", "]", False, "the"),
            ("Delimiters at the end [of]", "[", "]", False, "of"),
            ("[Multiple] [delimiters] in [one] string", "[", "]", False, "Multiple"),
            ("Special characters <|like|> these", "<|", "|>", False, "like"),
            ("Escaped delimiters \\[not\\] a match", "\\[", "\\]", False, "not"),
            ("Unbalanced [delimiters [like this", "[", "]", False, ""),
            ("Unbalanced delimiters like] this]", "[", "]", False, ""),
            ("Delimiters in [reverse] order]", "[", "]", False, "reverse"),
            ("Empty string", "[", "]", False, ""),
            ("Only delimiters []", "[]", "[]", False, ""),
            ("Same opening and closing delimiter [[content[[", "[", "[", False, "content"),
            ("Multiple same delimiters %%first%% and %%second%%", "%", "%", False, "first"),
            ("Overlapping delimiters [[[nested]]]", "[", "]", False, "[nested"),
        ]

        # Running the tests
        for text, start_delim, end_delim, include_delim, expected in test_cases:
            result = StringUtils.getSingleDelimitedText(text, start_delim, end_delim, include_delim)
            assert result == expected, f"Test failed for '{text}'. Expected: '{expected}', Got: '{result}'"
            print(f"Test passed for '{text}'. Result: '{result}'")

    dtxt = "(((Qo>3613&PO<11044,1&Qo<3597)|(Qo>3617&Qo<3600))&CE>0)"
    r = StringUtils.getSingleDelimitedText(dtxt, "(", ")")
    print(r)
