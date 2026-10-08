from time import sleep
from curses import wrapper
import curses
stdscr = curses.initscr()


class rocket():
    def __init__(self):
        self.pos = (1,0)
    
def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    t = 0
    i = 0
    key = 0
    stdscr.nodelay(True)
    ship = rocket()
    while True:
        t += 1
        stdscr.clear()
        stdscr.addstr(0, 0, 'input: {} count: {} __{}__'.format(key, i, t))

        try:
            key = stdscr.getch()
            if key != -1:
                i +=1
                if key == 119 or key == 259: #w
                    ship.pos = tuple(x + y for x, y in zip(ship.pos, (-1,0)))
                elif key == 115 or key == 258: #s
                    ship.pos = tuple(x + y for x, y in zip(ship.pos, (1,0)))
                elif key == 97 or key == 260: #a
                    ship.pos = tuple(x + y for x, y in zip(ship.pos, (0,-1)))
                elif key == 100 or key == 261: #d
                    ship.pos = tuple(x + y for x, y in zip(ship.pos, (0,1)))
        except curses.error:
            pass

        stdscr.addstr(ship.pos[0], ship.pos[1],'#')
        stdscr.refresh()
        sleep(0.015)

wrapper(main)