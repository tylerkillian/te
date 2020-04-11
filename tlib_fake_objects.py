class FakeScreen:
    def __init__(self, data):
        num_lines = len(data)
        num_columns = len(data[0])
        self.data = []
        for line_index in range(0, num_lines):
            self.data.append([' '] * num_columns)
            assert len(data[line_index]) == num_columns
            for column_index, character in enumerate(data[line_index]):
                self.data[line_index][column_index] = character
    def erase(self):
        for line_index, line in enumerate(self.data):
            for column_index in range(0, len(line)):
                line[column_index] =  ' '
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
    def get_data(self):
        result = []
        for line in self.data:
            result.append(''.join(line))
        return result
