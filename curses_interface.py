import curses

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
