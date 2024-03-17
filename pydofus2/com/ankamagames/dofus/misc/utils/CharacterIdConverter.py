class CharacterIdConverter:
    @staticmethod
    def extractServerCharacterIdFromInterserverCharacterId(interserverCharacterId):
        if interserverCharacterId:
            return interserverCharacterId // 65536
        return 0