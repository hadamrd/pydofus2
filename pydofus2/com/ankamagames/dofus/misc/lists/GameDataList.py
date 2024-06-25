from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentGift import AlignmentGift
from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentOrder import AlignmentOrder
from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentRank import AlignmentRank
from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentRankJntGift import AlignmentRankJntGift
from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentSide import AlignmentSide
from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentTitle import AlignmentTitle
from pydofus2.com.ankamagames.dofus.datacenter.effects.Effect import Effect
from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.items.EvolutiveItemType import EvolutiveItemType
from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemSet import ItemSet
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemType import ItemType
from pydofus2.com.ankamagames.dofus.datacenter.items.Weapon import Weapon
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Job import Job
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.monsters.MonsterDrop import MonsterDrop
from pydofus2.com.ankamagames.dofus.datacenter.monsters.MonsterGrade import MonsterGrade
from pydofus2.com.ankamagames.dofus.datacenter.monsters.MonsterRace import MonsterRace
from pydofus2.com.ankamagames.dofus.datacenter.monsters.MonsterSuperRace import MonsterSuperRace
from pydofus2.com.ankamagames.dofus.datacenter.servers.Server import Server
from pydofus2.com.ankamagames.dofus.datacenter.servers.ServerCommunity import ServerCommunity
from pydofus2.com.ankamagames.dofus.datacenter.servers.ServerGameType import ServerGameType
from pydofus2.com.ankamagames.dofus.datacenter.servers.ServerPopulation import ServerPopulation
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellState import SpellState
from pydofus2.com.ankamagames.dofus.datacenter.world.Area import Area
from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.dofus.datacenter.world.MapScrollAction import MapScrollAction
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.datacenter.world.SuperArea import SuperArea
from pydofus2.com.ankamagames.dofus.datacenter.world.WorldMap import WorldMap


class GameDataList:

    CLASSES: list[object] = [
        Server,
        ServerCommunity,
        ServerGameType,
        ServerPopulation,
        Monster,
        MonsterGrade,
        MonsterRace,
        MonsterSuperRace,
        MonsterDrop,
        Effect,
        EffectInstance,
        SpellState,
        SuperArea,
        Area,
        WorldMap,
        SubArea,
        MapPosition,
        MapScrollAction,
        Item,
        Weapon,
        Job,
        ItemSet,
        AlignmentGift,
        AlignmentOrder,
        AlignmentRank,
        AlignmentRankJntGift,
        AlignmentSide,
        AlignmentTitle,
        ItemType,
        EvolutiveItemType,
    ]

    def __init__(self):
        super().__init__()
