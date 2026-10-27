import yaml
from pathlib import Path
from pf2e.models import ClassDef, Ability, ProficiencyRank, Skill



def load_class(path: Path) -> ClassDef:
    raw = yaml.safe_load(path.read_text())
    name = raw["name"]
    hp_per_level = raw["hp_per_level"]
    try:
        key_abilities = [Ability[name] for name in raw["key_abilities"]]
    except KeyError as e:
        raise ValueError(
            f"{path.name}: unknown ability {e} in 'key_abilities'"
        ) from e
    perception = ProficiencyRank[raw["perception"]]
    saves = {name: ProficiencyRank[rank] for name, rank in raw["saves"].items()}
    trained_skills = [Skill[name] for name in raw["trained_skills"]]
    skill_choices = raw["skill_choices"]
    skill_options = [Skill[name] for name in raw["skill_options"]]
    return ClassDef(
        name=name,
        hp_per_level=hp_per_level,
        key_abilities=key_abilities,
        perception=perception,
        saves=saves,
        trained_skills=trained_skills,
        skill_choices=skill_choices,
        skill_options=skill_options
    )
