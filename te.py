import sys
import curses
import traceback
from curses_interface import CursesScreen, CursesSignalStream

class Text:
    def __init__(self, text=['']):
        self.text = text
    def get_text(self, line_index, num_lines, column_index, num_columns):
        result = []
        for line in self.text[line_index:line_index + num_lines]:
            result.append(line[column_index:column_index + num_columns])
        return result
    def get_num_lines(self):
        return len(self.text)
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

def refresh(text, screen, cursor, screen_offset):
    text_to_draw = text.get_text(
        screen_offset.get_line_index(),
        screen.get_num_lines(),
        screen_offset.get_column_index(),
        screen.get_num_columns())
    screen.draw(text_to_draw)
    screen.set_cursor_position(
        cursor.get_line_index() - screen_offset.get_line_index(),
        cursor.get_column_index() - screen_offset.get_column_index())

def capture_cursor(screen, cursor, screen_offset):
    cursor_line_index = cursor.get_line_index()
    cursor_column_index = cursor.get_column_index()
    screen_num_lines = screen.get_num_lines()
    screen_num_columns = screen.get_num_columns()
    screen_offset.capture(cursor_line_index, screen_num_lines, cursor_column_index, screen_num_columns)

def snap_cursor_to_text(text, cursor):
    if cursor.get_column_index() > len(text.get_line(cursor.get_line_index())):
        cursor.set_column_index(len(text.get_line(cursor.get_line_index())))

def cursor_at_beginning_of_text(cursor):
    if cursor.get_line_index() == 0 and cursor.get_column_index() == 0:
        return True
    return False

def cursor_at_last_line(text, cursor):
    if cursor.get_line_index() == text.get_num_lines() - 1:
        return True
    return False

def cursor_at_end_of_line(text, cursor):
    if cursor.get_column_index() == len(text.get_line(cursor.get_line_index())):
        return True
    return False

def cursor_at_end_of_text(text, cursor):
    if cursor_at_last_line(text, cursor) and cursor_at_end_of_line(text, cursor):
        return True
    return False

def resize(text, screen, cursor, screen_offset):
    capture_cursor(screen, cursor, screen_offset)

def move_cursor_up(text, screen, cursor, cursor_preferred_column, screen_offset):
    if cursor.get_line_index() == 0:
        return
    cursor.set_line_index(cursor.get_line_index() - 1)
    cursor.set_column_index(cursor_preferred_column)
    snap_cursor_to_text(text, cursor)
    capture_cursor(screen, cursor, screen_offset)

def move_cursor_down(text, screen, cursor, cursor_preferred_column, screen_offset):
    if cursor.get_line_index() == text.get_num_lines() - 1:
        return
    cursor.set_line_index(cursor.get_line_index() + 1)
    cursor.set_column_index(cursor_preferred_column)
    snap_cursor_to_text(text, cursor)
    capture_cursor(screen, cursor, screen_offset)

def move_cursor_left(text, screen, state, cursor, screen_offset):
    if cursor_at_beginning_of_text(cursor):
        return
    if cursor.get_column_index() == 0:
        cursor.set_line_index(cursor.get_line_index() - 1)
        line_length = len(text.get_line(cursor.get_line_index()))
        cursor.set_column_index(line_length)
    else:
        cursor.set_column_index(cursor.get_column_index() - 1)
    capture_cursor(screen, cursor, screen_offset)
    state['cursor']['preferred_column'] = cursor.get_column_index()

def move_cursor_right(text, screen, state, cursor, screen_offset):
    if cursor_at_end_of_text(text, cursor):
        return
    if cursor_at_end_of_line(text, cursor):
        cursor.set_column_index(0)
        cursor.set_line_index(cursor.get_line_index() + 1)
    else:
        cursor.set_column_index(cursor.get_column_index() + 1)
    capture_cursor(screen, cursor, screen_offset)
    state['cursor']['preferred_column'] = cursor.get_column_index()

def insert(text, screen, state, cursor, screen_offset, character):
    line_index = cursor.get_line_index()
    cursor_column = cursor.get_column_index()
    line_before_cursor = text.get_line(line_index)[0:cursor_column]
    line_after_cursor = text.get_line(line_index)[cursor_column:]
    text.set_line(line_index, line_before_cursor + character + line_after_cursor)
    move_cursor_right(text, screen, state, cursor, screen_offset)

