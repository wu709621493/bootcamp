from __future__ import annotations

import pytest

from jb_bootcamp.supermarket import (
    Delivery,
    SupermarketProduct,
    plan_restock,
    simulate_inventory,
)


def test_plan_restock_accounts_for_lead_time_and_safety_stock() -> None:
    products = [
        SupermarketProduct("荔枝", "produce", daily_demand=5.2, safety_stock=4),
        SupermarketProduct("rice noodles", "pantry", daily_demand=2.5, safety_stock=2),
    ]
    stock = {"荔枝": 6, "rice noodles": 3}

    orders = plan_restock(products, stock, lead_time_days=2, planning_days=3)

    assert orders == {"荔枝": 24, "rice noodles": 12}


def test_simulate_inventory_consumes_demand_and_applies_deliveries() -> None:
    products = [
        SupermarketProduct("荔枝", "produce", daily_demand=5, safety_stock=4),
        SupermarketProduct("rice noodles", "pantry", daily_demand=2, safety_stock=2),
    ]
    initial_stock = {"荔枝": 6, "rice noodles": 5}
    deliveries = [
        Delivery("荔枝", day=1, quantity=4),
        Delivery("rice noodles", day=2, quantity=3),
    ]
    patterns = {"荔枝": (3, 2), "rice noodles": (2,)}

    history = simulate_inventory(
        products,
        initial_stock,
        deliveries,
        patterns,
        days=4,
    )

    assert history == {"荔枝": (3, 5, 2, 0), "rice noodles": (3, 1, 2, 0)}


def test_simulate_inventory_rejects_unknown_demand_entry() -> None:
    products = [SupermarketProduct("豆腐", "fresh", daily_demand=2)]

    with pytest.raises(KeyError):
        simulate_inventory(
            products,
            initial_stock={"豆腐": 5},
            deliveries=(),
            demand_pattern={"辣椒": (1,)},
            days=2,
        )

