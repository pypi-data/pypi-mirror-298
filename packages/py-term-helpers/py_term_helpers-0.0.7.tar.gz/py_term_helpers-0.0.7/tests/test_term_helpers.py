import pytest
from ipdb import set_trace
from src.py_term_helpers import terminal_size, top_wrap, star_line, kv_print
from os import get_terminal_size
# needs the '-s' flag to run with prints

top_wrap("TESTING")


@pytest.fixture
def term_size():
    return get_terminal_size().columns


def test_term_size(term_size):
    print(f'\nterm_size is: {term_size} || test_size:{terminal_size()}')
    assert term_size is terminal_size()


def test_star_line():
    line_1 = star_line()
    line_2 = star_line("-")
    assert (line_1[0] and line_1[-1]) == "*"
    assert (line_2[0] and line_2[-1]) == "-"


def test_kv_print():
    my_dict = {"key": "value"}
    test_print = kv_print(my_dict)
    assert isinstance(test_print, str)
    splited = test_print.split("=>")
    assert "my_dict" in splited[0]
    assert ('key' and 'value') in splited[1]
