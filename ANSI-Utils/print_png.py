import sys
import colorsys
from functions import rgb_bg, reset
from os import get_terminal_size
from PIL import Image


def getpixel(img: Image.Image, x: int, y: int):
  r, g, b, a = img.getpixel((x, y))
  hsv = list(colorsys.rgb_to_hsv(r, g, b))
  hsv[2] *= a / 255
  r, g, b = colorsys.hsv_to_rgb(*hsv)
  return reset + rgb_bg(int(r), int(g), int(b)) + "  " + reset


img = Image.open(sys.argv[1])
if img.size[0] * 2 > get_terminal_size()[0]:
  print("\u0428\u0438\u0440\u0438\u043d\u0430 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u0430 \u0441\u043b\u0438\u0448\u043a\u043e\u043c \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0430\u044f, \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u043c\u043e\u0436\u0435\u0442 \u0432\u044b\u0433\u043b\u044f\u0434\u0435\u0442\u044c \u043d\u0435\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e", file=sys.stderr)
lines = []
for y in range(img.size[1]):
  line = []
  for x in range(img.size[0]):
    line.append(getpixel(img, x, y))
  lines.append("".join(line))
for i in lines:
  print(i)
