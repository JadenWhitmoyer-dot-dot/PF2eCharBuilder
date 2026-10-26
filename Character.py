from dataclasses import dataclass, field
from enum import Enum, IntEnum

class Ability(Enum):
    STR = "strength"
    DEF = "dexterity"
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


@dataclass
class Character:
    name: str
    level: int = 1
    # PF2e uses modifiers not raw stats: a base human is 0
    abilities: dict[Ability, int] = field(
        default_factory=lambda: {a: 0 for a in Ability}
    )
    ProficiencyRank: dict[ProficiencyRank, int] = field(
        default_factory=lambda: {p: 0 for p in ProficiencyRank}
    )

    def boost(self,ability: Ability) -> None:
        if self.abilities[ability] < 8:
            self.abilities[ability] += 2
        else:
            self.abilities[ability] += 1
    def modifier(self,ability: Ability) -> int:
        return self.abilities[ability] // 2