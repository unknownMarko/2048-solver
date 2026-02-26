"""2048 game — entry point."""

import argparse
import sys
from game import Game
from ui import GameUI


def main() -> None:
    parser = argparse.ArgumentParser(description="2048 game with AI solvers")
    parser.add_argument("--solver", choices=["random", "heuristic", "montecarlo"],
                        help="AI solver to use")
    parser.add_argument("--games", type=int, default=100,
                        help="number of games to run (default: 100)")
    parser.add_argument("--simulations", type=int, default=100,
                        help="number of MC simulations per move (default: 100)")
    args = parser.parse_args()
    
    if args.solver is None:
        # No solver specified — manual play
        GameUI(Game()).run()
    else:
        # Validate --games
        if args.games < 1:
            parser.error("--games must be at least 1")
        
        # Import solver
        if args.solver == "random":
            from solvers.random_solver import RandomSolver
            solver = RandomSolver()
        elif args.solver == "heuristic":
            from solvers.heuristic_solver import HeuristicSolver
            solver = HeuristicSolver()
        elif args.solver == "montecarlo":
            from solvers.monte_carlo_solver import MonteCarloSolver
            solver = MonteCarloSolver(simulations=args.simulations)
        
        from runner import run_games
        run_games(solver, args.games, args.solver)


if __name__ == "__main__":
    main()
