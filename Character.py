from dataclasses import dataclass, field
from enum import Enum

class Ability(Enum):
    STR = "strength"
    DEF = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHA = "charisma"


@dataclass
class Character:
    name: str
    level: int = 1
    # PF2e uses modifiers not raw stats: a base human is 0
    abilities: dict[Ability, int] = field(
        default_factory=lambda: {a: 0 for a in Ability}
    )

    def boost(self,ability: Ability) -> None:
        if self.abilities[ability] < 8:
            self.abilities[ability] += 2
        else:
            self.abilities[ability] += 1
    def modifier(self,ability: Ability) -> int:
        return self.abilities[ability] // 2