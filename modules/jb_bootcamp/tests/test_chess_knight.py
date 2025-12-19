import pytest

from jb_bootcamp.chess_knight import KnightBoard, knight_minimum_moves


def test_knight_minimum_moves_basic():
    assert knight_minimum_moves("a1", "c2") == 1
    assert knight_minimum_moves("a1", "a1") == 0


def test_knight_minimum_moves_longer_path():
    # Long diagonal requires several hops on an 8x8 board.
    assert knight_minimum_moves("a1", "h8") == 6


def test_knight_minimum_moves_unreachable_board():
    board = KnightBoard(size=2)
    with pytest.raises(ValueError):
        knight_minimum_moves("a1", "b2", size=board.size)
