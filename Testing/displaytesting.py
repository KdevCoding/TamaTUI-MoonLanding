from time import sleep
from curses import wrapper
import curses
stdscr = curses.initscr()


class Rocket():
    def __init__(self, pos=(1,0)):
        self.pos = pos
    
    def move(self, amount):
        self.pos = tuple(x + y for x, y in zip(self.pos, amount))


class Game_screen():
    def __init__(self, stdscr):
        self.y, self.x = stdscr.getmaxyx()
    
    def resize(self):
        self.y, self.x = stdscr.getmaxyx()

def main(stdscr):
    stdscr.clear()
    scr = Game_screen(stdscr)
    text = "GameOver you got lost"
    t = 0
    i = 0
    key = 0
    stdscr.nodelay(True)
    ship = Rocket(pos=(2, (scr.x // 2)))
    while True:
        t += 1
        stdscr.clear()
        stdscr.addstr(0, 0, f'input: {key} count: {i} __{t}__')
        scr.resize()
        
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
            stdscr.addstr(scr.y // 2, (scr.x // 2) - (len(text) // 2), text)
            stdscr.refresh()
            sleep(5)
            break
        stdscr.refresh()
        sleep(0.015)

wrapper(main)
