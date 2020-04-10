import te

def get_default_text():
    return te.Text([
        'line1',
        'this is line2',
        'line 3'
    ]

def get_default_state():
    return {
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

def test_move_cursor_up_normal():
    text = get_default_text()
    te.move_cursor_up(text, screen, state, cursor) 
    assert state == {
        'line_index': 
    } 
