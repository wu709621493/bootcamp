from jb_bootcamp.emergency_exit import Exit, estimate_evacuation_time, exit_throughput


def test_exit_throughput_respects_congestion():
    exit_clear = Exit(width_m=1.2)
    exit_congested = Exit(width_m=1.2, congested=True)

    baseline = exit_throughput(exit_clear)
    slowed = exit_throughput(exit_congested, congestion_penalty=0.2)

    assert slowed == baseline * 0.8


def test_estimate_evacuation_time_combines_travel_and_throughput():
    exits = [Exit(width_m=1.0), Exit(width_m=0.8)]
    total_time = estimate_evacuation_time(occupants=100, exits=exits, average_travel_time=20)

    # Combined throughput = (1.0 + 0.8) * 1.3 = 2.34 people/s
    expected = 20 + 100 / 2.34
    assert total_time == expected


def test_invalid_inputs_raise_value_error():
    single_exit = [Exit(width_m=1.0)]

    for occupants in (0, -10):
        try:
            estimate_evacuation_time(occupants=occupants, exits=single_exit)
        except ValueError:
            pass
        else:  # pragma: no cover - defensive clause
            raise AssertionError("Expected ValueError for non-positive occupants")

    for flow_rate in (0, -1):
        try:
            exit_throughput(single_exit[0], flow_rate_per_meter=flow_rate)
        except ValueError:
            pass
        else:  # pragma: no cover
            raise AssertionError("Expected ValueError for non-positive flow_rate_per_meter")

    try:
        estimate_evacuation_time(occupants=10, exits=[])
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("Expected ValueError for missing exits")
