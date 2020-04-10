import te

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
