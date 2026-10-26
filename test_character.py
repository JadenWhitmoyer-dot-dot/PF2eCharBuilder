from Character import Character, Ability

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