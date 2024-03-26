from pydofus2.com.ankamagames.dofus.internalDatacenter.lua.GroupMemberLuaData import \
    GroupMemberLuaData


class PlayerLuaData(GroupMemberLuaData):

    def __init__(
        self,
        pLevel: int,
        pIsStillPresentInFight: bool,
        pWisdom: int,
        pBonusMap: float,
        pBonusAlmanac: float,
        pXpBonusPercent: float,
        pIsRiding: bool,
        pRideXpBonus: float,
        pHasGuild: bool,
        pXpGuild: float,
        pSharedXPCoefficient: float,
        pUnsharedXPCoefficient: float,
    ):
        super().__init__(pLevel, False, pIsStillPresentInFight)
        self.wisdom = pWisdom
        self.bonusMap = pBonusMap
        self.bonusAlmanac = pBonusAlmanac
        self.xpBonusPercent = pXpBonusPercent
        self.isRiding = pIsRiding
        self.rideXPBonus = pRideXpBonus
        self.hasGuild = pHasGuild
        self.xpGuildGivenPercent = pXpGuild
        self.sharedXPCoefficient = pSharedXPCoefficient
        self.unsharedXPCoefficient = pUnsharedXPCoefficient

    def __str__(self):
        base_string = super().__str__()
        return f"{base_string}wisdom={self.wisdom};bonusMap={self.bonusMap};bonusAlmanach={self.bonusAlmanac};xpBonusPercent={self.xpBonusPercent};isRiding={self.isRiding};hasGuild={self.hasGuild};xpGuildGivenPercent={self.xpGuildGivenPercent};sharedXPCoefficient={self.sharedXPCoefficient};unsharedXPCoefficient={self.unsharedXPCoefficient};rideXPBonus={self.rideXPBonus};"
