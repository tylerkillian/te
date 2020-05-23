import sys
import curses
import traceback
from curses_interface import CursesScreen, CursesSignalStream

def replace_line(line_index, new_value):
    def _op(text, cursor):
        text[line_index] = new_value
    return _op

def delete_line(line_index):
    def _op(text, cursor):
        del text[line_index]
    return _op

def insert_line_op(line_index, value):
    def _op(text, cursor):
        text.insert(line_index, value)
    return _op

def move_cursor_op(line_index, column_index):
    def _op(text, cursor):
        cursor['line_index'] = line_index
        cursor['column_index'] = column_index
    return _op

def multiple_ops(ops):
    def _call_ops(text, cursor):
        for op in ops:
            op(text, cursor)
    return _call_ops

def undo(text, screen, cursor, screen_offset, undo_redo_pairs):
    if len(undo_redo_pairs['before']) == 0:
        return
    current_pair = undo_redo_pairs['before'].pop()
    current_pair['undo'](text, cursor)
    undo_redo_pairs['after'].insert(0, current_pair)
    snap_cursor_to_text(text, cursor)
    capture_cursor(screen, cursor, screen_offset)

def redo(text, screen, cursor, screen_offset, undo_redo_pairs):
    if len(undo_redo_pairs['after']) == 0:
        return
    current_pair = undo_redo_pairs['after'].pop(0)
    current_pair['redo'](text, cursor)
    undo_redo_pairs['before'].append(current_pair)
    snap_cursor_to_text(text, cursor)
    capture_cursor(screen, cursor, screen_offset)

def add_undo_redo_pair(undo_redo_pairs, undo_command, redo_command):
    undo_redo_pairs['after'].clear()
    undo_redo_pairs['before'].append({
        'undo': undo_command,
        'redo': redo_command
    })

def pop_undo_redo_pair(undo_redo_pairs):
    undo_redo_pairs['after'].clear()
    last_pair = undo_redo_pairs['before'].pop()
    return last_pair['undo'], last_pair['redo']

def get_section(text, line_index, num_lines, column_index, num_columns):
    result = []
    for line in text[line_index:line_index + num_lines]:
        result.append(line[column_index:column_index + num_columns])
    return result

def join_line(text, cursor, line_index, undo_redo_pairs):
    line_index = cursor['line_index']
    cursor_column = cursor['column_index']
    add_undo_redo_pair(
        undo_redo_pairs,
        multiple_ops([
            replace_line(line_index, text[line_index]),
            insert_line_op(line_index + 1, text[line_index + 1]),
            move_cursor_op(line_index, cursor_column)]),
        multiple_ops([
            replace_line(line_index, text[line_index] + text[line_index + 1]),
            delete_line(line_index + 1),
            move_cursor_op(cursor['line_index'], cursor['column_index'])]))
    text[line_index] = text[line_index] + text[line_index + 1]
    del text[line_index + 1]

def delete_character(text, line_index, column_index, undo_redo_pairs):
    cursor_column = column_index
    add_undo_redo_pair(
        undo_redo_pairs,
        multiple_ops([
            replace_line(line_index, text[line_index]),
            move_cursor_op(line_index, cursor_column)
        ]),
        multiple_ops([
            replace_line(line_index, text[line_index][0:column_index] + text[line_index][column_index+1:]),
            move_cursor_op(line_index, cursor_column)
        ]))
    text[line_index] = text[line_index][0:column_index] + text[line_index][column_index+1:]

def refresh(text, screen, cursor, screen_offset):
    screen.draw(get_section(
        text,
        screen_offset['line_index'],
        screen.get_num_lines(),
        screen_offset['column_index'],
        screen.get_num_columns()))
    screen.set_cursor_position(
        cursor['line_index'] - screen_offset['line_index'],
        cursor['column_index'] - screen_offset['column_index'])

def capture_index(interval_start, interval_width, index_to_capture):
    if index_to_capture < interval_start:
        return index_to_capture
    if index_to_capture >= interval_start + interval_width:
        return index_to_capture - interval_width + 1
    return interval_start

