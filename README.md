# 2048

Python implementation of the [2048 game](https://en.wikipedia.org/wiki/2048_(video_game)).

## How to Run

```bash
python3 main.py
```

Requires Python 3.x — no external dependencies.

## Controls

| Key | Action |
|-----|--------|
| Arrow keys | Move tiles |
| `r` | Restart |
| `q` | Quit |

## Solvers

The game includes three AI solvers:

- **Random**: Picks a random valid move each turn (baseline strategy)
- **Heuristic**: Evaluates board states using corner weight, empty cells, and monotonicity
- **Monte Carlo**: Runs random simulations per move, picks highest average score (default: 100 simulations)

## CLI Usage

```bash
python3 main.py                              # Manual play
python3 main.py --solver random --games 100  # Random solver, 100 games
python3 main.py --solver heuristic --games 50
python3 main.py --solver montecarlo --games 10
python3 main.py --solver montecarlo --games 5 --simulations 50  # Fewer sims = faster
```

## Statistics

Running a solver prints a statistics report with:
- Best/worst/average score
- Win/loss ratio
- Max tile distribution with bar chart
- Move direction breakdown
