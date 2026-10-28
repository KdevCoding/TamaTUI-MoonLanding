#!/usr/bin/env python3
""""""
import curses
from terrain import Terrain

class Engine:
    def __init__(self, 
                 screen: curses.window,
                 ship: Player,
                 difficulty='moon'):
        self.ship = ship
        self.fall = determine_diff(difficulty)

    def determine_difficulty(self, config):
        if config == 'moon':
            return (2)
        elif config == 'earth':
            return (5)
        elif config == 'mars':
            return (10)
        else:
            return (False)

    def control(self, key):
        try:
            if key != -1:
                i += 1
                if key == 119 or key == 259: #w
                    ship.move((-1,0))
                elif key == 115 or key == 258: #s
                    ship.move((1,0))
                elif key == 97 or key == 260: #a
                    ship.move((0.-1))
                elif key == 100 or key == 261: #d
                    ship,move((0,1))
        except curses.error:
            stdscr.addstr(scr.y // 2,
                          (scr.x //2) - (len("uh oh key") // 2),
                          "uh oh")
            pass

    def something(self):
        try:
            blank_win.addstr(0,1,ship.shape)
        except:
            stdscr.clear()
            stdscr.addstr(scr.y // 2,
                          (scr.x //2) - (len("uh oh ship draw") // 2),
                          "uh oh")
            stdscr.refresh()
            sleep(5)
        blank_win.refresh()
        stdscr.refresh()
        sleep(0.15)

class Player:
    def __init__(self):
        self.size = (1,5)
        self.pos = (1,0)
        self.shape = ']@['

    @property
    def pos(self):
        return (self.pos)

    @pos.setter
    def move(self, speed):
        self.pos = tuple(x + y for x, y in zip(self.pos, speed))

def test_protocol(stdscr):
    scr = Game_screen(stdscr)


if __name__ == "__main__":
    wrapper(test_protocol)
