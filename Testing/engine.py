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

class Engine:
    def __init__(self, 
                 screen: curses.window,
                 ship: Player,
                 difficulty='moon'):
        self.ship = ship
        self.fall = self.determine_diff(difficulty)

    def determine_diff(self, config):
        if config == 'moon':
            return (2)
        elif config == 'mars':
            return (5)
        elif config == 'earth':
            return (10)
        else:
            return (False)

    def control(self, key, scr, i):
        try:
            if key != -1:
                i += 1
                if key == 119 or key == 259: #w
                    self.hip.move((-1,0))
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
    stdscr.nodelay(True)
    curses.curs_set(0)
    ship = Player()
    physics = Engine(stdscr, ship, 'mars')
    terrain = Terrain(scr.y, scr.x)
    blank_win = curses.newwin(1,5,ship.pos[0], ship.pos[1])
    terrain.show()
    while True:
        curses.flushinp()
        sleep(0.05)
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        blank_win.clear()
        blank_win.mvwin(ship.pos[0], ship.pos[1])

        t += 1
        terrain.show()
        stdscr.addstr(0, 0, f'input: {key} count: {i} __{t}__')
        scr.resize()
        physics.control(stdscr.getch(), scr, i)
        physics.clean_up(scr, blank_win, ship)

if __name__ == "__main__":
    stdscr = curses.initscr()
    wrapper(main)
