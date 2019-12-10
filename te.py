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
    'Because it was grassy and wanted wear;abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
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
        if chr_int == 10:
            return 'ENTER'
        elif chr_int < 256:
            return 'CHARACTER_' + chr(chr_int)
        elif chr_int == curses.KEY_RESIZE:
            return 'RESIZE'
        elif chr_int == curses.KEY_UP:
            return 'UP'
        elif chr_int == curses.KEY_DOWN:
            return 'DOWN'
        elif chr_int == curses.KEY_RIGHT:
            return 'RIGHT'
        elif chr_int == curses.KEY_LEFT:
            return 'LEFT'
        elif chr_int == curses.KEY_DC:
            return 'DELETE'
        elif chr_int == curses.KEY_BACKSPACE:
            return 'BACKSPACE'
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
    def get_num_columns(self, line_index):
        return len(self.text[line_index])
    def get_line(self, line_index):
        return self.text[line_index]
    def set_line(self, line_index, value):
        self.text[line_index] = value
    def insert_line(self, line_index, line):
        self.text.insert(line_index, line)
    def delete_line(self, line_index):
        del self.text[line_index]

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
    def capture(self, line_index, num_lines, column_index, num_columns):
        if line_index < self.line_index:
            self.line_index = line_index
        if column_index < self.column_index:
            self.column_index = column_index
        if line_index >= self.line_index + num_lines:
            self.line_index = line_index - num_lines + 1
        if column_index >= self.column_index + num_columns:
            self.column_index = column_index - num_columns + 1

class ScreenRefresher:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
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

def capture_cursor(screen, cursor, screen_offset):
    cursor_line_index = cursor.get_line_index()
    cursor_column_index = cursor.get_column_index()
    screen_num_lines = screen.get_num_lines()
    screen_num_columns = screen.get_num_columns()
    screen_offset.capture(cursor_line_index, screen_num_lines, cursor_column_index, screen_num_columns)

def cursor_at_beginning_of_text(cursor):
    if cursor.get_line_index() == 0 and cursor.get_column_index() == 0:
        return True
    return False

def cursor_at_last_line(text, cursor):
    if cursor.get_line_index() == text.get_num_lines() - 1:
        return True
    return False

def cursor_at_end_of_line(text, cursor):
    if cursor.get_column_index() == text.get_line_length(cursor.get_line_index()):
        return True
    return False

def cursor_at_end_of_text(text, cursor):
    if cursor_at_last_line(text, cursor) and cursor_at_end_of_line(text, cursor):
        return True
    return False

class Resize:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def respond(self):
        capture_cursor(self.screen, self.cursor, self.screen_offset)

class MoveCursorUp:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def respond(self):
        if self.cursor.get_line_index() == 0:
            return
        self.cursor.set_line_index(self.cursor.get_line_index() - 1)
        if self.cursor.get_column_index() > self.text.get_line_length(self.cursor.get_line_index()):
            self.cursor.set_column_index(self.text.get_line_length(self.cursor.get_line_index()))
        capture_cursor(self.screen, self.cursor, self.screen_offset)

class MoveCursorDown:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def respond(self):
        if self.cursor.get_line_index() == self.text.get_num_lines() - 1:
            return
        self.cursor.set_line_index(self.cursor.get_line_index() + 1)
        if self.cursor.get_column_index() > self.text.get_line_length(self.cursor.get_line_index()):
            self.cursor.set_column_index(self.text.get_line_length(self.cursor.get_line_index()))
        capture_cursor(self.screen, self.cursor, self.screen_offset)

class MoveCursorLeft:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def respond(self):
        if cursor_at_beginning_of_text(self.cursor):
            return
        if self.cursor.get_column_index() == 0:
            self.cursor.set_line_index(self.cursor.get_line_index() - 1)
            line_length = self.text.get_line_length(self.cursor.get_line_index())
            self.cursor.set_column_index(line_length)
        else:
            self.cursor.set_column_index(self.cursor.get_column_index() - 1)
        capture_cursor(self.screen, self.cursor, self.screen_offset)

class MoveCursorRight:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def respond(self):
        if cursor_at_end_of_text(self.text, self.cursor):
            return
        if cursor_at_end_of_line(self.text, self.cursor):
            self.cursor.set_column_index(0)
            self.cursor.set_line_index(self.cursor.get_line_index() + 1)
        else:
            self.cursor.set_column_index(self.cursor.get_column_index() + 1)
        capture_cursor(self.screen, self.cursor, self.screen_offset)

class DeleteCharacter:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def cursor_at_last_line(self):
        if self.cursor.get_line_index() == self.text.get_num_lines() - 1:
            return True
        return False
    def cursor_at_end_of_line(self):
        if self.cursor.get_column_index() == self.text.get_line_length(self.cursor.get_line_index()):
            return True
        return False
    def cursor_at_end_of_text(self):
        if self.cursor_at_last_line() and self.cursor_at_end_of_line():
            return True
        return False
    def append_next_line_to_current_line(self):
        current_line_index = self.cursor.get_line_index()
        current_line = self.text.get_line(current_line_index)
        next_line = self.text.get_line(current_line_index + 1)
        self.text.set_line(current_line_index, current_line + next_line)
    def delete_next_line(self):
        next_line_index = self.cursor.get_line_index() + 1
        self.text.delete_line(next_line_index)
    def delete_current_character(self):
        current_line_index = self.cursor.get_line_index()
        current_line = self.text.get_line(current_line_index)
        current_character_index = self.cursor.get_column_index()
        new_line = current_line[0:current_character_index] + current_line[current_character_index+1:]
        self.text.set_line(current_line_index, new_line)
    def respond(self):
        if self.cursor_at_end_of_text():
            return
        if self.cursor_at_end_of_line():
            self.append_next_line_to_current_line()
            self.delete_next_line()
            return
        self.delete_current_character()

