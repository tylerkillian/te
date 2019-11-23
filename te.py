import sys
import curses
import traceback

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
        elif chr_int == curses.KEY_DOWN:
            return 'DOWN'
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
    def get_num_lines(self):
        return len(self.text)

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
    def set_column_index(self, value):
        self.column_index = value

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

class CursorMovements:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def move_cursor_up(self):
        if self.cursor.get_line_index() == 0:
            return
        self.cursor.set_line_index(self.cursor.get_line_index() - 1)
        if self.cursor.get_column_index() > self.text.get_line_length(self.cursor.get_line_index()):
            self.cursor.set_column_index(self.text.get_line_length(self.cursor.get_line_index()))
        if self.screen_offset.get_line_index() > self.cursor.get_line_index():
            self.screen_offset.set_line_index(self.cursor.get_line_index())
        if self.screen_offset.get_column_index() > self.cursor.get_column_index():
            self.screen_offset.set_column_index(self.cursor.get_column_index())
    def move_cursor_down(self):
        if self.cursor.get_line_index() == self.text.get_num_lines() - 1:
            return
        self.cursor.set_line_index(self.cursor.get_line_index() + 1)
        if self.cursor.get_column_index() > self.text.get_line_length(self.cursor.get_line_index()):
            self.cursor.set_column_index(self.text.get_line_length(self.cursor.get_line_index()))
        if self.screen_offset.get_line_index() + self.screen.get_num_lines() == self.cursor.get_line_index():
            self.screen_offset.set_line_index(self.screen_offset.get_line_index() + 1)
        if self.screen_offset.get_column_index() > self.cursor.get_column_index():
            self.screen_offset.set_column_index(self.cursor.get_column_index())

class MoveCursorUp:
    def __init__(self):
        pass
    def set_cursor_position(self, text, cursor):
        if cursor.get_line_index() == 0:
            return False
        cursor.set_line_index(cursor.get_line_index() - 1)
        if cursor.get_column_index() > text.get_line_length(cursor.get_line_index()):
            cursor.set_column_index(text.get_line_length(cursor.get_line_index()))
        return True
    def set_screen_offset(self, cursor, screen_offset):
        if screen_offset.get_line_index() > cursor.get_line_index():
            screen_offset.set_line_index(cursor.get_line_index())
        if screen_offset.get_column_index() > cursor.get_column_index():
            screen_offset.set_column_index(cursor.get_column_index())
    def respond(self, text, screen, cursor, screen_offset):
        cursor_moved = self.set_cursor_position(text, cursor)
        if cursor_moved:
            self.set_screen_offset(cursor, screen_offset)

class MoveCursorDown:
    def __init__(self):
        pass
    def set_cursor_position(self, text, cursor):
        if cursor.get_line_index() == text.get_num_lines() - 1:
            return False
        cursor.set_line_index(cursor.get_line_index() + 1)
        if cursor.get_column_index() > text.get_line_length(cursor.get_line_index()):
            cursor.set_column_index(text.get_line_length(cursor.get_line_index()))
        return True
    def set_screen_offset(self, screen, cursor, screen_offset):
        if screen_offset.get_line_index() + screen.get_num_lines() == cursor.get_line_index():
            screen_offset.set_line_index(screen_offset.get_line_index() + 1)
        if screen_offset.get_column_index() > cursor.get_column_index():
            screen_offset.set_column_index(cursor.get_column_index())
    def respond(self, text, screen, cursor, screen_offset):
        cursor_moved = self.set_cursor_position(text, cursor)
        if cursor_moved:
            self.set_screen_offset(screen, cursor, screen_offset)

def get_character(signal):
    return signal[-1]

def API():
    def api(signal):
        if signal == 'CHARACTER_q':
            return
        elif signal == 'RESIZE':
            return
        elif signal == 'UP':
            return MoveCursorUp()
        elif signal == 'DOWN':
            return MoveCursorDown()
        else:
            return
    return api

def get_character(signal):
    return signal[-1]

#def dispatch_signals(signal_stream, screen_refresher, cursor_movements):
#    while True:
#        signal = signal_stream.get_next_signal()
#        if signal == 'CHARACTER_q':
#            return
#        elif signal == 'RESIZE':
#            pass
#        elif signal == 'UP':
#            cursor_movements.move_cursor_up()
#        elif signal == 'DOWN':
#            cursor_movements.move_cursor_down()
#        else:
#            screen_refresher.screen.stdscr.addstr('handling ' + get_character(signal))
#        screen_refresher.refresh()

def dispatch_signals(signal_stream, api, text, screen, cursor, screen_offset, screen_refresher):
    signal_handler = api(signal_stream.get_next_signal())
    while signal_handler:
        signal_handler.respond(text, screen, cursor, screen_offset)
        screen_refresher.refresh()
        signal_handler = api(signal_stream.get_next_signal())

def curses_open():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

def curses_close(stdscr):
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

class CursesIO:
    def __init__(self, stdscr):
        self.screen = CursesScreen(stdscr)
        self.signal_stream = CursesSignalStream(stdscr)
    def get_screen(self):
        return self.screen
    def get_signal_stream(self):
        return self.signal_stream

def start_editor(io):
    text = Text(POEM)
    cursor = Cursor(text, 10, 50)
    screen_offset = ScreenOffset(text, 4, 3)
    screen_refresher = ScreenRefresher(io.get_screen(), text, cursor, screen_offset)
    cursor_movements = CursorMovements(text, io.get_screen(), cursor, screen_offset)
    screen_refresher.refresh()
    dispatch_signals(io.get_signal_stream(), API(), text, io.get_screen(), cursor, screen_offset, screen_refresher)

def main():
    try:
        stdscr = curses_open()
        start_editor(CursesIO(stdscr))
    except Exception as e:
        f = open('error_out', 'w')
        f.write('Exception: ' + str(e) + '\n\n')
        f.write('Stack trace: ' + traceback.format_exc())
        f.close()
    finally:
        curses_close(stdscr)

main()
