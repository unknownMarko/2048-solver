"""Core 2048 game logic — pure state machine, no I/O."""

from enum import IntEnum
import copy
import random


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Game:
    def __init__(self, board: list[list[int]] | None = None) -> None:
        if board is not None:
            self._board: list[list[int]] = copy.deepcopy(board)
        else:
            self._board = [[0] * 4 for _ in range(4)]
            self._spawn_tile()
            self._spawn_tile()
        self._score: int = 0

    def move(self, direction: Direction) -> bool:
        before = copy.deepcopy(self._board)
        delta = self._apply_direction(direction)
        if self._board == before:
            return False
        self._score += delta
        self._spawn_tile()
        return True

    def get_board(self) -> list[list[int]]:
        return copy.deepcopy(self._board)

    def get_score(self) -> int:
        return self._score

    def is_game_over(self) -> bool:
        for row in self._board:
            if 0 in row:
                return False
        for r in range(4):
            for c in range(4):
                v = self._board[r][c]
                if c + 1 < 4 and self._board[r][c + 1] == v:
                    return False
                if r + 1 < 4 and self._board[r + 1][c] == v:
                    return False
        return True

    def has_won(self) -> bool:
        return any(cell >= 2048 for row in self._board for cell in row)

    def get_available_moves(self) -> list[Direction]:
        available: list[Direction] = []
        for direction in Direction:
            original = copy.deepcopy(self._board)
            self._apply_direction(direction)
            changed = self._board != original
            self._board = original
            if changed:
                available.append(direction)
        return available

    def _spawn_tile(self) -> None:
        empties = [(r, c) for r in range(4) for c in range(4) if self._board[r][c] == 0]
        if not empties:
            return
        r, c = random.choice(empties)
        self._board[r][c] = 2 if random.random() < 0.9 else 4

    @staticmethod
    def _slide_row_left(row: list[int]) -> tuple[list[int], int]:
        compact = [x for x in row if x != 0]
        result: list[int] = []
        score = 0
        i = 0
        while i < len(compact):
            if i + 1 < len(compact) and compact[i] == compact[i + 1]:
                merged = compact[i] * 2
                result.append(merged)
                score += merged
                i += 2
            else:
                result.append(compact[i])
                i += 1
        result += [0] * (4 - len(result))
        return result, score

    def _transpose(self) -> None:
        self._board = [list(row) for row in zip(*self._board)]

    def _reverse_rows(self) -> None:
        for row in self._board:
            row.reverse()

    def _apply_direction(self, direction: Direction) -> int:
        if direction == Direction.UP:
            self._transpose()
            delta = self._slide_all_left()
            self._transpose()
        elif direction == Direction.DOWN:
            self._transpose()
            self._reverse_rows()
            delta = self._slide_all_left()
            self._reverse_rows()
            self._transpose()
        elif direction == Direction.LEFT:
            delta = self._slide_all_left()
        else:
            self._reverse_rows()
            delta = self._slide_all_left()
            self._reverse_rows()
        return delta

    def _slide_all_left(self) -> int:
        total = 0
        for i in range(4):
            self._board[i], delta = self._slide_row_left(self._board[i])
            total += delta
        return total
