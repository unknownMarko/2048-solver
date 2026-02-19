import curses

from game import Game, Direction


_COLOR_PAIRS: dict[int, int] = {}

_TILE_COLORS = {
    0: (curses.COLOR_BLACK, curses.COLOR_BLACK),
    2: (curses.COLOR_BLACK, curses.COLOR_WHITE),
    4: (curses.COLOR_BLACK, curses.COLOR_YELLOW),
    8: (curses.COLOR_WHITE, curses.COLOR_RED),
    16: (curses.COLOR_WHITE, curses.COLOR_RED),
    32: (curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    64: (curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    128: (curses.COLOR_BLACK, curses.COLOR_YELLOW),
    256: (curses.COLOR_BLACK, curses.COLOR_YELLOW),
    512: (curses.COLOR_BLACK, curses.COLOR_GREEN),
    1024: (curses.COLOR_WHITE, curses.COLOR_GREEN),
    2048: (curses.COLOR_WHITE, curses.COLOR_CYAN),
}

_CELL_WIDTH = 7
_ROW_SEP = "+------+------+------+------+"
_HINT = "Arrow keys: move | q: quit | r: restart"


def _init_colors() -> None:
    curses.start_color()
    curses.use_default_colors()

    pair_index = 1
    for tile_val, (fg, bg) in _TILE_COLORS.items():
        curses.init_pair(pair_index, fg, bg)
        _COLOR_PAIRS[tile_val] = pair_index
        pair_index += 1


def _get_color_attr(value: int) -> int:
    if value not in _COLOR_PAIRS:
        value = 2048
    return curses.color_pair(_COLOR_PAIRS[value])


class GameUI:
    """Curses-based terminal UI for 2048."""

    def __init__(self, game: Game) -> None:
        self._game = game

    def run(self) -> None:
        curses.wrapper(self._main_loop)

    def _main_loop(self, stdscr: "curses.window") -> None:
        curses.curs_set(0)
        stdscr.keypad(True)

        _init_colors()

        game = self._game

        while True:
            stdscr.clear()

            rows, cols = stdscr.getmaxyx()
            if rows < 15 or cols < 45:
                stdscr.addstr(0, 0, "Terminal too small! Need 45x15 minimum.")
                stdscr.refresh()
                stdscr.getch()
                return

            board = game.get_board()
            score = game.get_score()

            next_row = self._draw_full_board(stdscr, board, score, 0, 0)

            if game.is_game_over():
                stdscr.addstr(
                    next_row + 1, 0, "Game Over! Press r to restart or q to quit"
                )
            elif game.has_won():
                stdscr.addstr(next_row + 1, 0, "You Win! (keep playing...)")

            stdscr.addstr(next_row + 2, 0, _HINT)

            stdscr.refresh()

            key = stdscr.getch()

            if key == ord("q"):
                break
            elif key == ord("r"):
                game = Game()
                self._game = game
            elif key == curses.KEY_UP:
                game.move(Direction.UP)
            elif key == curses.KEY_DOWN:
                game.move(Direction.DOWN)
            elif key == curses.KEY_LEFT:
                game.move(Direction.LEFT)
            elif key == curses.KEY_RIGHT:
                game.move(Direction.RIGHT)

    def _draw_full_board(
        self,
        stdscr: "curses.window",
        board: list[list[int]],
        score: int,
        start_row: int,
        start_col: int,
    ) -> int:
        row = start_row
        col = start_col

        score_str = f"Score: {score}"
        stdscr.addstr(row, col, "2048")
        stdscr.addstr(row, col + len(_ROW_SEP) - len(score_str), score_str)
        row += 2

        for r in range(4):
            stdscr.addstr(row, col, _ROW_SEP)
            row += 1

            x = col
            for c in range(4):
                val = board[r][c]
                attr = _get_color_attr(val)
                cell_text = f"| {val:>4} " if val != 0 else "|      "
                stdscr.addstr(row, x, cell_text, attr)
                x += _CELL_WIDTH

            stdscr.addstr(row, x, "|")
            row += 1

        stdscr.addstr(row, col, _ROW_SEP)
        row += 1

        return row
