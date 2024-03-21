import sys,colorsys
from functions import rgb_bg,reset
from os import get_terminal_size
from PIL import Image
def getpixel(img,x,y):
  r,g,b,a=img.getpixel((x,y))
  hsv=list(colorsys.rgb_to_hsv(r,g,b))
  hsv[2]*=a/255
  r,g,b=colorsys.hsv_to_rgb(*hsv)
  return reset+rgb_bg(int(r),int(g),int(b))+"  "+reset
img=Image.open(sys.argv[1])
if img.size[0]*2>get_terminal_size()[0]:
  print("Ширина терминала слишком маленькая, картинка может выглядеть неправильно",file=sys.stderr)
lines=[]
for y in range(img.size[1]):
  line=[]
  for x in range(img.size[0]):
    line.append(getpixel(img,x,y))
  lines.append("".join(line))
for i in lines:
  print(i)