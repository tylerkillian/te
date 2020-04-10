import te

class FakeScreen:
    def __init__(self, num_lines, num_columns):
        self.data = []
        for line_index in range(0, num_lines):
            self.data.append(' ' * num_columns)
    def erase(self):
        for line_index, line in enumerate(self.data):
            for column_index in range(0, len(line)):
                line[column_index] =  ' '
    def draw(self, data):
        self.erase()
        for line_index, line in enumerate(data):
            for character_index, character in enumerate(line):
                self.data[line_index][character_index] = character
    def set_cursor_column(self, line_index, column_index):
        self.cursor_line_index = line_index
        self.cursor_column_index = column_index
    def get_num_lines(self):
        return len(self.data)
    def get_num_columns(self):
        return len(self.data[0])
    def get_data(self):
        return self.data

def initialize(text, screen, state, cursor):
    te.refresh(text, screen, state, cursor)

def test_move_cursor_up_normal():
    text = te.Text([
        'line1',
        'this is line2',
        'line 3'
    ])
    screen = FakeScreen(5, 15)
    state = {
        'cursor': {
            'line_index': 1,
            'column_index': 1,
            'preferred_column': 1
        },
        'screen_offset': {
            'line_index': 0,
            'column_index': 0
        }
    }
    cursor = te.Cursor(text, 1, 1)
    initialize(text, screen, state, cursor)
    te.move_cursor_up(text, screen, state, cursor) 
    print(screen.get_data())
    assert screen.get_data() == [
        'line1          ',
        'this is line2  ',
        'line3          ',
        '               ',
        '               '
    ]
    assert state == {
        'cursor': {
            'line_index': 0,
            'column_index': 1,
            'preferred_column': 1
        },
        'screen_offset': {
            'line_index': 0,
            'column_index': 0
        }
    }

test_move_cursor_up_normal()
