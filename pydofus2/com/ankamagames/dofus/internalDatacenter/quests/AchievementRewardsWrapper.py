from pydofus2.com.ankamagames.dofus.datacenter.quest.AchievementReward import AchievementReward


class AchievementRewardsWrapper(AchievementReward):

    def __init__(self):
        super().__init__()
        self.rewardsList = []
        self.rewardTruncated = False

    @staticmethod
    def create(rewards: list[AchievementReward], id, characterRewardsTruncated=False):
        mergedRewards = AchievementRewardsWrapper()
        mergedRewards.rewardsList = rewards
        mergedRewards.rewardTruncated = characterRewardsTruncated
        mergedRewards.achievementId = id
        mergedRewards.itemsReward = []
        mergedRewards.itemsQuantityReward = []
        mergedRewards.emotesReward = []
        mergedRewards.spellsReward = []
        mergedRewards.titlesReward = []
        mergedRewards.ornamentsReward = []

        for reward in rewards:
            if reward.kamasRatio:
                mergedRewards.kamasRatio = reward.kamasRatio
                mergedRewards.kamasScaleWithPlayerLevel = reward.kamasScaleWithPlayerLevel
            if reward.experienceRatio:
                mergedRewards.experienceRatio = reward.experienceRatio
            if reward.guildPoints:
                mergedRewards.guildPoints = reward.guildPoints
            mergedRewards.itemsReward.extend(reward.itemsReward)
            mergedRewards.itemsQuantityReward.extend(reward.itemsQuantityReward)
            mergedRewards.emotesReward.extend(reward.emotesReward)
            mergedRewards.spellsReward.extend(reward.spellsReward)
            mergedRewards.titlesReward.extend(reward.titlesReward)
            mergedRewards.ornamentsReward.extend(reward.ornamentsReward)

        return mergedRewards

    def update(self, rewards: list[AchievementReward], characterRewardsTruncated=False):
        self.rewardsList = rewards
        self.rewardTruncated = characterRewardsTruncated
        if rewards and len(rewards) > 0:
            self.achievementId = rewards[0].achievementId

        self.itemsReward = []
        self.itemsQuantityReward = []
        self.emotesReward = []
        self.spellsReward = []
        self.titlesReward = []
        self.ornamentsReward = []

        for reward in rewards:
            if reward.kamasRatio:
                self.kamasRatio = reward.kamasRatio
                self.kamasScaleWithPlayerLevel = reward.kamasScaleWithPlayerLevel
            if reward.experienceRatio:
                self.experienceRatio = reward.experienceRatio
            if reward.guildPoints:
                self.guildPoints = reward.guildPoints
            self.itemsReward.extend(reward.itemsReward)
            self.itemsQuantityReward.extend(reward.itemsQuantityReward)
            self.emotesReward.extend(reward.emotesReward)
            self.spellsReward.extend(reward.spellsReward)
            self.titlesReward.extend(reward.titlesReward)
            self.ornamentsReward.extend(reward.ornamentsReward)
