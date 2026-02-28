"""Random solver — picks a random valid move each turn."""

import random
from game import Game, Direction


class RandomSolver:
    def get_move(self, game: Game) -> Direction:
        return random.choice(game.get_available_moves())
