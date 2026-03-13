import jb_bootcamp


def test_liberator_removes_blocked_values_preserving_order():
    values = ["alpha", "beta", "gamma", "beta", "delta"]
    blocked = ["beta", "epsilon"]

    assert jb_bootcamp.liberator(values, blocked) == ["alpha", "gamma", "delta"]


def test_liberator_accepts_any_iterable_inputs():
    values = (1, 2, 3, 4, 5)
    blocked = {2, 4}

    assert jb_bootcamp.liberator(values, blocked) == [1, 3, 5]
