import curses
from random import randint


def key_event_loop(window):
    while True:
        c = window.getch()

        if c == ord('r') or c == ord('R'):
            window.clear()
            window.addstr('Getting quote...{}'.format(randint(0, 6)),
                          curses.color_pair(3))
            window.refresh()
        elif c == ord('q') or c == ord('Q'):
            break

        # Refresh the windows from the bottom up
        window.refresh()
        curses.doupdate()


@curses.wrapper
def main(stdscr):
    curses.curs_set(0)

    stdscr.addstr('Bio', curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)
    win_size_str = f'{curses.LINES}, {curses.COLS}'
    stdscr.addstr(0, curses.COLS - len(win_size_str), win_size_str, curses.A_REVERSE)

    stdscr.addstr(curses.LINES - 1, 0, "Press 'Q' to quit", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    # Set up the window to search
    search_window = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)

    mid_point = curses.LINES // 2
    text_window = search_window.subwin(3, curses.COLS - 4,
                                       mid_point - 2, 2)
    text_window.box()
    text_window.addstr(1, 2, f'Search your files.')


    # Draw a border around the main search window
    search_window.box()

    # Update the internal window data structures
    stdscr.noutrefresh()
    search_window.noutrefresh()

    # Redraw the screen
    curses.doupdate()

    key_event_loop(search_window)
