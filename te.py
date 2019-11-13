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

class Screen:
    def on(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
    def off(self):
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    def get_keyboard_input():
        key = self.stdscr.getch()
        if key < 256:
            return chr(key)
        else:
            return key

def main():
    filename = get_filename_from_command_line()
    text = load_text(filename)
    edit_text(text)
    save_text(text, filename)

    screen = Screen()
    screen.on()
    while True:
        key = get_keyboard_input()
        if key == 'q':
            break
        else:
            print(key)
    screen.off()

main()
