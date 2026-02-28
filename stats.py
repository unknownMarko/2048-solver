"""Statistics collection and reporting for 2048 solver runs."""


class GameStats:
    """Collects and reports statistics from solver game runs."""

    def __init__(self) -> None:
        """Initialize empty statistics storage."""
        self._scores: list[int] = []
        self._max_tiles: list[int] = []
        self._wins: int = 0
        self._losses: int = 0
        self._total_moves: list[int] = []
        self._moves_per_dir: dict[str, list[int]] = {
            "UP": [],
            "DOWN": [],
            "LEFT": [],
            "RIGHT": [],
        }

    def record_game(
        self,
        score: int,
        max_tile: int,
        won: bool,
        total_moves: int,
        moves_per_direction: dict[str, int],
    ) -> None:
        """Record results of a single game.

        Args:
            score: Final game score
            max_tile: Highest tile value achieved
            won: Whether the game reached 2048
            total_moves: Total number of moves made
            moves_per_direction: Count of moves in each direction (UP, DOWN, LEFT, RIGHT)
        """
        self._scores.append(score)
        self._max_tiles.append(max_tile)
        if won:
            self._wins += 1
        else:
            self._losses += 1
        self._total_moves.append(total_moves)
        for direction, count in moves_per_direction.items():
            if direction in self._moves_per_dir:
                self._moves_per_dir[direction].append(count)

    def print_report(self, solver_name: str, num_games: int) -> None:
        """Print formatted statistics report.

        Args:
            solver_name: Name of the solver being evaluated
            num_games: Number of games run
        """
        if not self._scores:
            print("No games recorded.")
            return

        # Header
        print("=== 2048 Solver Results ===")
        print(f"Solver: {solver_name} | Games: {num_games}")
        print()

        # Score section
        avg_score = sum(self._scores) / len(self._scores)
        print("Score:")
        print(f"  Best:    {max(self._scores)}")
        print(f"  Worst:   {min(self._scores)}")
        print(f"  Average: {avg_score:.1f}")
        print()

        # Win/Loss section
        total = self._wins + self._losses
        win_pct = (self._wins / total * 100) if total > 0 else 0.0
        loss_pct = (self._losses / total * 100) if total > 0 else 0.0
        print("Win/Loss:")
        print(f"  Wins:   {self._wins} ({win_pct:.1f}%)")
        print(f"  Losses: {self._losses} ({loss_pct:.1f}%)")
        print()

        # Max Tile section
        avg_max_tile = sum(self._max_tiles) / len(self._max_tiles)
        print("Max Tile:")
        print(f"  Average: {avg_max_tile:.1f}")
        print("  Distribution:")
        self._print_tile_distribution()
        print()

        # Moves section
        avg_moves = sum(self._total_moves) / len(self._total_moves)
        print("Moves:")
        print(f"  Average total: {avg_moves:.1f}")
        print("  Per direction:")

        total_dir_moves = sum(sum(counts) for counts in self._moves_per_dir.values())

        for direction in ("UP", "DOWN", "LEFT", "RIGHT"):
            counts = self._moves_per_dir[direction]
            avg_dir = sum(counts) / len(counts) if counts else 0.0
            dir_total = sum(counts)
            dir_pct = (
                (dir_total / total_dir_moves * 100) if total_dir_moves > 0 else 0.0
            )
            print(f"    {direction + ':':8s}{avg_dir:.1f} ({dir_pct:.1f}%)")

    def _print_tile_distribution(self) -> None:
        """Print tile distribution with ASCII bar chart."""
        # Count occurrences of each tile value
        tile_counts: dict[int, int] = {}
        for tile in self._max_tiles:
            tile_counts[tile] = tile_counts.get(tile, 0) + 1

        if not tile_counts:
            return

        max_count = max(tile_counts.values())
        total = len(self._max_tiles)
        max_bar_width = 40

        # Sort tiles in ascending order, skip zeros
        for tile in sorted(tile_counts.keys()):
            if tile == 0:
                continue
            count = tile_counts[tile]
            pct = count / total * 100
            bar_width = int(count / max_count * max_bar_width) if max_count > 0 else 0
            # Ensure at least 1 block for non-zero counts
            if bar_width == 0 and count > 0:
                bar_width = 1
            bar = "\u2588" * bar_width
            print(f"    {tile:>5d}: {bar} {count} ({pct:.1f}%)")
