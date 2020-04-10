def refresh(text, screen, state, cursor):
    text_to_draw = text.get_text(
        state['screen_offset']['line_index'],
        screen.get_num_lines(),
        state['screen_offset']['column_index'],
        screen.get_num_columns())
    screen.draw(text_to_draw)
    screen.set_cursor_position(
        cursor.get_line_index() - state['screen_offset']['line_index'],
        cursor.get_column_index() - state['screen_offset']['column_index'])
