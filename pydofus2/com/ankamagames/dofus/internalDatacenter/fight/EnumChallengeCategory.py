class EnumChallengeCategory:

    FIGHT = 1
    ACHIEVEMENT_DUNGEON = 3
    ACHIEVEMENT_ANOMALY = 9
    ACHIEVEMENT_COMPANION = 11
    ACHIEVEMENT_EXPEDITION = 10
    PANDALA = 4
    TEST = 5

    @staticmethod
    def isAchievementCategoryId(id):
        return id in [
            EnumChallengeCategory.ACHIEVEMENT_DUNGEON,
            EnumChallengeCategory.ACHIEVEMENT_ANOMALY,
            EnumChallengeCategory.ACHIEVEMENT_COMPANION,
            EnumChallengeCategory.ACHIEVEMENT_EXPEDITION,
        ]
