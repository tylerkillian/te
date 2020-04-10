def capture_index(interval_start, interval_width, index_to_capture):
    if index_to_capture < interval_start:
        return index_to_capture
    if index_to_capture >= interval_start + interval_width:
        return index_to_capture - interval_width + 1
    return interval_start

def capture_cursor(screen, cursor, screen_offset):
    screen_num_lines = screen.get_num_lines()
    screen_num_columns = screen.get_num_columns()
    screen_offset.set_line_offset(
    return {
        'line_index': capture_index(screen_offset['line_index'], screen_num_lines, cursor['line_index']),
        'column_index': capture_index(screen_offset['column_index'], screen_num_columns, cursor['column_index'])
    }

def snap_cursor_to_text(text, cursor):
    if cursor.get_column_index() > len(text.get_line(cursor.get_line_index())):
        cursor.set_column_index(len(text.get_line(cursor.get_line_index())))

class PressUpArrow:
    def __init__(self, text, screen, cursor, screen_offset, redrawer):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def handle(event):
        if self.cursor.get_line_index() == 0:
            return
        self.cursor.set_line_index(self.cursor.get_line_index() - 1)
        self.cursor.set_column_index(self.cursor.get_preferred_column())
        snap_cursor_to_text(self.text, self.cursor)
        capture_cursor(self.screen, self.cursor, self.screen_offset)
        self.redrawer.redraw()
