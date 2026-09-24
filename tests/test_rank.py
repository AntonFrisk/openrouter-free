from orfree.rank import demote


def test_demote_moves_two_steps():
    models = ["a", "b", "c", "d"]
    assert demote(models, "a") == ["b", "c", "a", "d"]


def test_demote_clamps_near_end():
    models = ["a", "b", "c"]
    assert demote(models, "b") == ["a", "c", "b"]
    models = ["a", "b"]
    assert demote(models, "a") == ["b", "a"]


def test_demote_missing_is_noop():
    models = ["a", "b"]
    assert demote(models, "z") == ["a", "b"]
