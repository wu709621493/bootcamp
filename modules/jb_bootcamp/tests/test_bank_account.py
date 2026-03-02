from concurrent.futures import ThreadPoolExecutor

import pytest

from jb_bootcamp.bank_account import BankAccount


def test_open_close_and_balance_lifecycle() -> None:
    account = BankAccount()

    with pytest.raises(ValueError):
        account.get_balance()

    account.open()
    assert account.get_balance() == 0

    account.increment_balance(14)
    account.increment_balance(-4)
    assert account.get_balance() == 10

    account.close()
    with pytest.raises(ValueError):
        account.get_balance()


def test_open_and_close_raise_on_invalid_state() -> None:
    account = BankAccount()

    with pytest.raises(ValueError):
        account.close()

    account.open()
    with pytest.raises(ValueError):
        account.open()


def test_increment_rejects_non_integer_amount() -> None:
    account = BankAccount()
    account.open()

    with pytest.raises(TypeError):
        account.increment_balance(1.5)


def test_increment_is_thread_safe() -> None:
    account = BankAccount()
    account.open()

    def deposit_many() -> None:
        for _ in range(1000):
            account.increment_balance(1)

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: deposit_many(), range(8)))

    assert account.get_balance() == 8000
