"""Utilities for modelling knight movement on a square board."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Iterable, List, Sequence, Tuple, Union

# The eight possible offsets a knight can travel from any given square.
_KNIGHT_DELTAS: Tuple[Tuple[int, int], ...] = (
    (1, 2),
    (2, 1),
    (-1, 2),
    (-2, 1),
    (1, -2),
    (2, -1),
    (-1, -2),
    (-2, -1),
)


@dataclass(frozen=True, order=True)
class Square:
    """A 1-indexed chessboard square."""

    file: int
    rank: int

    def __post_init__(self) -> None:
        if self.file < 1 or self.rank < 1:
            raise ValueError("file and rank must be positive integers.")

    def to_algebraic(self) -> str:
        """Return algebraic notation (e.g., ``'e4'``) for the square."""

        file_letter = chr(ord("a") + self.file - 1)
        return f"{file_letter}{self.rank}"

    @classmethod
    def from_algebraic(cls, notation: str) -> "Square":
        """Create a :class:`Square` from algebraic notation like ``'g6'``."""

        notation = notation.strip()
        if len(notation) < 2 or not notation[0].isalpha() or not notation[1:].isdigit():
            raise ValueError(f"Invalid algebraic notation {notation!r}.")
        file_letter = notation[0].lower()
        file_index = ord(file_letter) - ord("a") + 1
        return cls(file=file_index, rank=int(notation[1:]))


class KnightBoard:
    """Model knight movement and routing on an ``size``-by-``size`` board."""

    def __init__(self, size: int = 8) -> None:
        if size < 1:
            raise ValueError("Board size must be at least 1x1.")
        self.size = size

    def legal_moves(self, square: Union[Square, str]) -> List[Square]:
        """Return all legal knight destinations from ``square``."""

        start = self._coerce_square(square)
        moves: List[Square] = []
        for file_delta, rank_delta in _KNIGHT_DELTAS:
            candidate_file = start.file + file_delta
            candidate_rank = start.rank + rank_delta
            if 1 <= candidate_file <= self.size and 1 <= candidate_rank <= self.size:
                moves.append(Square(file=candidate_file, rank=candidate_rank))
        return sorted(moves)

    def shortest_path(self, start: Union[Square, str], target: Union[Square, str]) -> Sequence[Square]:
        """Compute the minimal sequence of knight moves from ``start`` to ``target``."""

        start_square = self._coerce_square(start)
        target_square = self._coerce_square(target)
        if start_square == target_square:
            return [start_square]

        queue: Deque[Square] = deque([start_square])
        parents: Dict[Square, Square | None] = {start_square: None}

        while queue:
            current = queue.popleft()
            for move in self.legal_moves(current):
                if move not in parents:
                    parents[move] = current
                    if move == target_square:
                        return self._reconstruct_path(parents, target_square)
                    queue.append(move)

        raise ValueError("Target square is unreachable for the knight.")

    def _reconstruct_path(self, parents: Dict[Square, Square | None], target: Square) -> Sequence[Square]:
        path: List[Square] = [target]
        while parents[path[-1]] is not None:
            parent = parents[path[-1]]
            if parent is None:
                break
            path.append(parent)
        path.reverse()
        return path

    def _coerce_square(self, value: Union[Square, str]) -> Square:
        if isinstance(value, Square):
            square = value
        else:
            square = Square.from_algebraic(value)
        if not self._is_on_board(square):
            raise ValueError(f"Square {square} is off a {self.size}x{self.size} board.")
        return square

    def _is_on_board(self, square: Square) -> bool:
        return 1 <= square.file <= self.size and 1 <= square.rank <= self.size


def move_sequence_as_algebraic(squares: Iterable[Square]) -> Tuple[str, ...]:
    """Render a sequence of squares as algebraic coordinates."""

    return tuple(square.to_algebraic() for square in squares)


def knight_minimum_moves(
    start: Union[Square, str],
    target: Union[Square, str],
    *,
    size: int = 8,
) -> int:
    """Return the minimal number of knight moves from ``start`` to ``target``.

    Parameters
    ----------
    start, target
        Starting and target squares, either as :class:`Square` objects or
        algebraic coordinates like ``"a1"``.
    size
        Board dimension; defaults to a standard ``8x8`` chessboard.

    Returns
    -------
    int
        Number of moves needed to reach the target.  A start square that is
        already the target returns ``0``.

    Raises
    ------
    ValueError
        If either square is off the board or the target cannot be reached on a
        board of the given size.
    """

    board = KnightBoard(size)
    path = board.shortest_path(start, target)
    return len(path) - 1
