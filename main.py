"""2048 game — entry point."""

from game import Game
from ui import GameUI


def main() -> None:
    GameUI(Game()).run()


if __name__ == "__main__":
    main()
