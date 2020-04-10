import te

class FakeScreen:
    def __init__(self, num_lines, num_columns):
        self.data = []
        for line_index in range(0, num_lines):
            self.data.append(' ' * num_columns)
    def erase(self):
        self.data = []
        for line_index in range(0, num_lines):
            self.data.append(' ' * num_columns)
    def draw(self, data):
        self.erase()
        for line_index, line in enumerate(data):
            for character_index, character in enumerate(line):
                self.data[line_index][character_index] = character
    def set_cursor_position(self, line_index, column_index):
        self.cursor_line_index = line_index
        self.cursor_column_index = column_index
    def get_num_lines(self):
        return len(self.data)
    def get_num_columns(self):
        return len(self.data[0])

def test_move_cursor_up_normal():
    text = te.Text([
        'line1',
        'this is line2',
        'line 3'
    ])
    screen = FakeScreen(20, 20)
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
    cursor = te.Cursor(text, 0, 0)
    te.move_cursor_up(text, screen, state, cursor) 

test_move_cursor_up_normal()
