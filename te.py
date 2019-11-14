import sys
import curses

def get_filename_from_command_line():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return None

def load_text(filename):
    if not filename:
        return ""
    print('loading ' + filename)
    return "the text"

def edit_text(text):
    print('editing ' + text)

def save_text(text, filename):
    if not filename:
        print('ask for filename')
        print('save ' + text)
    else:
        print('saving ' + text + ' to ' + filename)

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

class UserCommands:
    def __init__(self, kernel):
        self.kernel = kernel
    def handle_input(self, command):
        print('handling ' + command)
        if command == 'm':
            self.kernel.move_cursor_up()

class Kernel:
    def __init__(self, screen, text):
        self.screen = screen
        self.text = text
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
    filename = get_filename_from_command_line()
    text = load_text(filename)
    edit_text(text)
    save_text(text, filename)

    stdscr = initialize_curses()
    screen = CursesScreen(stdscr)
    kernel = Kernel(screen, text)
    user_commands = UserCommands(kernel)
    dispatch_input(stdscr, kernel, user_commands)
    cleanup_curses(stdscr)

main()
