import sys
import curses

class CursesScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr

class CursesSignalStream:
    def __init__(self, stdscr):
        self.stdscr = stdscr
    def get_next_signal():
        chr_int = self.stdscr.getch()
        if chr_int < 256:
            return 'CHARACTER_' + chr(key)
        elif chr_int == curses.KEY_RESIZE:
            return 'RESIZE'
        else:
            return 'UNKNOWN'

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

def get_character(signal):
    return signal[-1]

def dispatch_signals(signal_stream, screen_refresher, user_commands):
    while True:
        signal = signal_stream.get_next_signal()
        if signal == 'CHARACTER_q':
            return
        elif signal == 'RESIZE':
            screen_refresher.refresh()
        else:
            user_commands.handle_character(get_character(signal))

class IO:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.screen = CursesScreen(self.stdscr)
        self.signal_stream = CursesSignalStream(self.stdscr)
    def __del__(self):
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    def get_screen(self):
        return self.screen
    def get_signal_stream(self):
        return self.signal_stream

def start_editor(io):
    text = Text()
    cursor = Cursor(text)
    screen_offset = ScreenOffset(text)
    screen_refresher = ScreenRefresher(io.get_screen(), text, cursor, screen_offset)
    kernel = Kernel(text, cursor, screen_offset, screen_refresher)
    user_commands = UserCommands(kernel)
    dispatch_signals(io.get_signal_stream(), screen_refresher, user_commands)

def main():
    start_editor(IO())

main()
