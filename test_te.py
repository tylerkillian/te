import te

class FakeScreen:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.data = []
    def erase(self):
        pass
    def draw(self, data):
        self.erase()
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

def test_move_cursor_up_normal():
    text = te.Text([
        'line1',
        'this is line2',
        'line 3'
    ]
    state = {
        'cursor': {
            'line_index': 0,
            'column_index': 0,
            'preferred_position': 0
        },
        'screen_offset': {
            'line_index': 0,
            'column_index': 0
        }
    }
    te.move_cursor_up(text, screen, state, cursor) 
