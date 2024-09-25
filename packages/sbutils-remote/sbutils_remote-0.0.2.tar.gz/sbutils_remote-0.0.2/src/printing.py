import os
import textwrap
from getpass import getpass

if os.name == 'nt':
    os.system('color')

_indent_stack = []
_close_stack = []
_print = print
_input = input


def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


RESET = '\033[0m'
RED = get_color_escape(239, 51, 77)
GREEN = get_color_escape(6, 180, 120)
BLUE = get_color_escape(17, 138, 178)
YELLOW = get_color_escape(255, 209, 102)
MAGENTA = get_color_escape(170, 74, 178)
CYAN = get_color_escape(108, 200, 230)
ORANGE = get_color_escape(255, 127, 17)
WHITE = get_color_escape(255, 255, 255)

colors = {
    '🟥': RED,
    '🟧': ORANGE,
    '🟨': YELLOW,
    '🟩': GREEN,
    '⏹': CYAN,
    '🟦': BLUE,
    '🟪': MAGENTA,
    '⬜': WHITE,
    '⬛': RESET
}


class IndentManager:

    def indent(self, indent: str = '    ', close=''):
        _indent_stack.append(indent)
        _close_stack.append(close)

    def dedent(self):
        _indent_stack.pop()
        _close_stack.pop()

    def __enter__(self):
        _indent_stack.append(self._next_indent)
        _close_stack.append(self._next_close)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _indent_stack.pop()
        _print(_close_stack.pop(), end='')

    def _color(self, text):
        colored = False
        for color, escape in colors.items():
            if color in text:
                text = text.replace(color, escape)
                colored = True

        if colored:
            text += RESET
        return text

    def __call__(self, *args, indent: str = '    ', close='', **kwargs):
        text = ' '.join(map(str, args))
        text = self._color(text)
        text = textwrap.indent(text, ''.join(_indent_stack))
        _print(text, **kwargs)
        self._next_indent = indent
        self._next_close = close
        return self

    def input(self, prompt: str = '', password: bool = False):
        prompt = textwrap.indent(prompt, ''.join(_indent_stack))
        prompt = self._color(prompt)
        if password:
            return getpass(prompt)
        return _input(prompt)


_inter = IndentManager()
print = _inter
input = print.input
