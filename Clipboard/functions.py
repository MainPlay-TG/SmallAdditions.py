import sys,pyperclip
from typing import Union
from time import sleep
from PIL import Image,ImageGrab
__all__=["get","set"]
if sys.platform=="win32":
  import win32clipboard
  from io import BytesIO
  __all__.append("set_img")
  def set_img(img:Image.Image):
    out=BytesIO()
    img.save(out,"BMP")
    data=out.getvalue()[14:]
    out.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB,data)
    win32clipboard.CloseClipboard()
def get()->Union[str,Image.Image]:
  text=pyperclip.paste()
  if text=="":
    img=ImageGrab.grabclipboard()
    if img!=None:
      return img.copy()
  return text
def set(content:Union[str,Image.Image]):
  if type(content)==str:
    pyperclip.copy(content)
  elif type(content)==Image.Image:
    set_img(content)
  else:
    raise TypeError(f"Unknown content type: {type(content)}")
def on_changes(interval:Union[int,float]=0.1):
  old=get()
  while True:
    new=get()
    if old!=new:
      break
    old=new
    sleep(interval)
  return new
