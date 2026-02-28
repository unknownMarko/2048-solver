"""Heuristic solver — evaluates board states using corner weight, empty cells, and monotonicity."""

from game import Game, Direction

# Snake-pattern weight matrix: highest weight in top-left corner,
# winding down so the largest tile is rewarded for staying in the corner.
_WEIGHT_MATRIX = [
    [2**15, 2**14, 2**13, 2**12],
    [2**8, 2**9, 2**10, 2**11],
    [2**7, 2**6, 2**5, 2**4],
    [2**0, 2**1, 2**2, 2**3],
]

_EMPTY_CELL_WEIGHT = 1000


class HeuristicSolver:
    def get_move(self, game: Game) -> Direction:
        best_score = -1.0
        best_dir = game.get_available_moves()[0]
        for direction in game.get_available_moves():
            trial = Game(board=game.get_board())
            trial.move(direction)
            score = self._evaluate(trial.get_board())
            if score > best_score:
                best_score = score
                best_dir = direction
        return best_dir

    def _evaluate(self, board: list[list[int]]) -> float:
        corner = 0.0
        empty = 0
        for r in range(4):
            for c in range(4):
                v = board[r][c]
                corner += v * _WEIGHT_MATRIX[r][c]
                if v == 0:
                    empty += 1

        mono = 0.0
        for r in range(4):
            row = board[r]
            if all(row[i] >= row[i + 1] for i in range(3)):
                mono += sum(row)
            elif all(row[i] <= row[i + 1] for i in range(3)):
                mono += sum(row)
        for c in range(4):
            col = [board[r][c] for r in range(4)]
            if all(col[i] >= col[i + 1] for i in range(3)):
                mono += sum(col)
            elif all(col[i] <= col[i + 1] for i in range(3)):
                mono += sum(col)

        return corner + empty * _EMPTY_CELL_WEIGHT + mono
