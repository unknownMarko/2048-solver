"""Monte Carlo solver — uses random playouts to evaluate moves."""

import random
from game import Game, Direction


class MonteCarloSolver:
    def __init__(self, simulations: int = 100) -> None:
        self._simulations = simulations

    def get_move(self, game: Game) -> Direction:
        available = game.get_available_moves()

        # Optimization: skip simulation if only one move
        if len(available) == 1:
            return available[0]

        best_direction = available[0]
        best_avg_score = -1.0

        for direction in available:
            total_score = 0
            for _ in range(self._simulations):
                # Clone game and apply candidate move
                sim = Game(board=game.get_board())
                sim.move(direction)

                # Random playout until game over
                while not sim.is_game_over():
                    moves = sim.get_available_moves()
                    sim.move(random.choice(moves))

                total_score += sim.get_score()

            avg_score = total_score / self._simulations
            if avg_score > best_avg_score:
                best_avg_score = avg_score
                best_direction = direction

        return best_direction
