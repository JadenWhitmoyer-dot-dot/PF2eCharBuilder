from pf2e.models import Character, Ability, ProficiencyRank, Skill
import pytest

# --- Ability Boosts---
def test_boost_below_threshold():
    c = Character("Test")
    c.abilities[Ability.STR] = 6 # a +3 mod
    c.boost(Ability.STR)
    assert c.modifier(Ability.STR) == 4

def test_boost_at_threshold_is_partial():
    c = Character("Test")
    c.abilities[Ability.STR] = 8 # a +4 mod
    c.boost(Ability.STR)
    assert c.abilities[Ability.STR] == 9
    assert c.modifier(Ability.STR) == 4 # still +4

def test_boost_two_half_points_is_full():
    c = Character("Test")
    c.abilities[Ability.STR] = 9 # a +4 mod and one half point
    c.boost(Ability.STR)
    assert c.abilities[Ability.STR] == 10
    assert c.modifier(Ability.STR) == 5 # now a +5 mod

# --- Prof Ranks ---

def test_untrained_ignores_level():
    assert ProficiencyRank.Untrained.bonus(1) == 0
    assert ProficiencyRank.Untrained.bonus(10) == 0

def test_trained_at_level_1():
    assert ProficiencyRank.Trained.bonus(1) == 3

def test_legendary_at_level_20():
    assert ProficiencyRank.Legendary.bonus(20) == 28

# Testing the two classes together
def test_rank_bonus_uses_character_level():
    c = Character("Test", level=5)
    assert ProficiencyRank.Expert.bonus(c.level) == 9

@pytest.mark.parametrize("rank, level, expected", [
    (ProficiencyRank.Untrained, 1, 0),
    (ProficiencyRank.Untrained, 10, 0),
    (ProficiencyRank.Trained, 1, 3),
    (ProficiencyRank.Expert, 5, 9),
    (ProficiencyRank.Master, 10, 16),
    (ProficiencyRank.Legendary, 20, 28),
])
def test_proficiency_bonus(rank, level, expected):
    assert rank.bonus(level) == expected

# --- Skills ---

def test_all_skills_default_to_untrained():
    c = Character("Test")
    assert all(rank == ProficiencyRank.Untrained
               for rank in c.proficiencies.values())
    assert set(c.proficiencies) == set(Skill)
def test_skill_bonus_trained():
    c = Character("Test", level=3)
    c.abilities[Ability.DEX] = 4 # a +2mod
    c.proficiencies[Skill.ACROBATICS] = ProficiencyRank.Trained
    assert c.skill_bonus(Skill.ACROBATICS) == 7 #2+(3+2)

def test_skill_bous_untrained_is_just_ability_mod():
    c = Character("Test", level=3)
    c.abilities[Ability.DEX] = 4
    assert c.skill_bonus(Skill.ACROBATICS) == 2 #2=0, level ignored

def test_skill_bonus_uses_the_skills_key_ability():
    c = Character("Test", level=1)
    c.abilities[Ability.INT] = 6 # +3 Mod
    c.abilities[Ability.STR] = 0 # +0 Mod
    assert c.skill_bonus(Skill.ARCANA) == 3 #Int-Based
    assert c.skill_bonus(Skill.ATHLETICS) ==0 #STR-Based
