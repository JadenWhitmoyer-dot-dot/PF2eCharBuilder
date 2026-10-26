from pathlib import Path
import pytest
from pf2e.yml_loader import load_class
from pf2e.models import Ability, ProficiencyRank

HERE = Path(__file__).parent

def test_load_fighter():
    fighter = load_class(HERE.parent / "data" / "classes" / "fighter.yaml")
    assert fighter.hp_per_level == 10
    assert Ability.STR in fighter.key_abilities
    assert fighter.perception == ProficiencyRank.Expert
def test_bad_ability_name_raises(tmp_path):
    good = (HERE.parent / "data" / "classes" / "fighter.yaml").read_text()
    bad_file = tmp_path / "bad_fighter.yaml"
    bad_file.write_text(good.replace("STR", "STRR", 1))

    with pytest.raises(KeyError, match="STRR"):
        load_class(bad_file)