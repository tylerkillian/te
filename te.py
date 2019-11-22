import sys
import curses

POEM = [
    'Two roads diverged in a yellow wood,',
    'And sorry I could not travel both',
    'And be one traveler, long I stood',
    'And looked down one as far as I could',
    'To where it bent in the undergrowth;',
    '',
    'Then took the other, as just as fair,',
    'And having perhaps the better claim,',
    'Because it was grassy and wanted wear;',
    'Though as for that the passing there',
    'Had worn them really about the same,',
    '',
    'And both that morning equally lay',
    'In leaves no step had trodden black.',
    'Oh, I kept the first for another day!',
    'Yet knowing how way leads on to way,',
    'I doubted if I should ever come back.',
    '',
    'I shall be telling this with a sigh',
    'Somewhere ages and ages hence:',
    'Two roads diverged in a wood, and I-',
    'I took the one less traveled by,',
    'And that has made all the difference.'
]

class CursesScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr
    def draw(self, data):
        self.stdscr.erase()
        try:
            for line_index, line in enumerate(data):
                for character_index, character in enumerate(line):
                    self.stdscr.addch(line_index, character_index, ord(character))
            junk.close()
        except Exception: # capture exception after writing to lower right hand corner of window
            pass
        self.stdscr.refresh()
    def set_cursor_position(self, line_index, column_index):
        self.stdscr.move(line_index, column_index)
    def get_num_lines(self):
        num_lines, _ = self.stdscr.getmaxyx()
        return num_lines
    def get_num_columns(self):
        _, num_columns = self.stdscr.getmaxyx()
        return num_columns
                

class CursesSignalStream:
    def __init__(self, stdscr):
        self.stdscr = stdscr
    def get_next_signal(self):
        chr_int = self.stdscr.getch()
        if chr_int < 256:
            return 'CHARACTER_' + chr(chr_int)
        elif chr_int == curses.KEY_RESIZE:
            return 'RESIZE'
        elif chr_int == curses.KEY_UP:
            return 'UP'
        else:
            return 'UNKNOWN'

class Text:
    def __init__(self, text=''):
        self.text = text
    def get_text(self, line_index, num_lines, column_index, num_columns):
        result = []
        for line in self.text[line_index:line_index + num_lines]:
            result.append(line[column_index:column_index + num_columns])
        return result
    def get_line_length(self, line_index):
        return len(self.text[line_index])

class Cursor:
    def __init__(self, text, line_index=0, column_index=0):
        self.line_index = line_index
        self.column_index = column_index
        self.text = text
    def get_line_index(self):
        return self.line_index
    def set_line_index(self, value):
        self.line_index = value
    def get_column_index(self):
        return self.column_index
    def set_column_index(self, value):
        self.column_index = value

class ScreenOffset:
    def __init__(self, text, line_index=0, column_index=0):
        self.line_index = line_index
        self.column_index = column_index
        self.text = text
    def get_line_index(self):
        return self.line_index
    def set_line_index(self, value):
        self.line_index = value
    def get_column_index(self):
        return self.column_index

class ScreenRefresher:
    def __init__(self, screen, text, cursor, screen_offset):
        self.screen = screen
        self.text = text
        self.cursor = cursor
        self.screen_offset = screen_offset
    def refresh(self):
        text_to_draw = self.text.get_text(
            self.screen_offset.get_line_index(),
            self.screen.get_num_lines(),
            self.screen_offset.get_column_index(),
            self.screen.get_num_columns())
        self.screen.draw(text_to_draw)
        self.screen.set_cursor_position(
            self.cursor.get_line_index() - self.screen_offset.get_line_index(),
            self.cursor.get_column_index() - self.screen_offset.get_column_index())

class Kernel:
    def __init__(self, text, cursor, screen_offset, screen_refresher):
        self.text = text
        self.cursor = cursor
        self.screen_offset = screen_offset
        self.screen_refresher = screen_refresher
    def move_cursor_up(self):
        #self.screen_refresher.screen.stdscr.addstr('moving cursor up')
        if self.cursor.get_line_index() == 0:
            return
        self.cursor.set_line_index(self.cursor.get_line_index() - 1)
        if self.cursor.get_column_index() > self.text.get_line_length(self.cursor.get_line_index()):
            self.cursor.set_column_index(self.text.get_line_length(self.cursor.get_line_index()))

        #if self.screen_offset.get_line_index() > cursor_new_line_index:
        #    self.screen_offset.set_line_index(self.cursor.get_line_index())
        #if self.screen_offset.get_column_index() > self.cursor.get_column_index():
        #    self.screen_offset.set_column_index(self.cursor.get_column_index())
        self.screen_refresher.refresh()

class UserCommands:
    def __init__(self, kernel):
        self.kernel = kernel
    def handle_character(self, character):
        self.kernel.screen_refresher.screen.stdscr.addstr('handling ' + character)
    def handle_arrow(self, direction):
        if direction == 'UP':
            self.kernel.move_cursor_up()

def get_character(signal):
    return signal[-1]

def dispatch_signals(signal_stream, screen_refresher, user_commands):
    while True:
        signal = signal_stream.get_next_signal()
        if signal == 'CHARACTER_q':
            return
        elif signal == 'RESIZE':
            screen_refresher.refresh()
        elif signal == 'UP':
            user_commands.handle_arrow('UP')
        else:
            user_commands.handle_character(get_character(signal))

class CursesIO:
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
    text = Text(POEM)
    cursor = Cursor(text, 10, 50)
    screen_offset = ScreenOffset(text)#, 2, 3)
    screen_refresher = ScreenRefresher(io.get_screen(), text, cursor, screen_offset)
    kernel = Kernel(text, cursor, screen_offset, screen_refresher)
    user_commands = UserCommands(kernel)
    screen_refresher.refresh()
    dispatch_signals(io.get_signal_stream(), screen_refresher, user_commands)

def main():
     start_editor(CursesIO())
#    try:
#        start_editor(CursesIO())
#    except Exception as e:
#        print(str(e))
#        while True:
#            pass
#    io = CursesIO()
#    text = Text(POEM)
#    cursor = Cursor(text, 0, 0)
#    screen_offset = ScreenOffset(text, 0, 0)
#    screen_refresher = ScreenRefresher(io.get_screen(), text, cursor, screen_offset)
#    screen_refresher.refresh()
#    io.get_signal_stream().get_next_signal()

main()
