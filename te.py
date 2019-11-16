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

def main():
    stdscr = initialize_curses()

    screen = CursesScreen(stdscr)
    text = Text()
    cursor = Cursor(sceen, text)
    field_of_view = FieldOfView(screen, text)
    user_commands = UserCommands(Kernel(screen, text, screen_offset, cursor_position))

    dispatch_input(stdscr, screen_resizer, user_commands)

    cleanup_curses(stdscr)

main()
