import curses
import math
import random


class Terrain:
    """the terrain class"""
    def __init__(self, height, width):
        """get the current screen extents"""
        self.__height = height
        self.__width = width

        self.__offset_x0 = random.uniform(0, 9)
        self.__offset_x1 = random.uniform(0, 6)
        self.__offset_x2 = random.uniform(0, 3)

        self.__wavelen_0 = random.uniform(0.3,0.6)
        self.__wavelen_1 = random.uniform(1.8,3.6)
        self.__wavelen_2 = random.uniform(4.5,7)

        self.__max_x0 = self.__wavelen_0 * math.pi
        self.__max_x1 = self.__wavelen_1 * math.pi
        self.__max_x2 = self.__wavelen_2 * math.pi

        self.__min_x0 = -1 * self.__max_x0
        self.__min_x1 = -1 * self.__max_x1
        self.__min_x2 = -1 * self.__max_x2

        self.__Amplitude = 2.5 # random.uniform(2.5,4.5)

        self.__min_y = self.__Amplitude * -1
        self.__max_y = self.__Amplitude

        self.__math_x0 = 0
        self.__math_x1 = 0
        self.__math_x2 = 0

        self.__math_y = 0

        self.__row = 0;

    def draw_t(self):
        """the function to draw the terrain"""
        for col in range(self.__width):
            self.__math_x0 = (self.__min_x0 + (col / (self.__width - 1 or 1)) * (self.__max_x0 - self.__min_x0)) + self.__offset_x0
            self.__math_x1 = (self.__min_x1 + (col / (self.__width - 1 or 1)) * (self.__max_x1 - self.__min_x1)) + self.__offset_x1
            self.__math_x2 = (self.__min_x2 + (col / (self.__width - 1 or 1)) * (self.__max_x2 - self.__min_x2)) + self.__offset_x2

            self.__math_y = (math.sin(self.__math_x0) / 2 ) + (math.sin(self.__math_x1) / 3) + (math.sin(self.__math_x2) / 6)
            self.__row = int((self.__math_y / (self.__max_y - self.__min_y)) * (self.__height - 1))

            if 0 <= self.__row < self.__height:  
                stdscr.addch(self.__row, col, '*')


def draw_graph(stdscr):
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()

    terrain = Terrain(height, width)

    while True:
        # Clear the screen and re-read dimensions (handles terminal resizes)
        stdscr.clear()
        # note that this might need to be changed

        terrain.draw_t()

        title = f" offset_x0 = {offset_x0:.2f} "
        stdscr.addstr(0, max(0, origin_x - len(title) // 2), title, curses.A_REVERSE)

        title = f" wavex = {wavex0:.2f} "
        stdscr.addstr(1, max(0, wavex0 - len(title) // 2), title, curses.A_REVERSE)        

        prompt = "Press any key for a new shape, or q to quit..."
        stdscr.addstr(height - 1, 0, prompt[:width - 1])

        stdscr.refresh()

        # Wait for a keystroke: q exits, anything else loops and redraws
        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break

if __name__ == "__main__":
    curses.wrapper(draw_graph)