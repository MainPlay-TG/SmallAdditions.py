reset="\u001b[0m"

color=lambda x:f"\u001b[38;5;{x}m"
color_bg=lambda x:f"\u001b[48;5;{x}m"

up=lambda x:f"\u001b[{x}A"
down=lambda x:f"\u001b[{x}B"
left=lambda x:f"\u001b[{x}C"
right=lambda x:f"\u001b[{x}D"

clear="\u001b[2J"

rgb=lambda r,g,b:f"\u001b[38;2;{r};{g};{b}m"
rgb_bg=lambda r,g,b:f"\u001b[48;2;{r};{g};{b}m"