def capture_cursor(screen, cursor, screen_offset):
    screen_num_lines = screen.get_num_lines()
    screen_num_columns = screen.get_num_columns()
    screen_offset['line_index'] = capture_index(screen_offset['line_index'], screen_num_lines, cursor['line_index'])
    screen_offset['column_index'] = capture_index(screen_offset['column_index'], screen_num_columns, cursor['column_index'])

def snap_cursor_to_text(text, cursor):
    if cursor['line_index'] >= len(text):
        cursor['line_index'] = len(text) - 1
    if cursor['column_index'] > len(text[cursor['line_index']]):
        cursor['column_index'] = len(text[cursor['line_index']])

def cursor_on_first_line(cursor):
    return cursor['line_index'] == 0

def cursor_on_last_line(text, cursor):
    return cursor['line_index'] == len(text) - 1

def cursor_at_beginning_of_line(cursor):
    return cursor['column_index'] == 0 

def cursor_at_end_of_line(text, cursor):
    return cursor['column_index'] == len(text[cursor['line_index']])

def cursor_at_beginning_of_text(cursor):
    return cursor_on_first_line(cursor) and cursor_at_beginning_of_line(cursor)

def cursor_at_end_of_text(text, cursor):
    return cursor_on_last_line(text, cursor) and cursor_at_end_of_line(text, cursor) 

def resize(screen, cursor, screen_offset):
    capture_cursor(screen, cursor, screen_offset)

def move_cursor_up(text, screen, cursor, screen_offset):
    if cursor_on_first_line(cursor):
        return
    cursor['line_index'] -= 1
    cursor['column_index'] = cursor['preferred_column']
    snap_cursor_to_text(text, cursor)
    capture_cursor(screen, cursor, screen_offset)

def move_cursor_down(text, screen, cursor, screen_offset):
    if cursor_on_last_line(text, cursor):
        return
    cursor['line_index'] += 1
    cursor['column_index'] = cursor['preferred_column']
    snap_cursor_to_text(text, cursor)
    capture_cursor(screen, cursor, screen_offset)

def move_cursor_left(text, screen, cursor, screen_offset):
    if cursor_at_beginning_of_text(cursor):
        return
    if cursor_at_beginning_of_line(cursor):
        cursor['line_index'] -= 1
        line_length = len(text[cursor['line_index']])
        cursor['column_index'] = line_length
    else:
        cursor['column_index'] -= 1
    cursor['preferred_column'] = cursor['column_index']
    capture_cursor(screen, cursor, screen_offset)

def move_cursor_right(text, screen, cursor, screen_offset):
    if cursor_at_end_of_text(text, cursor):
        return
    if cursor_at_end_of_line(text, cursor):
        cursor['column_index'] = 0
        cursor['line_index'] += 1
    else:
        cursor['column_index'] += 1
    cursor['preferred_column'] = cursor['column_index']
    capture_cursor(screen, cursor, screen_offset)

def insert(text, screen, cursor, screen_offset, character, undo_redo_pairs):
    line_index = cursor['line_index']
    cursor_column = cursor['column_index']
    line_before_cursor = text[line_index][0:cursor_column]
    line_after_cursor = text[line_index][cursor_column:]
    text[line_index] = line_before_cursor + character + line_after_cursor
    move_cursor_right(text, screen, cursor, screen_offset)
    add_undo_redo_pair(
        undo_redo_pairs,
        multiple_ops([
            replace_line(line_index, line_before_cursor + line_after_cursor),
            move_cursor_op(line_index, cursor_column)]),
        multiple_ops([
            replace_line(line_index, line_before_cursor + character + line_after_cursor),
            move_cursor_op(cursor['line_index'], cursor['column_index'])]))
            

