
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class ItemCriterionFactory:

    def create(pServerCriterionForm: str) -> IItemCriterion:
        criterion = None
        s = pServerCriterionForm[0:2]

        if s == "BI":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.UnusableItemCriterion import \
                ItemCriterion
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
                erion
            criterion = ItemCriterion(pServerCriterionForm)

        elif s == "EA":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MonsterGroupChallengeCriterion import \
                roupChallengeCriterion
            criterion = MonsterGroupChallengeCriterion(pServerCriterionForm)

        elif s == "EB":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NumberOfMountBirthedCriterion import \
                MountBirthedCriterion
            criterion = NumberOfMountBirthedCriterion(pServerCriterionForm)

        elif s == "Ec":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NumberOfItemMadeCriterion import \
                ItemMadeCriterion
            criterion = NumberOfItemMadeCriterion(pServerCriterionForm)

        elif s == "Eu":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.RuneByBreakingItemCriterion import \
                eakingItemCriterion
            criterion = RuneByBreakingItemCriterion(pServerCriterionForm)

        elif s == "Kd":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaDuelRankCriterion import \
                lRankCriterion
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
                mRankCriterion
            criterion = ArenaTeamRankCriterion(pServerCriterionForm)

        elif s == "KT":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ArenaMaxTeamRankCriterion import \
                TeamRankCriterion
            criterion = ArenaMaxTeamRankCriterion(pServerCriterionForm)

        elif s == "MK":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MapCharactersItemCriterion import \
                ctersItemCriterion
            criterion = MapCharactersItemCriterion(pServerCriterionForm)

        elif s == "Oa":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementPointsItemCriterion import \
                entPointsItemCriterion

            criterion = AchievementPointsItemCriterion(pServerCriterionForm)

        elif s == "OA":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementItemCriterion import \
                entItemCriterion
            criterion = AchievementItemCriterion(pServerCriterionForm)

        elif s == "Ob":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementAccountItemCriterion import \
                entAccountItemCriterion
            criterion = AchievementAccountItemCriterion(pServerCriterionForm)

        elif s == "Of":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MountFamilyItemCriterion import \
                ilyItemCriterion
            criterion = MountFamilyItemCriterion(pServerCriterionForm)

        elif s == "OH":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NewHavenbagItemCriterion import \
                bagItemCriterion

            criterion = NewHavenbagItemCriterion(pServerCriterionForm)

        elif s == "OO":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AchievementObjectiveValidated import \
                entObjectiveValidated
            criterion = AchievementObjectiveValidated(pServerCriterionForm)

        elif s == "Os":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SmileyPackItemCriterion import \
                ckItemCriterion

            criterion = SmileyPackItemCriterion(pServerCriterionForm)

        elif s == "OV":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SubscriptionDurationItemCriterion import \
                tionDurationItemCriterion
            criterion = SubscriptionDurationItemCriterion(pServerCriterionForm)

        elif s == "Ow":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AllianceItemCriterion import \
                ItemCriterion
            criterion = AllianceItemCriterion(pServerCriterionForm)

        elif s == "Ox":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AllianceRightsItemCriterion import \
                AllianceRightsItemCriterion

            criterion = AllianceRightsItemCriterion(pServerCriterionForm)

        elif s == "Oz":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AllianceAvAItemCriterion import \
                AllianceAvAItemCriterion

            criterion = AllianceAvAItemCriterion(pServerCriterionForm)

        elif s == "Pa":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AlignmentLevelItemCriterion import \
                AlignmentLevelItemCriterion

            criterion = AlignmentLevelItemCriterion(pServerCriterionForm)

        elif s == "PA":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SoulStoneItemCriterion import \
                eItemCriterion
            criterion = SoulStoneItemCriterion(pServerCriterionForm)

        elif s == "Pb":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.FriendlistItemCriterion import \
                stItemCriterion
            criterion = FriendlistItemCriterion(pServerCriterionForm)

        elif s == "PB":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SubareaItemCriterion import \
                temCriterion
            criterion = SubareaItemCriterion(pServerCriterionForm)

        elif s == "Pe":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.PremiumAccountItemCriterion import \
                ccountItemCriterion
            criterion = PremiumAccountItemCriterion(pServerCriterionForm)

        elif s == "PE":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.EmoteItemCriterion import \
                EmoteItemCriterion

            criterion = EmoteItemCriterion(pServerCriterionForm)

        elif s == "Pf":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.RideItemCriterion import \
                RideItemCriterion

            criterion = RideItemCriterion(pServerCriterionForm)

        elif s == "Pg":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GiftItemCriterion import \
                Criterion
            criterion = GiftItemCriterion(pServerCriterionForm)

        elif s == "PG":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.BreedItemCriterion import \
                mCriterion
            criterion = BreedItemCriterion(pServerCriterionForm)

        elif s in ["Pi", "PI"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SkillItemCriterion import \
                mCriterion

            criterion = SkillItemCriterion(pServerCriterionForm)

        elif s in ["PJ", "Pj"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.JobItemCriterion import \
                riterion
            criterion = JobItemCriterion(pServerCriterionForm)

        elif s == "Pk":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.BonusSetItemCriterion import \
                ItemCriterion
            criterion = BonusSetItemCriterion(pServerCriterionForm)

        elif s == "PK":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.KamaItemCriterion import \
                Criterion
            criterion = KamaItemCriterion(pServerCriterionForm)

        elif s == "PL":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.LevelItemCriterion import \
                LevelItemCriterion

            criterion = LevelItemCriterion(pServerCriterionForm)

        elif s == "Pl":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.PrestigeLevelItemCriterion import \
                LevelItemCriterion

            criterion = PrestigeLevelItemCriterion(pServerCriterionForm)

        elif s == "Pm":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MapItemCriterion import \
                MapItemCriterion

            criterion = MapItemCriterion(pServerCriterionForm)

        elif s == "PN":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.NameItemCriterion import \
                NameItemCriterion

            criterion = NameItemCriterion(pServerCriterionForm)

        elif s == "PO":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ObjectItemCriterion import \
                emCriterion
            criterion = ObjectItemCriterion(pServerCriterionForm)

        elif s == "Po":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AreaItemCriterion import \
                AreaItemCriterion

            criterion = AreaItemCriterion(pServerCriterionForm)

        elif s in ["Pp", "PP"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.PVPRankItemCriterion import \
                PVPRankItemCriterion

            criterion = PVPRankItemCriterion(pServerCriterionForm)

        elif s == "Pr":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SpecializationItemCriterion import \
                zationItemCriterion

            criterion = SpecializationItemCriterion(pServerCriterionForm)

        elif s == "PR":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MariedItemCriterion import \
                MariedItemCriterion
            criterion = MariedItemCriterion(pServerCriterionForm)

        elif s == "Ps":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AlignmentItemCriterion import \
                AlignmentItemCriterion

            criterion = AlignmentItemCriterion(pServerCriterionForm)

        elif s == "PS":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SexItemCriterion import \
                SexItemCriterion
            criterion = SexItemCriterion(pServerCriterionForm)

        elif s == "PT":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SpellItemCriterion import \
                mCriterion
            criterion = SpellItemCriterion(pServerCriterionForm)

        elif s == "PU":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.BonesItemCriterion import \
                mCriterion
            criterion = BonesItemCriterion(pServerCriterionForm)

        elif s == "Pw":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GuildItemCriterion import \
                mCriterion
            criterion = GuildItemCriterion(pServerCriterionForm)

        elif s == "PW":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.WeightItemCriterion import \
                emCriterion

            criterion = WeightItemCriterion(pServerCriterionForm)

        elif s == "Px":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GuildRightsItemCriterion import \
                GuildRightsItemCriterion
            criterion = GuildRightsItemCriterion(pServerCriterionForm)

        elif s == "PX":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.AccountRightsItemCriterion import \
                ightsItemCriterion
    
            criterion = AccountRightsItemCriterion(pServerCriterionForm)

        elif s == "Py":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GuildLevelItemCriterion import \
                elItemCriterion
            criterion = GuildLevelItemCriterion(pServerCriterionForm)

        elif s in ["Pz", "PZ"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.SubscribeItemCriterion import \
                eItemCriterion
            criterion = SubscribeItemCriterion(pServerCriterionForm)

        elif s in ["Qa", "Qc", "Qf"]:
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.QuestItemCriterion import \
                mCriterion
            criterion = QuestItemCriterion(pServerCriterionForm)

        elif s == "Qo":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.QuestObjectiveItemCriterion import \
                ectiveItemCriterion
            criterion = QuestObjectiveItemCriterion(pServerCriterionForm)

        elif s == "SC":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ServerTypeItemCriterion import \
                peItemCriterion

            criterion = ServerTypeItemCriterion(pServerCriterionForm)

        elif s == "Sc":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.StaticCriterionItemCriterion import \
                iterionItemCriterion
            criterion = StaticCriterionItemCriterion(pServerCriterionForm)

        elif s == "Sd":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.DayItemCriterion import \
                riterion
            criterion = DayItemCriterion(pServerCriterionForm)

        elif s == "SG":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.MonthItemCriterion import \
                MonthItemCriterion

            criterion = MonthItemCriterion(pServerCriterionForm)

        elif s == "SI":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ServerItemCriterion import \
                emCriterion
            criterion = ServerItemCriterion(pServerCriterionForm)

        elif s == "ST":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ServerSeasonTemporisCriterion import \
                asonTemporisCriterion
            criterion = ServerSeasonTemporisCriterion(pServerCriterionForm)

        elif s == "Sy":
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.CommunityItemCriterion import \
                yItemCriterion
            criterion = CommunityItemCriterion(pServerCriterionForm)

        else:
            # Logger().warn(f"Criterion '{s}' unknow or unused ({pServerCriterionForm})")
            pass

        return criterion
