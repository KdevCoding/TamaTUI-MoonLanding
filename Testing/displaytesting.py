from time import sleep
from curses import wrapper
import curses
stdscr = curses.initscr()


class rocket():
    def __init__(self, pos=(1,0)):
        self.pos = pos
    
    def move(self, amount):
        self.pos = tuple(x + y for x, y in zip(self.pos, amount))
        
def main(stdscr):
    stdscr.clear()
    
    text = "GameOver you got lost"
    t = 0
    i = 0
    key = 0
    h, w = stdscr.getmaxyx()
    x = (w // 2)
    y = h // 2
    stdscr.nodelay(True)
    ship = rocket(pos=(2, x))
    while True:
        t += 1
        stdscr.clear()
        stdscr.addstr(0, 0, f'input: {key} count: {i} __{t}__')
        
        h, w = stdscr.getmaxyx()
        x = (w // 2) - (len(text) // 2)
        y = h // 2
        
        try:
            key = stdscr.getch()
            if key != -1:
                i +=1
                if key == 119 or key == 259: #w
                    ship.move((-1,0))
                elif key == 115 or key == 258: #s
                    ship.move((1,0))
                elif key == 97 or key == 260: #a
                    ship.move((0,-1))
                elif key == 100 or key == 261: #d
                    ship.move((0,1))
        except curses.error:
            pass
        
        try:
            stdscr.addstr(ship.pos[0], ship.pos[1],'<.>')
        except:
            stdscr.clear()
            stdscr.addstr(y, x, text)
            stdscr.refresh()
            sleep(5)
            break
        stdscr.refresh()
        sleep(0.015)

wrapper(main)
