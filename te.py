import sys
import curses

def initialize_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

def cleanup_curses(stdscr):
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

class CursesScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr

class Text:
    def __init__(self):
        self.text = ""

class UserCommands:
    def __init__(self, kernel):
        self.kernel = kernel
    def handle_input(self, command):
        print('handling ' + command)
        if command == 'm':
            self.kernel.move_cursor_up()

class Kernel:
    def __init__(self, screen, text, screen_offset, cursor_position):
        self.screen = screen
        self.text = text
        self.screen_offset = screen_offset
        self.cursor_position = cursor_position
    def handle_resize(self):
        print('got resize')
    def move_cursor_up(self):
        print('moving cursor up')

def dispatch_input(stdscr, kernel, user_commands):
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            return
        elif key < 256:
            user_commands.handle_input(chr(key))
        elif key == curses.KEY_RESIZE:
            kernel.handle_resize()
        else:
            pass

def open_io():
    stdscr = initialize_curses()
    return {
        'screen': CursesScreen(stdscr),
        'signal_stream': stdscr
    }

def close_io(io):
    cleanup_curses(io['signal_stream'])

def start_editor(io):
    text = Text()
    cursor = Cursor(text)
    screen_offset = ScreenOffset(text)
    screen_refresher = ScreenRefresher(io['screen'], text, cursor, screen_offset)
    kernel = Kernel(text, cursor, screen_offset, screen_refresher)
    user_commands = UserCommands(kernel)
    dispatch_input(io['signal_stream'], screen_refresher, user_commands)

def main():
    io = open_io()
    start_editor(io)
    close_io(io)

main()
