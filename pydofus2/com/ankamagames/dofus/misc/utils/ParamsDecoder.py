import datetime

from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentSide import AlignmentSide
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemType import ItemType
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Job import Job
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Companion import Companion
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.monsters.MonsterRace import MonsterRace
from pydofus2.com.ankamagames.dofus.datacenter.monsters.MonsterSuperRace import MonsterSuperRace
from pydofus2.com.ankamagames.dofus.datacenter.quest.Achievement import Achievement
from pydofus2.com.ankamagames.dofus.datacenter.quest.Quest import Quest
from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import TimeManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class ParamsDecoder:
    @classmethod
    def applyParams(cls, txt: str, params: list, replace: str = "%") -> str:
        c = None
        lectureType = False
        lectureId = False
        type = ""
        id = ""
        s = ""
        for i in range(len(txt)):
            c = txt[i]
            if c == "$":
                lectureType = True
            elif c == replace:
                if i + 1 < len(txt) and txt[i + 1] == replace:
                    lectureId = False
                    lectureType = False
                    i += 1
                else:
                    lectureType = False
                    lectureId = True
            if lectureType:
                type += c
            elif lectureId:
                if c == replace:
                    if len(id) == 0:
                        id += c
                    else:
                        s += cls.processReplace(type, id, params)
                        type = ""
                        id = c
                elif c >= "0" and c <= "9":
                    id += c
                    if i + 1 == len(txt):
                        lectureId = False
                        s += cls.processReplace(type, id, params)
                        type = ""
                        id = ""
                else:
                    lectureId = False
                    s += cls.processReplace(type, id, params)
                    type = ""
                    id = ""
                    s += c
            else:
                if id != "":
                    s += cls.processReplace(type, id, params)
                    type = ""
                    id = ""
                s += c
        return s

    def processReplace(type: str, id: str, params: list) -> str:
        newString = ""
        if id[1:] == "" and len(params) == 0:
            return ""
        nid = int(float(id[1:])) - 1
        if type == "":
            try:
                newString = params[nid]
            except IndexError:
                return ""
        else:
            if type == "$item":
                # item = Item.getItemById(int(params[nid]))
                # if item:
                #     itemw = ItemWrapper.create(0, 0, int(params[nid]), 0, [], False)
                #     newString = HyperlinkItemManager.newChatItem(itemw)
                # else:
                #     Logger().error(f"{type} {params[nid]} introuvable")
                #     newString = ""
                newString = "item"
            elif type == "$itemType":
                itemType = ItemType.getItemTypeById(params[nid])
                if itemType:
                    newString = itemType.name
                else:
                    Logger().error(f"{type} {params[nid]} introuvable")
                    newString = ""
            elif type == "$quantity":
                newString = str(int(params[nid]))
            elif type == "$job":
                job = Job.getJobById(params[nid])
                if job:
                    newString = job.name
                else:
                    Logger().error(f"{type} {params[nid]} introuvable")
                    newString = ""
            elif type == "$quest":
                quest = Quest.getQuestById(params[nid])
                if quest:
                    newString = HyperlinkShowQuestManager.addQuest(quest.id)
                else:
                    Logger().error(f"{type} {params[nid]} introuvable")
                    newString = ""
            elif type == "$achievement":
                achievement = Achievement.getAchievementById(params[nid])
                if achievement:
                    # newString = HyperlinkShowAchievementManager.addAchievement(achievement.id)
                    newString = f"Achievement {achievement.id}"
                else:
                    Logger().error(f"{type} {params[nid]} introuvable")
                    newString = ""
            elif type == "$title":
                title = Title.getTitleById(params[nid])
                if title:
                    newString = HyperlinkShowTitleManager.addTitle(title.id)
                else:
                    Logger().error(f"{type} {params[nid]} introuvable")
                    newString = ""
            elif type == "$ornament":
                ornament = Ornament.getOrnamentById(params[nid])
                if ornament:
                    newString = HyperlinkShowOrnamentManager.addOrnament(ornament.id)
                else:
                    Logger().error(f"{type} {params[nid]} introuvable")
                    newString = ""
            if type == "$spell":
                spell = Spell.getSpellById(params[nid])
                if spell:
                    newString = spell.name
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            elif type == "$spellState":
                spellState = SpellState.getSpellStateById(params[nid])
                if spellState:
                    newString = spellState.name
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            elif type == "$breed":
                breed = Breed.getBreedById(params[nid])
                if breed:
                    newString = breed.shortName
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            elif type == "$area":
                area = Area.getAreaById(params[nid])
                if area:
                    newString = area.name
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            elif type == "$subarea":
                subArea = SubArea.getSubAreaById(params[nid])
                if subArea:
                    newString = "{subArea," + params[nid] + "}"
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            elif type == "$map":
                map = MapPosition.getMapPositionById(params[nid])
                if map:
                    if map.name:
                        newString = map.name
                    else:
                        newString = HyperlinkMapPosition.getLink(int(map.posX), int(map.posY), int(map.worldMap))
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            elif type == "$emote":
                emote = Emoticon.getEmoticonById(params[nid])
                if emote:
                    newString = emote.name
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            elif type == "$monster":
                monster = Monster.getMonsterById(params[nid])
                if monster:
                    newString = monster.name
                else:
                    Logger().error(type + " " + params[nid] + " introuvable")
                    newString = ""
            if type == "$monsterRace":
                monster_race = MonsterRace.getMonsterRaceById(params[nid])
                if monster_race:
                    newString = monster_race.name
                else:
                    print(f"{type} {params[nid]} not found")
                    newString = ""
            elif type == "$monsterSuperRace":
                monster_super_race = MonsterSuperRace.getMonsterSuperRaceById(params[nid])
                if monster_super_race:
                    newString = monster_super_race.name
                else:
                    print(f"{type} {params[nid]} not found")
                    newString = ""
            elif type == "$challenge":
                # challenge = Challenge.getChallengeById(params[nid])
                # if challenge:
                #     newString = challenge.name
                # else:
                #     print(f"{type} {params[nid]} not found")
                #     newString = ""
                return ""
            elif type == "$alignment":
                alignment_side = AlignmentSide.getAlignmentSideById(params[nid])
                if alignment_side:
                    newString = alignment_side.name
                else:
                    print(f"{type} {params[nid]} not found")
                    newString = ""
            elif type == "$stat":
                stats = I18n.getUiText("ui.item.characteristics").split(",")
                if stats[params[nid]]:
                    newString = stats[params[nid]]
                else:
                    print(f"{type} {params[nid]} not found")
                    newString = ""
            elif type == "$dungeon":
                dungeon = Dungeon.getDungeonById(params[nid])
                if dungeon:
                    newString = dungeon.name
                else:
                    print(f"{type} {params[nid]} not found")
                    newString = ""
            elif type == "$time":
                time = datetime.datetime.now()
                time_to_display = params[nid] * 1000 - int(time.timestamp())
                if time_to_display < 0:
                    time_to_display = 0
                newString = TimeManager().getDuration(time_to_display, False, True)
            elif type == "$date":
                newString = (
                    TimeManager().format_date_irl(params[nid] * 1000, True, False)
                    + " "
                    + TimeManager().format_clock(params[nid] * 1000, False, True)
                )
            elif type in ["$companion", "$sideKick"]:
                companion = Companion.getCompanionById(params[nid])
                if companion:
                    newString = companion.name
                else:
                    print(f"{type} {params[nid]} not found")
                    newString = ""
            elif type == "$breach":
                newString = (
                    I18n.getUiText("ui.breach.roomNumber", [params[nid].room])
                    + ", "
                    + I18n.getUiText("ui.breach.floor", [params[nid].floor])
                )
        return newString
