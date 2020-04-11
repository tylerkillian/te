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
    cursor = Cursor(1, 1, 1)
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
    assert screen_offset.get_line_offset() == 0
    assert screen_offset.get_column_offset() == 0

def test_press_up_arrow_top_of_screen():
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
    cursor = Cursor(0, 1, 1)
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
    assert screen_offset.get_line_offset() == 0
    assert screen_offset.get_column_offset() == 0

def test_press_up_arrow_move_to_shorter_line():
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
    cursor = Cursor(0, 7, 7)
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
    print(cursor.get_column_index())
    assert cursor.get_column_index() == 5
    assert screen_offset.get_line_offset() == 0
    assert screen_offset.get_column_offset() == 0


test_press_up_arrow_normal()
test_press_up_arrow_top_of_screen()
test_press_up_arrow_move_to_shorter_line()
