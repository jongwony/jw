import curses.textpad

from imgcat import img

stdscr = curses.initscr()

curses.noecho()
# curses.echo()

begin_x = 5
begin_y = 7
height = 40
width = 40
win = curses.newwin(height, width, begin_y, begin_x)
tb = curses.textpad.Textbox(win)
text = tb.edit()
curses.addstr(10, 10, img.test())

hw = "Hello world!"
while 1:
    c = stdscr.getch()
    curses.addstr(1, 1, c)
    if c == ord('p'):
        pass
    elif c == ord('q'):
        break  # Exit the while()
    elif c == curses.KEY_HOME:
        x = y = 0

curses.endwin()
