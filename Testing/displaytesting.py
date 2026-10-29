from time import sleep
from curses import wrapper
import curses
from terrain import Terrain
stdscr = curses.initscr()


class Rocket():
    def __init__(self, pos=(1,0)):
        self.pos = pos
        self.size = (1,5)

    def move(self, amount):
        self.pos = tuple(x + y for x, y in zip(self.pos, amount))


class Game_screen():
    def __init__(self, stdscr):
        self.y, self.x = stdscr.getmaxyx()
    
    def resize(self):
        self.y, self.x = stdscr.getmaxyx()


class Menu():
    def __init__(self, stdscr, scr):
        self.y = scr.y
        self.x = scr.x
        self.stdscr = stdscr
        self.state = True
        self.screen = "MM"
        
    def main_menu(self):
        Text= ["S: Start", "O: Options", "E: Exit"]
        for i, option in enumerate(Text):
            stdscr.addstr((self.y // 2) + i, (self.x // 2) - (len(option) // 2), option)
    
    def display(self):
        if self.screen == "MM":
            self.main_menu()
        try:
            key = stdscr.getch()
            if key != -1:
                if key == 115: #s
                    self.state = False
                elif key == 111: #o
                    pass
                elif key == 101: #e
                    exit()                
        except curses.error:
            pass
        
def main(stdscr):
    scr = Game_screen(stdscr)

    t = 0
    i = 0
    key = 0
    stdscr.nodelay(False)
    curses.curs_set(0)
    ship = Rocket(pos=(2, (scr.x // 2)))
    menu = Menu(stdscr, scr)
    terrain = Terrain(scr.y, scr.x)
    blank_win = curses.newwin(1, 5, ship.pos[0], ship.pos[1])
    terrain.show()
    while True:
        while menu.state:
            menu.display()
        curses.flushinp()
        sleep(0.01)
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        blank_win.clear()
        try:
            blank_win.mvwin(ship.pos[0], ship.pos[1])
        except:
            stdscr.clear()
            stdscr.addstr(scr.y // 2, (scr.x // 2) - (len("GameOver you got lost") // 2), "GameOver you got lost")
            stdscr.refresh()
            menu.state = True
            sleep(5)
            break
        t += 1
        terrain.show()
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
            blank_win.addstr(0, 1,'<.>')
        except:
            stdscr.clear()
            stdscr.addstr(scr.y // 2, (scr.x // 2) - (len("GameOver you got lost") // 2))
            stdscr.refresh()
            menu.state = True
            sleep(5)
            break
        blank_win.refresh()
        stdscr.refresh()
        sleep(0.15)

wrapper(main)
