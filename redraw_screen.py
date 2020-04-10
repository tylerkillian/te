class Redrawer:
    def init__(text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def redraw():
        text_to_draw = self.text.get_text(
            self.screen_offset.get_line_index(),
            self.screen.get_num_lines(),
            self.screen_offset.get_column_index(),
            self.screen.get_num_lines(),
            self.screen.get_num_columns())
        self.screen.draw(text_to_draw)
        self.screen.set_cursor_position(
            self.cursor.get_line_index() - self.screen_offset.get_line_index(),
            self.cursor.get_column_index() - self.screen_offset.get_column_index())
