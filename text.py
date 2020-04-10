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
