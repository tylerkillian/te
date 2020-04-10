class Cursor:
    def __init__(self, line_index=0, column_index=0, preferred_column_index=0):
        self.line_index = line_index
        self.column_index = column_index
        self.preferred_column_index = preferred_column_index
    def get_line_index(self):
        return self.line_index
    def set_line_index(self, value):
        self.line_index = value
    def get_column_index(self):
        return self.column_index
    def set_column_index(self, value):
        self.column_index = value
    def get_preferred_column_index(self):
        return self.preferred_column_index
    def set_preferred_column_index(self, value):
        self.preferred_column_index = value

class ScreenOffset:
    def __init__(self, line_offset=0, column_offset=0):
        self.line_offset = line_offset
        self.column_offset = column_offset
    def get_line_offset(self):
        return self.line_offset
    def set_line_offset(self, value):
        self.line_offset = value
    def get_column_offset(self):
        return self.column_offset
    def set_column_offset(self, value):
        self.column_offset = value