def insert_line(text, screen, state, cursor, screen_offset):
    line_index = cursor.get_line_index()
    cursor_column = cursor.get_column_index()
    line_before_cursor = text.get_line(line_index)[0:cursor_column]
    line_after_cursor = text.get_line(line_index)[cursor_column:]
    text.set_line(line_index, line_before_cursor)
    text.insert_line(line_index + 1, line_after_cursor)
    move_cursor_right(text, screen, state, cursor, screen_offset)

def append_next_line_to_current_line(text, cursor):
    current_line_index = cursor.get_line_index()
    current_line = text.get_line(current_line_index)
    next_line = text.get_line(current_line_index + 1)
    text.set_line(current_line_index, current_line + next_line)

def delete_next_line(text, cursor):
    next_line_index = cursor.get_line_index() + 1
    text.delete_line(next_line_index)

def delete_current_character(text, cursor):
    current_line_index = cursor.get_line_index()
    current_line = text.get_line(current_line_index)
    current_character_index = cursor.get_column_index()
    new_line = current_line[0:current_character_index] + current_line[current_character_index+1:]
    text.set_line(current_line_index, new_line)

def delete_character(text, screen, state, cursor, screen_offset):
    if cursor_at_end_of_text(text, cursor):
        return
    if cursor_at_end_of_line(text, cursor):
        append_next_line_to_current_line(text, cursor)
        delete_next_line(text, cursor)
        return
    delete_current_character(text, cursor)
    state['cursor']['preferred_column'] = cursor.get_column_index()

def backspace(text, screen, state, cursor, screen_offset):
    if cursor_at_beginning_of_text(cursor):
        return
    move_cursor_left(text, screen, state, cursor, screen_offset)
    delete_character(text, screen, state, cursor, screen_offset)

def dispatch_signals(signal_stream, text, screen, state, cursor, cursor_preferred_column, screen_offset):
    while True:
        next_signal = signal_stream.get_next_signal()
        if next_signal == 'UP':
            move_cursor_up(text, screen, state, cursor, cursor_preferred_column, screen_offset)
        elif next_signal == 'DOWN':
            move_cursor_down(text, screen, state, cursor, cursor_preferred_column, screen_offset)
        elif next_signal == 'LEFT':
            state['cursor']['preferred_column'] = cursor_preferred_column
            move_cursor_left(text, screen, state, cursor, screen_offset)
            cursor_preferred_column = state['cursor']['preferred_column']
        elif next_signal == 'RIGHT':
            state['cursor']['preferred_column'] = cursor_preferred_column
            move_cursor_right(text, screen, state, cursor, screen_offset)
            cursor_preferred_column = state['cursor']['preferred_column']
        elif next_signal[0:10] == 'CHARACTER_':
            state['cursor']['preferred_column'] = cursor_preferred_column
            insert(text, screen, state, cursor, screen_offset, next_signal[-1])
            cursor_preferred_column = state['cursor']['preferred_column']
        elif next_signal == 'ENTER':
            state['cursor']['preferred_column'] = cursor_preferred_column
            insert_line(text, screen, state, cursor, screen_offset)
            cursor_preferred_column = state['cursor']['preferred_column']
        elif next_signal == 'BACKSPACE':
            state['cursor']['preferred_column'] = cursor_preferred_column
            backspace(text, screen, state, cursor, screen_offset)
            cursor_preferred_column = state['cursor']['preferred_column']
        elif next_signal == 'DELETE':
            state['cursor']['preferred_column'] = cursor_preferred_column
            delete_character(text, screen, state, cursor, screen_offset)
            cursor_preferred_column = state['cursor']['preferred_column']
        elif next_signal == 'RESIZE':
            resize(text, screen, cursor, screen_offset)
        refresh(text, screen, cursor, screen_offset)

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
    text = Text()
    state = {
        'cursor': {
            'preferred_position': 0,
        }
    }
    cursor = Cursor(text, 0, 0)
    cursor_preferred_column = 0
    screen_offset = ScreenOffset(text, 0, 0)
    refresh(text, screen, cursor, screen_offset)
    dispatch_signals(signal_stream, text, screen, state, cursor, cursor_preferred_column, screen_offset)

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
