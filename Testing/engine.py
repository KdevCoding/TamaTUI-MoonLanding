import curses
from curses import wrapper
from time import sleep
from terrain import Terrain

class Game_screen():
    def __init__(self, stdscr):
        self.y, self.x = stdscr.getmaxyx()

    def resize(self):
        self.y, self.x = stdscr.getmaxyx()

class Player:
    def __init__(self, pos=(1,0)):
        self.size = (1,5)
        self.pos = pos
        self.shape = ']@['

    @property
    def pos(self):
        return (self.__pos)

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    def move(self, speed):
        curses.flushinp()
        self.pos = tuple(x + y for x, y in zip(self.pos, speed))

    def reset(self):
        self.pos = (1,0)

    def control(self, key, scr):
        try:
            if key != -1:
                if key == 119 or key == 259: #w
                    self.move((-1,0))
                elif key == 115 or key == 258: #s
                    self.move((1,0))
                elif key == 97 or key == 260: #a
                    self.move((0,-1))
                elif key == 100 or key == 261: #d
                    self.move((0,1))

        except curses.error:
            stdscr.addstr(scr.y // 2,
                          (scr.x //2) - (len("uh oh key") // 2),
                          "uh oh key")
            pass
class Menu():
    def __init__(self, stdscr, scr):
        self.scr = scr
        self.stdscr = stdscr
        self.state = True
        self.screen = "MM"
        self.dif = "Easy"
        
        
        
    def main_menu(self):
        MM= ["S: Start", f"E|M|H: {self.dif}", "Q: Quit"]
        for i, option in enumerate(MM):
            stdscr.addstr((self.scr.y // 2) + i, (self.scr.x // 2) - (len(option) // 2), option)
    
    def refresh(self, stdscr):
        stdscr.clear()

        self.main_menu()
        stdscr.refresh

    def display(self, stdscr, scr):
        while True:
            stdscr.nodelay(False)
            scr.resize()
            self.refresh(stdscr)
            key = stdscr.getch()
            if key != -1:
                if key == 115: #s
                    stdscr.clear()
                    stdscr.nodelay(True)
                    self.game = Engine(self.dif)
                    self.game.start(stdscr, scr)
                    curses.flushinp()
                    
                elif key == 111: #o
                    pass
                elif key == 101: #e
                    self.dif = "Easy"
                elif key == 109: #m
                    self.dif = "Medium"
                elif key == 104: #h
                    self.dif = "Hard"   
                elif key == 113: #q
                    exit()              
                self.refresh(stdscr)

class Engine:
    def __init__(self, 
                 difficulty='Easy'):
        self.ship = Player()
        self.difficulty = difficulty
        self.fall = self.determine_fall(self.difficulty)
    
    def determine_fall(self, config):
        if config == 'Easy': #moon
            return (2)
        elif config == 'Medium': #mars
            return (5)
        elif config == 'Hard': #earth
            return (10)
        else:
            return (False)

    def start(self, stdscr, scr):
        self.ship.reset()
        scr.resize()
        terrain = Terrain(scr.y, scr.x, self.difficulty)
        blank_win = curses.newwin(1, 5, self.ship.pos[0], self.ship.pos[1])
        terrain.show()
        self.loop(stdscr, scr, blank_win, terrain)  
          
    def loop(self, stdscr, scr, blank_win, terrain):
        while True:
            terrain.show()
            #curses.flushinp()
            sleep(0.01)
            blank_win.clear()
            try:
                blank_win.mvwin(self.ship.pos[0], self.ship.pos[1])
            except curses.error:
                self.end_screen(stdscr, scr, "GameOver you got lost")
                break
            #terrain.show()
            scr.resize()
            self.ship.control(stdscr.getch(), scr)
            self.clean_up(scr, blank_win)
            if terrain.is_below(self.ship.pos):
                if terrain.landed(self.ship.pos):
                    text = "Congrats you landed!"
                else:
                    text = "GameOver you hit the terrain"
                self.end_screen(stdscr, scr, text)
                break
    def end_screen(self, stdscr, scr, text):
        stdscr.clear()
        stdscr.addstr(scr.y // 2, (scr.x // 2) - (len(text) // 2), text)
        stdscr.refresh()
        curses.flushinp()
        sleep(5)

    def clean_up(self, scr, blank_win):
        try:
            blank_win.addstr(0,1, self.ship.shape)
        except:
            stdscr.clear()
            stdscr.addstr(scr.y // 2,
                          (scr.x //2) - (len("uh oh ship draw") // 2),
                          "uh oh ship draw")
            stdscr.refresh()
            sleep(2)
        blank_win.refresh()
        sleep(0.15)

def main(stdscr):
    scr = Game_screen(stdscr)
    menu = Menu(stdscr, scr)
    curses.curs_set(0)
    while True:
            menu.display(stdscr, scr)
    
        

if __name__ == "__main__":
    stdscr = curses.initscr()
    wrapper(main)
