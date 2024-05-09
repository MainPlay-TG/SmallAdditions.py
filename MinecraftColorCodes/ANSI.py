reset = "\u001b[0m"


def color(x): return f"\u001b[38;5;{x}m"
def color_bg(x): return f"\u001b[48;5;{x}m"


def up(x): return f"\u001b[{x}A"
def down(x): return f"\u001b[{x}B"
def left(x): return f"\u001b[{x}C"
def right(x): return f"\u001b[{x}D"


clear = "\u001b[2J"


def rgb(r, g, b): return f"\u001b[38;2;{r};{g};{b}m"
def rgb_bg(r, g, b): return f"\u001b[48;2;{r};{g};{b}m"
