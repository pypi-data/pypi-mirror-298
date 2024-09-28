import subprocess

from rich import print
from rich.padding import Padding


def message(s, padding=None, indent: int = 0):
    if indent:
        s = Padding.indent(s, indent)

    if padding == "around":
        s = Padding(s, pad=(1, 2, 1, 2))
    elif padding == "above":
        s = Padding(s, pad=(1, 2, 0, 2))
    elif padding == "below":
        s = Padding(s, pad=(0, 2, 1, 2))

    print(s)


def color(s, color):
    return f"[bold {color}]{s}[/]"


def cmd(args):
    return subprocess.run(args, check=True, capture_output=True, encoding="utf-8")
