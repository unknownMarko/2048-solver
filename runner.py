"""Headless game runner for solver evaluation."""

import sys
from game import Game, Direction
from stats import GameStats


def run_games(solver, num_games: int, solver_name: str) -> None:
    """Run num_games games with the given solver and print stats."""
    verbose = solver_name == "montecarlo"
    stats = GameStats()
    for i in range(num_games):
        game_label = f"Game {i + 1}/{num_games}"
        if not verbose:
            print(f"\r{game_label}...", end="", file=sys.stderr)
        game = Game()
        moves_per_dir: dict[str, int] = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        total_moves = 0
        while not game.is_game_over():
            if verbose:
                print(
                    f"\r{game_label}: move {total_moves + 1} (score: {game.get_score()})...",
                    end="",
                    file=sys.stderr,
                )
            direction = solver.get_move(game)
            if game.move(direction):
                moves_per_dir[direction.name] += 1
                total_moves += 1
        if verbose:
            print(
                f"\r{game_label}: done — score {game.get_score()}, {total_moves} moves",
                file=sys.stderr,
            )
        max_tile = max(c for r in game.get_board() for c in r)
        won = game.has_won()
        stats.record_game(game.get_score(), max_tile, won, total_moves, moves_per_dir)
    if not verbose:
        print(file=sys.stderr)  # newline after progress
    stats.print_report(solver_name, num_games)
