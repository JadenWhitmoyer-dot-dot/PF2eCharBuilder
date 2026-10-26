from Character import Character, Ability, ProficiencyRank
import pytest

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