class Backspace:
    def __init__(self, cursor, move_cursor_left, delete_character):
        self.cursor = cursor
        self.move_cursor_left = move_cursor_left
        self.delete_character = delete_character
    def cursor_at_beginning_of_text(self):
        if self.cursor.get_line_index() == 0 and self.cursor.get_column_index() == 0:
            return True
        return False
    def respond(self):
        if self.cursor_at_beginning_of_text():
            return
        self.move_cursor_left.respond()
        self.delete_character.respond()

class InsertCharacter:
    def __init__(self, text, cursor, move_cursor_right, character):
        self.text = text
        self.cursor = cursor
        self.move_cursor_right = move_cursor_right
        self.character = character
    def respond(self):
        line_index = self.cursor.get_line_index()
        cursor_column = self.cursor.get_column_index()
        line_before_cursor = self.text.get_line(line_index)[0:cursor_column]
        line_after_cursor = self.text.get_line(line_index)[cursor_column:]
        self.text.set_line(line_index, line_before_cursor + self.character + line_after_cursor)
        self.move_cursor_right.respond()

class Insert:
    def __init__(self, text, cursor, move_cursor_right):
        self.text = text
        self.cursor = cursor
        self.move_cursor_right = move_cursor_right
    def insert(self, character):
        line_index = self.cursor.get_line_index()
        cursor_column = self.cursor.get_column_index()
        line_before_cursor = self.text.get_line(line_index)[0:cursor_column]
        line_after_cursor = self.text.get_line(line_index)[cursor_column:]
        self.text.set_line(line_index, line_before_cursor + character + line_after_cursor)
        self.move_cursor_right.respond()

class InsertLine:
    def __init__(self, text, cursor, move_cursor_right):
        self.text = text
        self.cursor = cursor
        self.move_cursor_right = move_cursor_right
    def respond(self):
        line_index = self.cursor.get_line_index()
        cursor_column = self.cursor.get_column_index()
        line_before_cursor = self.text.get_line(line_index)[0:cursor_column]
        line_after_cursor = self.text.get_line(line_index)[cursor_column:]
        self.text.set_line(line_index, line_before_cursor)
        self.text.insert_line(line_index + 1, line_after_cursor)
        self.move_cursor_right.respond()

def API(text, screen, cursor, screen_offset):
    api_new = {
        'move_up': MoveCursorUp(text, screen, cursor, screen_offset),
        'move_down': MoveCursorDown(text, screen, cursor, screen_offset),
        'move_left': MoveCursorLeft(text, screen, cursor, screen_offset),
        'move_right': MoveCursorRight(text, screen, cursor, screen_offset),
        'insert': Insert(text, cursor, MoveCursorRight(text, screen, cursor, screen_offset)),
        'newline': InsertLine(text, cursor, MoveCursorRight(text, screen, cursor, screen_offset)),
        'backspace': Backspace(cursor, MoveCursorLeft(text, screen, cursor, screen_offset), DeleteCharacter(text, screen, cursor, screen_offset)),
        'delete': DeleteCharacter(text, screen, cursor, screen_offset),
        'resize': Resize(text, screen, cursor, screen_offset),
    }
    return api_new

def dispatch_signals(signal_stream, api_new, screen_refresher):
    screen_refresher.refresh()
    while True:
        next_signal = signal_stream.get_next_signal()
        if next_signal == 'UP':
            api_new['move_up'].respond()
        elif next_signal == 'DOWN':
            api_new['move_down'].respond()
        elif next_signal == 'LEFT':
            api_new['move_left'].respond()
        elif next_signal == 'RIGHT':
            api_new['move_right'].respond()
        elif next_signal[0:10] == 'CHARACTER_':
            api_new['insert'].insert(next_signal[-1])
        elif next_signal == 'ENTER':
            api_new['newline'].respond()
        elif next_signal == 'BACKSPACE':
            api_new['backspace'].respond()
        elif next_signal == 'DELETE':
            api_new['delete'].respond()
        elif next_signal == 'RESIZE':
            api_new['resize'].respond()
        screen_refresher.refresh()

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

def start_editor(screen, signal_stream):
    text = Text(POEM)
    cursor = Cursor(text, 12, 5)
    screen_offset = ScreenOffset(text, 4, 3)

    api = API(text, screen, cursor, screen_offset)
    screen_refresher = ScreenRefresher(text, screen, cursor, screen_offset)
    dispatch_signals(signal_stream, api, screen_refresher)

def main():
    try:
        stdscr = curses_open()
        start_editor(CursesScreen(stdscr), CursesSignalStream(stdscr))
    except Exception as e:
        f = open('error_out', 'w')
        f.write('Exception: ' + str(e) + '\n\n')
        f.write('Stack trace: ' + traceback.format_exc())
        f.close()
    finally:
        curses_close(stdscr)

main()
