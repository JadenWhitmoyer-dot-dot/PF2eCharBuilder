from pathlib import Path
from pf2e.yml_loader import load_class
from pf2e.models import Ability, ProficiencyRank

def test_load_fighter():
    fighter = load_class(Path("../data/fighter.yaml"))
    assert fighter.hp_per_level == 10
    assert Ability.STR in fighter.key_abilities
    assert fighter.perception == ProficiencyRank.Expert