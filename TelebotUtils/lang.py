import HTML
import MainShortcuts as ms
from typing import Union
from telebot.types import *
class lang:
  def __init__(self,path:str,dl:str="en"):
    self.data={}
    self.dl=dl
    self.path=path
  def __getitem__(self,k):
    return self.data[k]
  def __setitem__(self,k,v):
    self.data[k]=v
  def __call__(self,*ps,**kw)->str:
    if len(ps)==2:
      part="msg"
      name=ps[1]
    elif len(ps)==3:
      part=ps[1]
      name=ps[2]
    else:
      raise Exception("необходимо 2 или 3 аргумента")
    if type(ps[0])==str:
      code=ps[0]
    if type(ps[0])==User:
      code=ps[0].language_code
    if type(ps[0])==Message:
      code=ps[0].from_user.language_code
    if not code in self.data:
      self.data[code]={}
    if not part in self.data[code]:
      self.data[code][part]={}
    if not name in self.data[code][part]:
      self.data[code][part][name]="Текст отсутствует"
      if self.dl!=code:
        return self(self.dl,part,name,**kw)
    if "msg" in part:
      text=HTML.from_list(self.data[code][part][name])
    else:
      text=self.data[code][part][name]
    for k,v in kw.items():
      if "msg" in part:
        text=text.replace(f"#${k}$#",HTML.normal(str(v)))
      else:
        text=text.replace(f"#${k}$#",str(v))
    return text
  def read(self,**kw):
    self.data=ms.json.read(self.path,**kw)
  def write(self,**kw):
    ms.json.write(self.path,self.data,**kw)
  def codes(self)->list:
    r=[]
    for code in self.data:
      r.append(code)
    return r
  def parts(self,codes:Union[str,list]=None)->list:
    r=[]
    if type(codes)==str:
      codes=[codes]
    if codes==None:
      codes=self.codes()
    for code in codes:
      if code in self.data:
        for part in self.data[code]:
          if not part in r:
            r.append(part)
    return r