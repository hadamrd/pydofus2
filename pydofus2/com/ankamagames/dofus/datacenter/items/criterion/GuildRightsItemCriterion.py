from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class GuildRightsItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        hasThisRight = False
        socialFrame: SocialFrame = Kernel().worker.getFrameByName("SocialFrame")
        if not socialFrame.hasGuild:
            if self._operator.text == ItemCriterionOperator.DIFFERENT:
                return True
            return False
        guild: GuildWrapper = socialFrame.guild
        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_BOSS:
            hasThisRight = guild.isBoss

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_BAN_MEMBERS:
            hasThisRight = guild.banMembers

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_COLLECT:
            hasThisRight = guild.collect

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_COLLECT_MY_TAX_COLLECTOR:
            hasThisRight = guild.collectMyTaxCollectors

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_DEFENSE_PRIORITY:
            hasThisRight = guild.prioritizeMeInDefense

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_HIRE_TAX_COLLECTOR:
            hasThisRight = guild.hireTaxCollector

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_INVITE_NEW_MEMBERS:
            hasThisRight = guild.inviteNewMembers

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_GUILD_BOOSTS:
            hasThisRight = guild.manageGuildBoosts

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_MY_XP_CONTRIBUTION:
            hasThisRight = guild.manageMyXpContribution

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_RANKS:
            hasThisRight = guild.manageRanks

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_RIGHTS:
            hasThisRight = guild.manageRights

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_XP_CONTRIBUTION:
            hasThisRight = guild.manageXPContribution

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_ORGANIZE_PADDOCKS:
            hasThisRight = guild.organizeFarms

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_SET_ALLIANCE_PRISM:
            hasThisRight = guild.setAlliancePrism

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_TALK_IN_ALLIANCE_CHAN:
            hasThisRight = guild.talkInAllianceChannel

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_TAKE_OTHERS_MOUNTS_IN_PADDOCKS:
            hasThisRight = guild.takeOthersRidesInFarm

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_USE_PADDOCKS:
            hasThisRight = guild.useFarms

        if self._operator.text == ItemCriterionOperator.EQUAL:
            return hasThisRight

        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            return not hasThisRight

        else:
            return False

    @property
    def text(self) -> str:
        readableCriterion: str = None
        readableCriterionValue: str = None

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_BOSS:
            readableCriterionValue = I18n.getUiText("ui.guild.right.leader")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_BAN_MEMBERS:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsBann")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_COLLECT:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsCollect")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_COLLECT_MY_TAX_COLLECTOR:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsCollectMy")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_DEFENSE_PRIORITY:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsPrioritizeMe")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_HIRE_TAX_COLLECTOR:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsHiretax")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_INVITE_NEW_MEMBERS:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsInvit")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_GUILD_BOOSTS:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsBoost")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_MY_XP_CONTRIBUTION:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightManageOwnXP")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_RANKS:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsRank")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_RIGHTS:
            readableCriterionValue = I18n.getUiText("ui.social.guildManageRights")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_MANAGE_XP_CONTRIBUTION:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsPercentXp")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_ORGANIZE_PADDOCKS:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsMountParkArrange")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_SET_ALLIANCE_PRISM:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsSetAlliancePrism")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_TALK_IN_ALLIANCE_CHAN:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsTalkInAllianceChannel")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_TAKE_OTHERS_MOUNTS_IN_PADDOCKS:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsManageOtherMount")

        if self.criterionValue == GuildRightsBitEnum.GUILD_RIGHT_USE_PADDOCKS:
            readableCriterionValue = I18n.getUiText("ui.social.guildRightsMountParkUse")

        if self._operator.text == ItemCriterionOperator.EQUAL:
            readableCriterion = I18n.getUiText("ui.criterion.guildRights", [readableCriterionValue])

        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.criterion.notGuildRights", [readableCriterionValue])
        return readableCriterion

    def clone(self) -> "IItemCriterion":
        return GuildRightsItemCriterion(self.basicText)
