import key_handlers
import tlib_fake_objects

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
    assert screen.get_data() == [
        'line1          ',
        'this is line2  ',
        'line 3         ',
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
