#! /usr/bin/env python

# vim: set ai sw=4 sm:

import curses
from time import sleep
from os import system
import sys
import argparse

def c_init():
    stdscr = curses.initscr()
    curses.noecho()
    # curses.cbreak()
    stdscr.keypad(1)
    return stdscr

def c_cleanup(stdscr):
    stdscr.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def do_stuff(window, *stuff, **pause):
    pause_each = True
    pause_end  = True
    if 'pause_each' in pause:
        pause_each = pause['pause_each']
    if 'pause_end' in pause:
        pause_end = pause['pause_end']

    for item in stuff:
        item(window)
        window.refresh()
        if pause_each:
            window.getch()
    if pause_end and not pause_each:
        window.getch()

# Some stuff from:
#   http://www.tuxradar.com/content/code-project-build-ncurses-ui-python
def first_ui():
    myscreen = curses.initscr()

    # myscreen.border(0)
    myscreen.addstr(12, 25, "Python curses in action!")
    # myscreen.refresh()
    myscreen.getch()

    curses.endwin()

# more stuff from ui example (the real code)
def get_param(screen, prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

def execute_cmd(cmd_string):
     system("clear")
     a = system(cmd_string)
     print ""
     if a == 0:
       print "Command executed correctly"
     else:
       print "Command terminated with error"
     raw_input("Press enter")
     print ""

def example_main():
    x = 0

    screen = curses.initscr()
    while x != ord('4'):
        screen.clear()
        screen.border(0)
        screen.addstr(2, 2, "Please enter a number...")
        screen.addstr(4, 4, "1 - Add a user")
        screen.addstr(5, 4, "2 - Restart Apache")
        screen.addstr(6, 4, "3 - Show disk space")
        screen.addstr(7, 4, "4 - Exit")
        screen.refresh()

        x = screen.getch()

        if x == ord('1'):
            username = get_param(screen, "Enter the username")
            homedir = get_param(screen, "Enter the home directory, eg /home/nate")
            groups = get_param(screen, "Enter comma-separated groups, eg adm,dialout,cdrom")
            shell = get_param(screen, "Enter the shell, eg /bin/bash:")
            curses.endwin()
            # execute_cmd("useradd -d " + homedir + " -g 1000 -G " + groups + " -m -s " + shell + " " + username)
            execute_cmd("echo useradd -d " + homedir + " -g 1000 -G " + groups + " -m -s " + shell + " " + username)
        if x == ord('2'):
            curses.endwin()
            # execute_cmd("apachectl restart")
            execute_cmd("echo apachectl restart")
        if x == ord('3'):
            curses.endwin()
            # execute_cmd("df -h")
            execute_cmd("echo df -h")

    curses.endwin()
# end of more stuff ...

def clear(window):
    window.erase()
    #window.clear()

def phello(window):
    window.addstr(5, 10, 'Hello, world!')

def show_size(window):
    y,x = window.getmaxyx()
    size_str = '{}x{}'.format(y, x)
    window.addstr(0, 1, size_str)

def border(window):
    window.border(0)

def draw_walls(window):
    wall_chrs = [curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LRCORNER, curses.ACS_LLCORNER,
                 curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_TTEE, curses.ACS_BTEE,
                 curses.ACS_HLINE, curses.ACS_VLINE, curses.ACS_PLUS]
    y,x = window.getmaxyx()

    window.move(2,1)
    for ch in wall_chrs:
        window.addch(ch)

LEFT   = 0
TOP    = 1
RIGHT  = 2
BOTTOM = 3

def move_cursor(window, from_side, location, direction):
    """Move cursor in specified direction, if possible.
       If cursor is already against edge, leave it in current location."""
    y,x = location
    miny, minx = 0, 0
    maxy, maxx = window.getmaxyx()

    if direction == curses.KEY_DOWN:
        if from_side == LEFT:
            window.addch(y-1, x+1, curses.ACS_URCORNER)
            window.addch(y, x+1, curses.ACS_VLINE)
            window.addch(y+1, x-1, curses.ACS_URCORNER)
            window.addch(y+1, x+1, curses.ACS_VLINE)
            window.addch(y+2, x-1, curses.ACS_VLINE)
        elif from_side == TOP:
            window.addch(y, x+1, curses.ACS_VLINE)
            window.addch(y+1, x-1, curses.ACS_VLINE)
            window.addch(y+1, x+1, curses.ACS_VLINE)
            window.addch(y+2, x-1, curses.ACS_VLINE)
        y = min(y+2, maxy-1)
        from_side = TOP
    elif direction == curses.KEY_UP:
        # y = max(y-1, miny)
        pass
    elif direction == curses.KEY_LEFT:
        # x = max(x-1, minx)
        pass
    elif direction == curses.KEY_RIGHT:
        if from_side == TOP:
            window.addch(y-1, x+1, curses.ACS_LLCORNER)
            if x == maxx - 3:
                window.addch(y-1, x+2, curses.ACS_BTEE)
            else:
                window.addch(y-1, x+2, curses.ACS_HLINE)

            if x == 1:
                window.addch(y+1, x-1, curses.ACS_LTEE)
            else:
                window.addch(y+1, x-1, curses.ACS_LLCORNER)
            window.addch(y+1, x, curses.ACS_HLINE)
            window.addch(y+1, x+1, curses.ACS_HLINE)
            if x == maxx - 3:
                window.addch(y, x+2, ' ')
                window.addch(y+1, x+2, curses.ACS_TTEE)
        elif from_side == LEFT:
            window.addch(y-1, x+1, curses.ACS_HLINE)
            if x == maxx - 3:
                window.addch(y-1, x+2, curses.ACS_BTEE)
            else:
                window.addch(y-1, x+2, curses.ACS_HLINE)
            window.addch(y+1, x, curses.ACS_HLINE)
            window.addch(y+1, x+1, curses.ACS_HLINE)
            if x == maxx - 3:
                window.addch(y, x+2, ' ')
                window.addch(y+1, x+2, curses.ACS_TTEE)
        x = min(x+2, maxx-1)
        from_side = LEFT
    return (from_side, (y,x))


def move_through(window):
    """Assume that we're in a window with a border drawn.
       Open a hole on the top left, and allow cursor to move toward
       the bottom right"""

    y,x = window.getmaxyx()
    window.keypad(1)
    moves = [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT]
    multi_moves = [[27, 91, 66], [27, 91, 65], [27, 91, 68], [27, 91, 67]]

    window.move(2,0)
    window.addch(curses.ACS_BTEE)
    window.addch(curses.ACS_HLINE)
    window.move(3,0)
    window.addch(' ')
    window.move(4,0)
    window.addch(curses.ACS_TTEE)
    window.refresh()

    location = (3,1)
    from_side = LEFT;
    window.move(*location)

    while True:
        ch = window.getch()
        rep = str(ch)
        if ch == ord(' '):
            break
        window.addstr(y-1, x-10, rep)
        for col in range(x+len(rep)-10, x-1):
            window.addch(y-1, col, curses.ACS_HLINE)
        if ch in moves:
            from_side, location = move_cursor(window, from_side, location, ch)
            # if ch == curses.KEY_DOWN: location = (location[0]+1, location[1])
            # elif ch == curses.KEY_UP: location = (location[0]-1, location[1])
            # elif ch == curses.KEY_LEFT: location = (location[0], location[1]-1)
            # elif ch == curses.KEY_RIGHT: location = (location[0], location[1]+1)
        window.move(*location)
        window.refresh()

def show_input(win):
    win.erase()
    win.border(0)
    y,x = window.getmaxyx()
    size_str = '{}x{}'.format(y, x)
    window.addstr(0, 1, size_str)

global_exception = None

def taddch(win, ch):
    # Yuck.  Bug in python curses: doing addch() in the lower right
    # corner of a window throws an exception.  See commentary here:
    # https://bugs.python.org/issue8243
    try:
        win.addch(ch)
    except curses.error as e:
        y, x = win.getmaxyx()
        if (y-1, x-1) == win.getyx():
            return
        raise e

CH_UNKNOWN = 0
CH_EMPTY   = 1
CH_FULL    = 2

class CharBlock(object):
    """Class to hold all the possible combinations of neighbor values for a
    given location, and map them to a specific output value for the location."""

    pass

class Snake(object):
    """Class to play a snake game in a text window."""
    Right = (0,1)
    Left  = (0,-1)
    Down  = (1, 0)
    Up    = (-1, 0)
    Head_ch = '@'
    Body_ch = 'o'
    Directions = {curses.KEY_LEFT:(0, -1),
		  ord('h'):(0,-1),
		  curses.KEY_RIGHT:(0,1),
		  ord('l'):(0,1),
		  curses.KEY_UP:(-1,0),
		  ord('k'):(-1,0),
		  curses.KEY_DOWN:(1,0),
		  ord('j'):(1,0)}

    def __init__(self, win=None):
	self.move_time = 0.35
	self.win = win
	self.location = (1,1)	# Start in upper left corner
	self.direction = Snake.Right   # Start moving right
	self.round = 1
	self.add_every = 5
	self.speedup = 10

    def draw(self):
	if self.win:
	    self.win.border(0)

    @staticmethod
    def calc_move(old, delta):
	return (old[0]+delta[0], old[1]+delta[1])

    def move(self, grow=False):
	old_head = self.head
	new_head = Snake.calc_move(old_head, self.direction)
	win = self.win
	inch = win.inch(*new_head)
	if inch != ord(' '):
	    self.done = True
	    # raise ValueError('head ran into {:x}'.format(inch))

	self.head = new_head
	self.snake.insert(0,new_head)
	win.addch(new_head[0], new_head[1], Snake.Head_ch)
	win.addch(old_head[0], old_head[1], Snake.Body_ch)
	if not grow:
	    # Get tail position
	    y,x = self.snake[-1]
	    win.addch(y, x, ' ')
	    self.snake.pop()
	    win.move(*self.head)

    def handle_input(self, ch):
	if ch == ord('q') or ch == ord('Q'):
	    self.done = True
	elif ch == ord(' '):
	    self.pause = not self.pause
	elif ch in Snake.Directions:
	    self.direction = Snake.Directions[ch]

    def play(self):
	self.snake = [self.location]
	self.head = self.location
	self.tail = self.location
	self.done = False
	self.pause = False

	self.win.nodelay(True)
	self.win.move(*self.location)
	self.win.addch(Snake.Head_ch)

	while True:
	    while True:
		ch = self.win.getch()
		if ch == -1:
		    # No input available
		    break
		self.handle_input(ch)
	    if self.done:
		break
	    if self.pause:
		continue
	    if self.add_every != 0 and self.round % self.add_every == 0:
		self.move(True)
	    else:
		self.move(False)
	    if self.speedup != 0 and self.round % self.speedup == 0:
		self.move_time *= 0.9

	    self.round += 1
	    self.win.move(*self.location)
	    self.win.refresh()

	    sleep(0.1 + self.move_time)

class Maze(object):
    outch = '? #'

    def __init__(self, win=None, ingress=(0,0)):
        self.win = win
        self.ysize, self.xsize = (0,0)
        if win:
            self.ysize, self.xsize = win.getmaxyx()
        self.ingress = ingress
        self.egress = (0,0)
        self.initgrid()
        self.cursor=(0,0)

    def initgrid(self, value=CH_UNKNOWN):
        if self.ysize == 0 or self.xsize == 0:
            self.grid = None
        else:
            self.grid = [[value for x in range(self.xsize)] for y in range(self.ysize)]

    def goto(self, y, x):
        self.cursor = (y, x)

    def move(self, offset):
        y,x = self.cursor
        yoff, xoff = offset
        y = y + yoff
        x = x + xoff
        y = max(0, y)
        y = min(self.ysize-1, y)
        x = max(0, x)
        x = min(self.xsize-1, x)

        self.cursor = (y, x)

    def display(self):
        if not self.win:
            return
        assert(len(self.grid) == self.ysize and len(self.grid[0]) == self.xsize)
        for row in range(len(self.grid)):
            self.win.move(row, 0)
            for col in range(len(self.grid[row])):
                taddch(self.win, self.outch[self.grid[row][col]])
        self.win.move(*self.cursor)
        self.win.refresh()

    def display2(self):
        if not self.win:
            return
        assert(len(self.grid) == self.ysize and len(self.grid[0]) == self.xsize)

	def calc_ch(y, x):
	    if y == 0:
		# Top row
		if x == 0:
		    # Left column
		    pass
		elif x == self.xsize - 1:
		    # Right column
		    pass
		else:
		    # Middle column
		    pass
	    elif y == self.ysize - 1:
		# Bottom row
		if x == 0:
		    # Left column
		    pass
		elif x == self.xsize - 1:
		    # Right column
		    pass
		else:
		    # Middle column
		    pass
	    else:
		# Middle row
		if x == 0:
		    # Left column
		    pass
		elif x == self.xsize - 1:
		    # Right column
		    pass
		else:
		    # Middle column
		    pass

        for row in range(len(self.grid)):
            self.win.move(row, 0)
            for col in range(len(self.grid[row])):
                taddch(self.win, self.outch[self.grid[row][col]])
        self.win.move(*self.cursor)
        self.win.refresh()

    def dispkey(self, ch):
        assert(0 < ch < 1000)
        assert(self.xsize > 5)
        self.win.move(0, self.xsize-4)
        self.win.addstr('{:3}'.format(ch))
        self.win.refresh()

    def build(self, ingress, display_keys=False):
        moves = {curses.KEY_LEFT:(0, -1), curses.KEY_RIGHT:(0,1),
                 curses.KEY_UP:(-1,0), curses.KEY_DOWN:(1,0)}
        assert(len(ingress) == 2)
        y,x = ingress
        assert(0 <= y < self.ysize)
        assert(0 <= x < self.xsize)
        assert(x == 0 or y == 0)
        assert(not (x == 0 and y == 0))

        self.initgrid(CH_FULL)
        self.ingress = ingress
        self.goto(y, x)
        self.grid[y][x] = CH_EMPTY
        self.display()
        ch = self.win.getch()
        while (ch != ord('q') and ch != ord('Q')):
	    # these 2 lines show the ordinal value of each input character
	    # in the upper right corner of the window for 1/2 second.
	    if display_keys:
		self.dispkey(ch)
		sleep(0.5)
            if ch in moves:
                # raise(ValueError)
                self.move(moves[ch])
                y,x = self.cursor
                self.grid[y][x] = CH_EMPTY
                self.display()
            ch = self.win.getch()

    def setwin(win):
        self.__init__(win)

def maketunnel(window):
    do_stuff(window, clear, border, show_size, pause_each=False)
    sub1 = window.derwin(20,40, 5, 5)
    do_stuff(sub1, border, show_size, pause_each=False)
    move_through(sub1)

def do_maze(draw_base=True, pause_each=False, early_exit=False):
    window = c_init()
    if draw_base:
	do_stuff(window, clear, border, show_size, pause_each=pause_each)

    if early_exit:
	c_cleanup(window)
	return

    y, x = (20, 40)
    win1 = window.derwin(y, x, 2, 5)
    win1.keypad(1)
    maze = Maze(win1)
    # maze.initgrid(CH_FULL)
    # maze.display()
    maze.build((2,0), display_keys=False)
    # window.getch()

    c_cleanup(window)
    print 'maze is {}x{}.'.format(maze.ysize, maze.xsize)
    print 'win1 is {}x{}.'.format(*win1.getmaxyx())

def do_tunnel():
    window = c_init()
    window.erase()
    window.refresh()
    sleep(1)
    maketunnel(window)
    c_cleanup(window)

def do_cleanup():
    window = c_init()
    c_cleanup(window)

def do_some_stuff():
    window = c_init()
    do_stuff(window, border, show_size)
    sub1 = window.derwin(20,40, 5, 5)
    do_stuff(sub1, border, show_size, draw_walls)
    do_stuff(sub1, phello)
    inch = sub1.inch(1,1)
    # first_ui()
    c_cleanup(window)
    print "Char at (1,1) is: '{}'".format(inch)

def do_snake():
    window = c_init()
    screen_size = window.getmaxyx()
    s = Snake(window)
    s.draw()
    window.getch()
    s.play()
    c_cleanup(window)
    print screen_size

if __name__ == '__main__':
    command_list = {'maze':do_maze,
		    'tunnel':do_tunnel,
		    'stuff': do_some_stuff,
		    'cleanup': do_cleanup,
		    'snake': do_snake}
    p = argparse.ArgumentParser(description='Some curses programs')
    p.add_argument('command', choices=command_list, nargs='?', default='maze')
    args = p.parse_args()
    # print 'Command is: {}'.format(args.command)
    command = command_list[args.command]
    command()
