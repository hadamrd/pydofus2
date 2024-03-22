
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion


class ItemCriterionFactory:

    def create(pServerCriterionForm: str) -> IItemCriterion:
        criterion = None
        s = pServerCriterionForm[0:2]

        if s == "BI":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.UnusableItemCriterion import UnusableItemCriterion
            criterion = UnusableItemCriterion(pServerCriterionForm)

        elif s in [
            "Ca",
            "CA",
            "ca",
            "Cc",
            "CC",
            "cc",
            "CD",
            "Ce",
            "CE",
            "CH",
            "Ci",
            "CI",
            "ci",
            "CL",
            "CM",
            "CP",
            "Cs",
            "CS",
            "cs",
            "Ct",
            "CT",
            "Cv",
            "CV",
            "cv",
            "Cw",
            "CW",
            "cw",
        ]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
            criterion = ItemCriterion(pServerCriterionForm)

        elif s == "EA":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MonsterGroupChallengeCriterion import \
    MonsterGroupChallengeCriterion
            criterion = MonsterGroupChallengeCriterion(pServerCriterionForm)

        elif s == "EB":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NumberOfMountBirthedCriterion import \
    NumberOfMountBirthedCriterion
            criterion = NumberOfMountBirthedCriterion(pServerCriterionForm)

        elif s == "Ec":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NumberOfItemMadeCriterion import \
    NumberOfItemMadeCriterion
            criterion = NumberOfItemMadeCriterion(pServerCriterionForm)

        elif s == "Eu":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.RuneByBreakingItemCriterion import \
    RuneByBreakingItemCriterion
            criterion = RuneByBreakingItemCriterion(pServerCriterionForm)

        elif s == "Kd":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaDuelRankCriterion import \
    ArenaDuelRankCriterion
            criterion = ArenaDuelRankCriterion(pServerCriterionForm)

        elif s == "KD":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaMaxDuelRankCriterion import \
                ArenaMaxDuelRankCriterion

            criterion = ArenaMaxDuelRankCriterion(pServerCriterionForm)

        elif s == "Ks":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaSoloRankCriterion import \
                ArenaSoloRankCriterion

            criterion = ArenaSoloRankCriterion(pServerCriterionForm)

        elif s == "KS":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaMaxSoloRankCriterion import \
                ArenaMaxSoloRankCriterion

            criterion = ArenaMaxSoloRankCriterion(pServerCriterionForm)

        elif s == "Kt":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaTeamRankCriterion import \
    ArenaTeamRankCriterion
            criterion = ArenaTeamRankCriterion(pServerCriterionForm)

        elif s == "KT":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaMaxTeamRankCriterion import \
    ArenaMaxTeamRankCriterion
            criterion = ArenaMaxTeamRankCriterion(pServerCriterionForm)

        elif s == "MK":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MapCharactersItemCriterion import \
    MapCharactersItemCriterion
            criterion = MapCharactersItemCriterion(pServerCriterionForm)

        elif s == "Oa":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementPointsItemCriterion import \
    AchievementPointsItemCriterion

            criterion = AchievementPointsItemCriterion(pServerCriterionForm)

        elif s == "OA":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementItemCriterion import \
    AchievementItemCriterion
            criterion = AchievementItemCriterion(pServerCriterionForm)

        elif s == "Ob":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementAccountItemCriterion import \
    AchievementAccountItemCriterion
            criterion = AchievementAccountItemCriterion(pServerCriterionForm)

        elif s == "Of":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MountFamilyItemCriterion import \
    MountFamilyItemCriterion
            criterion = MountFamilyItemCriterion(pServerCriterionForm)

        elif s == "OH":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NewHavenbagItemCriterion import \
    NewHavenbagItemCriterion

            criterion = NewHavenbagItemCriterion(pServerCriterionForm)

        elif s == "OO":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementObjectiveValidated import \
    AchievementObjectiveValidated
            criterion = AchievementObjectiveValidated(pServerCriterionForm)

        elif s == "Os":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SmileyPackItemCriterion import \
    SmileyPackItemCriterion

            criterion = SmileyPackItemCriterion(pServerCriterionForm)

        elif s == "OV":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SubscriptionDurationItemCriterion import \
    SubscriptionDurationItemCriterion
            criterion = SubscriptionDurationItemCriterion(pServerCriterionForm)

        elif s == "Ow":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AllianceItemCriterion import \
    AllianceItemCriterion
            criterion = AllianceItemCriterion(pServerCriterionForm)

        elif s == "Ox":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AllianceRightsItemCriterion import AllianceRightsItemCriterion

            criterion = AllianceRightsItemCriterion(pServerCriterionForm)

        elif s == "Oz":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AllianceAvAItemCriterion import AllianceAvAItemCriterion

            criterion = AllianceAvAItemCriterion(pServerCriterionForm)

        elif s == "Pa":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AlignmentLevelItemCriterion import \
                AlignmentLevelItemCriterion

            criterion = AlignmentLevelItemCriterion(pServerCriterionForm)

        elif s == "PA":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SoulStoneItemCriterion import \
    SoulStoneItemCriterion
            criterion = SoulStoneItemCriterion(pServerCriterionForm)

        elif s == "Pb":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.FriendlistItemCriterion import \
    FriendlistItemCriterion
            criterion = FriendlistItemCriterion(pServerCriterionForm)

        elif s == "PB":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SubareaItemCriterion import \
    SubareaItemCriterion
            criterion = SubareaItemCriterion(pServerCriterionForm)

        elif s == "Pe":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.PremiumAccountItemCriterion import \
    PremiumAccountItemCriterion
            criterion = PremiumAccountItemCriterion(pServerCriterionForm)

        elif s == "PE":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.EmoteItemCriterion import EmoteItemCriterion

            criterion = EmoteItemCriterion(pServerCriterionForm)

        elif s == "Pf":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.RideItemCriterion import RideItemCriterion

            criterion = RideItemCriterion(pServerCriterionForm)

        elif s == "Pg":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GiftItemCriterion import \
    GiftItemCriterion
            criterion = GiftItemCriterion(pServerCriterionForm)

        elif s == "PG":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.BreedItemCriterion import \
    BreedItemCriterion
            criterion = BreedItemCriterion(pServerCriterionForm)

        elif s in ["Pi", "PI"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SkillItemCriterion import \
    SkillItemCriterion

            criterion = SkillItemCriterion(pServerCriterionForm)

        elif s in ["PJ", "Pj"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.JobItemCriterion import \
    JobItemCriterion
            criterion = JobItemCriterion(pServerCriterionForm)

        elif s == "Pk":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.BonusSetItemCriterion import \
    BonusSetItemCriterion
            criterion = BonusSetItemCriterion(pServerCriterionForm)

        elif s == "PK":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.KamaItemCriterion import \
    KamaItemCriterion
            criterion = KamaItemCriterion(pServerCriterionForm)

        elif s == "PL":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.LevelItemCriterion import \
                LevelItemCriterion

            criterion = LevelItemCriterion(pServerCriterionForm)

        elif s == "Pl":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.PrestigeLevelItemCriterion import \
    PrestigeLevelItemCriterion

            criterion = PrestigeLevelItemCriterion(pServerCriterionForm)

        elif s == "Pm":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MapItemCriterion import MapItemCriterion

            criterion = MapItemCriterion(pServerCriterionForm)

        elif s == "PN":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NameItemCriterion import NameItemCriterion

            criterion = NameItemCriterion(pServerCriterionForm)

        elif s == "PO":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ObjectItemCriterion import \
    ObjectItemCriterion
            criterion = ObjectItemCriterion(pServerCriterionForm)

        elif s == "Po":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AreaItemCriterion import AreaItemCriterion

            criterion = AreaItemCriterion(pServerCriterionForm)

        elif s in ["Pp", "PP"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.PVPRankItemCriterion import PVPRankItemCriterion

            criterion = PVPRankItemCriterion(pServerCriterionForm)

        elif s == "Pr":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SpecializationItemCriterion import \
    SpecializationItemCriterion

            criterion = SpecializationItemCriterion(pServerCriterionForm)

        elif s == "PR":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MariedItemCriterion import MariedItemCriterion
            criterion = MariedItemCriterion(pServerCriterionForm)

        elif s == "Ps":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AlignmentItemCriterion import AlignmentItemCriterion

            criterion = AlignmentItemCriterion(pServerCriterionForm)

        elif s == "PS":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SexItemCriterion import SexItemCriterion
            criterion = SexItemCriterion(pServerCriterionForm)

        elif s == "PT":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SpellItemCriterion import \
    SpellItemCriterion
            criterion = SpellItemCriterion(pServerCriterionForm)

        elif s == "PU":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.BonesItemCriterion import \
    BonesItemCriterion
            criterion = BonesItemCriterion(pServerCriterionForm)

        elif s == "Pw":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GuildItemCriterion import \
    GuildItemCriterion
            criterion = GuildItemCriterion(pServerCriterionForm)

        elif s == "PW":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.WeightItemCriterion import \
    WeightItemCriterion

            criterion = WeightItemCriterion(pServerCriterionForm)

        elif s == "Px":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GuildRightsItemCriterion import GuildRightsItemCriterion
            criterion = GuildRightsItemCriterion(pServerCriterionForm)

        elif s == "PX":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AccountRightsItemCriterion import \
    AccountRightsItemCriterion
    
            criterion = AccountRightsItemCriterion(pServerCriterionForm)

        elif s == "Py":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GuildLevelItemCriterion import \
    GuildLevelItemCriterion
            criterion = GuildLevelItemCriterion(pServerCriterionForm)

        elif s in ["Pz", "PZ"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SubscribeItemCriterion import \
    SubscribeItemCriterion
            criterion = SubscribeItemCriterion(pServerCriterionForm)

        elif s in ["Qa", "Qc", "Qf"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.QuestItemCriterion import \
    QuestItemCriterion
            criterion = QuestItemCriterion(pServerCriterionForm)

        elif s == "Qo":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.QuestObjectiveItemCriterion import \
    QuestObjectiveItemCriterion
            criterion = QuestObjectiveItemCriterion(pServerCriterionForm)

        elif s == "SC":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ServerTypeItemCriterion import \
    ServerTypeItemCriterion

            criterion = ServerTypeItemCriterion(pServerCriterionForm)

        elif s == "Sc":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.StaticCriterionItemCriterion import \
    StaticCriterionItemCriterion
            criterion = StaticCriterionItemCriterion(pServerCriterionForm)

        elif s == "Sd":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.DayItemCriterion import \
    DayItemCriterion
            criterion = DayItemCriterion(pServerCriterionForm)

        elif s == "SG":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MonthItemCriterion import MonthItemCriterion

            criterion = MonthItemCriterion(pServerCriterionForm)

        elif s == "SI":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ServerItemCriterion import \
    ServerItemCriterion
            criterion = ServerItemCriterion(pServerCriterionForm)

        elif s == "ST":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ServerSeasonTemporisCriterion import \
    ServerSeasonTemporisCriterion
            criterion = ServerSeasonTemporisCriterion(pServerCriterionForm)

        elif s == "Sy":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.CommunityItemCriterion import \
    CommunityItemCriterion
            criterion = CommunityItemCriterion(pServerCriterionForm)

        else:
            # Logger().warn(f"Criterion '{s}' unknow or unused ({pServerCriterionForm})")
            pass

        return criterion