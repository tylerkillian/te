from text import Text
from tlib_fake_objects import FakeScreen
from state import Cursor, ScreenOffset
from redraw_screen import Redrawer
from key_handlers import PressUpArrow

def test_press_up_arrow_normal():
    text = Text([
        'line1',
        'this is line2',
        'line 3'
    ])
    screen = FakeScreen([
        'line1          ',
        'this is line2  ',
        'line 3         ',
        '               ',
        '               '
    ])
    cursor = Cursor(1, 1)
    screen_offset = ScreenOffset(0, 0)
    redrawer = Redrawer(text, screen, cursor, screen_offset)
    up_arrow_pressed = PressUpArrow(text, screen, cursor, screen_offset, redrawer)
    up_arrow_pressed.handle(None)
    assert screen.get_data() == [
        'line1          ',
        'this is line2  ',
        'line 3         ',
        '               ',
        '               '
    ]
    assert cursor.get_line_index() == 0
    assert cursor.get_column_index() == 1
    assert screen_offset.get_line_index() == 0
    assert screen_offset.get_column_index() == 0

test_press_up_arrow_normal()
