#!/usr/bin/env python3
import curses
import math
import random


class Terrain:
    """generate terrain shape & render to curses pad"""

    def __init__(self, height, width, difficulty="Easy"):
        """all of the sin wave values"""
        self.__height = height
        self.__width = width

        if difficulty == "Easy":
            self.__amplitude = 5
            self.__breadth = 9
        elif difficulty == "Medium":
            self.__amplitude = 3
            self.__breadth = 6
        elif difficulty == "Hard":
            self.__amplitude = 1.5
            self.__breadth = 3

        self.__offset_x0 = random.uniform(0, 9)
        self.__offset_x1 = random.uniform(0, 6)
        self.__offset_x2 = random.uniform(0, 3)

        self.__wavelen_0 = random.uniform(0.3, 0.6)
        self.__wavelen_1 = random.uniform(1.8, 3.6)
        self.__wavelen_2 = random.uniform(4.5, 7)

        self.__max_x0 = self.__wavelen_0 * math.pi
        self.__max_x1 = self.__wavelen_1 * math.pi
        self.__max_x2 = self.__wavelen_2 * math.pi

        self.__min_x0 = -self.__max_x0
        self.__min_x1 = -self.__max_x1
        self.__min_x2 = -self.__max_x2

        self.__min_y = -self.__amplitude
        self.__max_y = self.__amplitude

        """off screen canvas, drawn here first"""
        self.__pad = curses.newpad(self.__height, self.__width)
        self.__land = self.__landing()
        self.__render()

    def __landing(self):
        """cycle through the pad width and find possible landing sites"""
        locations = []

        for col in range(self.__breadth, self.__width - self.__breadth):
            first = self.__surface_row(col)
            if all(self.__surface_row(col + i) == first for i in range(1, self.__breadth)):
                locations.append(col)

        if locations:
            return random.choice(locations)
        return 0

    """private values for HUD placement"""
    @property
    def pad(self):
        return self.__pad

    @property
    def offset_x0(self):
        return self.__offset_x0

    @property
    def wavelen_0(self):
        return self.__wavelen_0

    def __surface_row(self, col):
        """Return the pad row of the terrain surface at a given column.

        0,0 is top left - max vals are 'bottom right' of screen
        """
        span = (self.__width - 1) or 1
        t = col / span

        x0 = self.__min_x0 + t * (self.__max_x0 - self.__min_x0) + self.__offset_x0
        x1 = self.__min_x1 + t * (self.__max_x1 - self.__min_x1) + self.__offset_x1
        x2 = self.__min_x2 + t * (self.__max_x2 - self.__min_x2) + self.__offset_x2

        y = math.sin(x0) / 2 + math.sin(x1) / 3 + math.sin(x2) / 6

        """Map y from [min_y, max_y] onto [0, height-1], flipped so up is up"""
        norm = (y - self.__min_y) / (self.__max_y - self.__min_y)
        return (self.__height - 1) - int(norm * (self.__height - 1))

    def __render(self):
        """cycle through the pad width and draw each column"""
        self.__pad.erase()
        shape = '*'

        for col in range(self.__width):

            if col == self.__land - 1:
                shape = '|'
            if col == self.__land:
                shape = '_'
            if col == self.__land + self.__breadth:
                shape = '|'
            if col > self.__land + self.__breadth:
                shape = '*'

            row = self.__surface_row(col)

            if 0 <= row < self.__height:
                try:
                    self.__pad.addch(row, col, shape)
                except curses.error:
                    """bottom-right cell raises safe to ignore"""
                    pass
    
    def landed(self, pos):
        return pos[1] in range(self.__land, self.__land + self.__breadth + 1)
    
    def is_below(self, pos):
        """True if the point (y, x) is on or below the terrain curve.

        x is a pad column and y is a pad row (row 0 = top), the same
        coordinates the terrain is drawn in.
        """
        col = max(0, min(self.__width - 1, int(pos[1])))  # clamp to the pad
        return int(pos[0]) >= self.__surface_row(col)

    def is_above(self, pos):
        return not self.is_below(pos)

    def label(self, row, text, col=0):
        """Write overlay text onto the pad so it ends up in the same refresh."""
        try:
            self.__pad.addstr(row, max(0, col), text[: self.__width - col - 1],
                              curses.A_REVERSE)
        except curses.error:
            pass

    def show(self):
        """Copy the pad to the physical screen"""
        self.__pad.refresh(0, 0, 0, 0, self.__height - 1, self.__width - 1)


def draw_graph(stdscr):
    curses.curs_set(0)

    terrain = None
    while True:
        height, width = stdscr.getmaxyx()

        if terrain is None:
            terrain = Terrain(height, width, "Hard")

        terrain.label(height - 1, "Press any key for a new shape, or q to quit...")

        terrain.show()

        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break
        if key == curses.KEY_RESIZE:
            curses.update_lines_cols()
            stdscr.clear()
        """any key (or a resize) builds a new terrain/pad"""
        terrain = None


if __name__ == "__main__":
    curses.wrapper(draw_graph)