def insert_line(text, screen, cursor, screen_offset, undo_redo_pairs):
    line_index = cursor['line_index']
    cursor_column = cursor['column_index']
    line_before_cursor = text[line_index][0:cursor_column]
    line_after_cursor = text[line_index][cursor_column:]
    text[line_index] = line_before_cursor
    text.insert(line_index + 1, line_after_cursor)
    move_cursor_right(text, screen, cursor, screen_offset)
    add_undo_redo_pair(
        undo_redo_pairs,
        multiple_ops([
            delete_line(line_index + 1),
            replace_line(line_index, line_before_cursor + line_after_cursor),
            move_cursor_op(line_index, cursor_column)]),
        multiple_ops([
            replace_line(line_index, line_before_cursor),
            insert_line_op(line_index + 1, line_after_cursor),
            move_cursor_op(cursor['line_index'], cursor['column_index'])]))

def delete(text, cursor, undo_redo_pairs):
    if cursor_at_end_of_text(text, cursor):
        return
    if cursor_at_end_of_line(text, cursor):
        join_line(text, cursor, cursor['line_index'], undo_redo_pairs)
        return
    delete_character(text, cursor['line_index'], cursor['column_index'], undo_redo_pairs)
    cursor['preferred_column'] = cursor['column_index']

def backspace(text, screen, cursor, screen_offset, undo_redo_pairs):
    if cursor_at_beginning_of_text(cursor):
        return
    move_cursor_left(text, screen, cursor, screen_offset)
    delete(text, cursor, undo_redo_pairs)
    undo_command, redo_command = pop_undo_redo_pair(undo_redo_pairs)
    add_undo_redo_pair(undo_redo_pairs, multiple_ops([undo_command, move_cursor_op(cursor['line_index'], cursor['column_index'] + 1)]), redo_command)

def dispatch_signals(signal_stream, text, screen, cursor, screen_offset, undo_redo_pairs):
    while True:
        next_signal = signal_stream.get_next_signal()
        if next_signal == 'UP':
            move_cursor_up(text, screen, cursor, screen_offset)
        elif next_signal == 'DOWN':
            move_cursor_down(text, screen, cursor, screen_offset)
        elif next_signal == 'LEFT':
            move_cursor_left(text, screen, cursor, screen_offset)
        elif next_signal == 'RIGHT':
            move_cursor_right(text, screen, cursor, screen_offset)
        elif next_signal[0:10] == 'CHARACTER_':
            insert(text, screen, cursor, screen_offset, next_signal[-1], undo_redo_pairs)
        elif next_signal == 'ENTER':
            insert_line(text, screen, cursor, screen_offset, undo_redo_pairs)
        elif next_signal == 'BACKSPACE':
            backspace(text, screen, cursor, screen_offset, undo_redo_pairs)
        elif next_signal == 'DELETE':
            delete(text, cursor, undo_redo_pairs)
        elif next_signal == 'RESIZE':
            resize(screen, cursor, screen_offset)
        elif next_signal == 'CTRL-Z':
            undo(text, screen, cursor, screen_offset, undo_redo_pairs)
        elif next_signal == 'CTRL-Y':
            redo(text, screen, cursor, screen_offset, undo_redo_pairs)
        elif next_signal == 'CTRL-C':
            return
        refresh(text, screen, cursor, screen_offset)

def curses_open():
    stdscr = curses.initscr()
    curses.noecho()
    curses.raw()
    stdscr.keypad(True)
    return stdscr

def curses_close(stdscr):
    stdscr.keypad(False)
    curses.noraw()
    curses.echo()
    curses.endwin()

def start_editor(screen, signal_stream):
    text = ['']
    cursor = {
        'line_index': 0,
        'column_index': 0,
        'preferred_position': 0
    }
    screen_offset = {
        'line_index': 0,
        'column_index': 0
    }
    undo_redo_pairs = {
        'before': [],
        'after': []
    }
    refresh(text, screen, cursor, screen_offset)
    dispatch_signals(signal_stream, text, screen, cursor, screen_offset, undo_redo_pairs)

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

if __name__ == '__main__':
    main()
