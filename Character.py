from dataclasses import dataclass, field
from enum import Enum, IntEnum

class Ability(Enum):
    STR = "strength"
    DEX = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHA = "charisma"

class ProficiencyRank(IntEnum):
    Untrained = 0
    Trained = 2
    Expert = 4
    Master = 6
    Legendary = 8

    def bonus(self,level: int)->int:
        if self == ProficiencyRank.Untrained:
            return 0
        return level + self.value

class Skill(Enum):
    ACROBATICS = ("acrobatics", Ability.DEX)
    ARCANA = ("arcana", Ability.INT)
    ATHLETICS = ("athletics", Ability.STR)
    CRAFTING = ("crafting", Ability.INT)
    DECEPTION = ("deception", Ability.CHA)
    DIPLOMACY = ("diplomacy", Ability.CHA)
    INTIMIDATION = ("intimidation", Ability.CHA)
    MEDICINE = ("medicine", Ability.WIS)
    NATURE = ("nature", Ability.WIS)
    OCCULTISM = ("occultism", Ability.INT)
    PERFORMANCE = ("performance", Ability.CHA)
    RELIGION = ("religion", Ability.WIS)
    SOCIETY = ("society", Ability.INT)
    STEALTH = ("stealth", Ability.DEX)
    SURVIVAL = ("survival", Ability.WIS)
    THIEVERY = ("thievery", Ability.DEX)

    def __init__(self, label: str, key_ability: Ability):
        self.label = label
        self.key_ability = key_ability

@dataclass
class Character:
    name: str
    level: int = 1
    #Sets the abilities to default(0)
    abilities: dict[Ability, int] = field(
        default_factory=lambda: {a: 0 for a in Ability}
    )
    #Sets the skill proficiencies to default(Untrained)
    proficiencies: dict[Skill, ProficiencyRank] = field(
        default_factory=lambda: {s: ProficiencyRank.Untrained for s in Skill}
    )
    #Increases the given Ability by 2 if < 8 else increases by 1
    def boost(self,ability: Ability) -> None:
        if self.abilities[ability] < 8:
            self.abilities[ability] += 2
        else:
            self.abilities[ability] += 1
    #Since PF2E uses modifiers, we divide our ability score by 2 to bring us back to where we need
    #to be in line with the rules. This doubling and dividing prevents half points.
    def modifier(self,ability: Ability) -> int:
        return self.abilities[ability] // 2
    #returns the sum of the Ability modifier and the Proficiency modifier
    def skill_bonus(self, skill: Skill) -> int:
        ability_mod = self.modifier(skill.key_ability)
        rank = self.proficiencies[skill]
        return ability_mod + rank.bonus(self.level)