class PressUpArrow:
    def __init__(self, text, screen, cursor, screen_offset):
        self.text = text
        self.screen = screen
        self.cursor = cursor
        self.screen_offset = screen_offset
    def handle():
        if cursor.get_line_index() == 0:
            return
        cursor.set_line_index(cursor.get_line_index() - 1)
        cursor.set_column_index(state['cursor']['preferred_column'])
        state['cursor']['line_index'] = cursor.get_line_index() #temp
        state['cursor']['column_index'] = cursor.get_column_index() #temp
        snap_cursor_to_text(text, state['cursor'])
        state['screen_offset'] = capture_cursor(screen, state['cursor'], state['screen_offset'])
        cursor.set_line_index(state['cursor']['line_index'])
        cursor.set_column_index(state['cursor']['column_index'])
