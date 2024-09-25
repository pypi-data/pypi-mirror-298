from os import get_terminal_size, system
import inspect
import re

# If in pytest will sometimes throw "OSError: [Errno 25] Inappropriate ioctl for device" on .get_terminal_size()
term_size = 0
try:
    term_size = get_terminal_size().columns
except:
    term_size = 80


def terminal_size():
    return term_size


def top_wrap(string: str, char="*"):
    system("clear")
    term_wrap(string, char)


def term_wrap(string: str, char="*"):
    string, char = str(string), str(char)[0]
    star_line(char)
    center_string_stars(string, char)
    star_line(char)


def star_line(char="*"):
    output = str(char)[0] * term_size
    print(output)
    return output


def center_string_stars(string: str, char="*"):
    string, char = str(string), str(char)[0]
    if len(string) > term_size:
        string[0:term_size - 2]
    half_size = (term_size - len(string) - 2) / 2
    half_stars = char[0] * int(half_size)
    output = f"{half_stars} {string} {half_stars}"
    print(output)
    return output


def kv_print(obj):
    frame = inspect.currentframe()
    try:
        context = inspect.getframeinfo(frame.f_back).code_context
        caller_lines = ''.join([line.strip() for line in context])
        m = re.search(r'kv_print\s*\((.+?)\)$', caller_lines)
        if m:
            key = m.group(1)
            output = f'{key} => {obj}'
            print(output)
            return output
    finally:
        del frame
