#!/usr/bin/env python3
import curses
import math
import random


class Terrain:
    """generate terrain shape & render to curses pad"""

    def __init__(self, height, width):
        """all of the sin wave values"""
        self.__height = height
        self.__width = width

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

        self.__amplitude = 2.5
        self.__min_y = -self.__amplitude
        self.__max_y = self.__amplitude

        """off screen canvas, drawn here first"""
        self.__pad = curses.newpad(self.__height, self.__width)
        self.__render()

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

    def __render(self):
        """cycle through the pad width and draw each column"""
        self.__pad.erase()
        span = (self.__width - 1) or 1

        for col in range(self.__width):
            t = col / span
            x0 = self.__min_x0 + t * (self.__max_x0 - self.__min_x0) + self.__offset_x0
            x1 = self.__min_x1 + t * (self.__max_x1 - self.__min_x1) + self.__offset_x1
            x2 = self.__min_x2 + t * (self.__max_x2 - self.__min_x2) + self.__offset_x2

            y = math.sin(x0) / 2 + math.sin(x1) / 3 + math.sin(x2) / 6

            """Map y from [min_y, max_y] onto [0, height-1], flipped so up is up"""
            norm = (y - self.__min_y) / (self.__max_y - self.__min_y)
            row = (self.__height - 1) - int(norm * (self.__height - 1))

            if 0 <= row < self.__height:
                try:
                    self.__pad.addch(row, col, '*')
                except curses.error:
                    """bottom-right cell raises safe to ignore"""
                    pass

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
            terrain = Terrain(height, width)

        # terrain.label(0, f" offset_x0 = {terrain.offset_x0:.2f} ", col=2)
        # terrain.label(1, f" wavelen_0 = {terrain.wavelen_0:.2f} ", col=2)
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