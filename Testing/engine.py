#!/usr/bin/env python3

""""""

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
        self.pos = tuple(x + y for x, y in zip(self.pos, speed))

    def reset(self):
        self.pos = (1,0)

class Menu():
    def __init__(self, stdscr, scr):
        self.y = scr.y
        self.x = scr.x
        self.stdscr = stdscr
        self.state = True
        self.screen = "MM"
        self.dif = "Easy"
        
        
    def main_menu(self):
        MM= ["S: Start", f"E|M|H: {self.dif}", "Q: Quit"]
        for i, option in enumerate(MM):
            stdscr.addstr((self.y // 2) + i, (self.x // 2) - (len(option) // 2), option)
    
    def refresh(self, stdscr):
        stdscr.clear()
        self.main_menu()
        stdscr.refresh

    def display(self, stdscr, scr, terrain):
        stdscr.nodelay(False)
        scr.resize()
        self.refresh(stdscr)
        while self.state == True:
            key = stdscr.getch()
            if key != -1:
                if key == 115: #s
                    self.state = False
                    stdscr.clear()
                    stdscr.nodelay(True)
                    terrain.show()
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
                 screen: curses.window,
                 ship: Player,
                 difficulty='moon'):
        self.ship = ship
        self.fall = self.determine_diff(difficulty)

    def determine_diff(self, config):
        if config == 'Easy': #moon
            return (2)
        elif config == 'Medium': #mars
            return (5)
        elif config == 'Hard': #earth
            return (10)
        else:
            return (False)

    def control(self, key, scr, i):
        try:
            if key != -1:
                i += 1
                if key == 119 or key == 259: #w
                    self.ship.move((-1,0))
                elif key == 115 or key == 258: #s
                    self.ship.move((1,0))
                elif key == 97 or key == 260: #a
                    self.ship.move((0.-1))
                elif key == 100 or key == 261: #d
                    self.ship.move((0,1))

        except curses.error:
            stdscr.addstr(scr.y // 2,
                          (scr.x //2) - (len("uh oh key") // 2),
                          "uh oh key")
            pass

    def clean_up(self, scr, blank_win, ship):
        try:
            blank_win.addstr(0,1, ship.shape)
        except:
            stdscr.clear()
            stdscr.addstr(scr.y // 2,
                          (scr.x //2) - (len("uh oh ship draw") // 2),
                          "uh oh ship draw")
            stdscr.refresh()
            sleep(2)
        blank_win.refresh()
        stdscr.refresh()
        sleep(0.15)

def main(stdscr):
    scr = Game_screen(stdscr)
    text = "GameOver you got lost"
    t = 0
    i = 0
    key = 0
    ship = Player()
    menu = Menu(stdscr, scr)
    curses.curs_set(0)
    while True:
        if menu.state == True:
            terrain = Terrain(scr.y, scr.x)
            blank_win = curses.newwin(1,5,ship.pos[0], ship.pos[1])
            menu.display(stdscr, scr, terrain)
            ship.reset()
            physics = Engine(stdscr, ship, menu.dif)
        curses.flushinp()
        sleep(0.05)
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        blank_win.clear()
        try:
            blank_win.mvwin(ship.pos[0], ship.pos[1])
        except curses.error:
            stdscr.clear()
            stdscr.addstr(scr.y // 2, (scr.x // 2) - (len("GameOver you got lost") // 2), "GameOver you got lost")
            stdscr.refresh()
            menu.state = True
            sleep(5)
            continue

        t += 1
        terrain.show()
        stdscr.addstr(0, 0, f'dif: {menu.dif} __{t}__')
        scr.resize()
        physics.control(stdscr.getch(), scr, i)
        physics.clean_up(scr, blank_win, ship)

if __name__ == "__main__":
    stdscr = curses.initscr()
    wrapper(main)
