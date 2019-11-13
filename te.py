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
    return curses.initscr()

def cleanup_curses(stdscr):
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

class CursesScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr

class CursesKeyboard:
    def __init__(self, stdscr):
        self.stdscr = stdscr
    def get_input(self):
        key = self.stdscr.getch()
        if key < 256:
            return chr(key)
        elif key == curses.KEY_RESIZE:
            return 'resize'
        else:
            return key

def main():
    filename = get_filename_from_command_line()
    text = load_text(filename)
    edit_text(text)
    save_text(text, filename)

    stdscr = initialize_curses()
    screen = CursesScreen(stdscr)
    keyboard = CursesKeyboard(stdscr)
    key = keyboard.get_input()
    cleanup_curses(stdscr)
    print(key)

main()
