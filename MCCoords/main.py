import MainShortcuts as ms
from time import sleep
from tkinter import *
from functions import *
FPS=30
SIZE_X,SIZE_Y=300,180
root=Tk()
root.title("MCCoords")
root.geometry(f"{SIZE_X}x{SIZE_Y}")
root.resizable(False,False)
def clipboard_set(text:str=None):
  root.clipboard_clear()
  if text!=None:root.clipboard_append(str(text))
def copy_ft1():
  clipboard_set("{x1} {y1} {z1} {x2} {y2} {z2}".format(**ft))
def copy_ft2():
  clipboard_set("x1={x1},y1={y1},z1={z1},x2={x2},y2={y2},z2={z2}".format(**ft))
def copy_sd1():
  clipboard_set("{x} {y} {z} {dx} {dy} {dz}".format(**sd))
def copy_sd2():
  clipboard_set("x={x},y={y},z={z},dx={dx},dy={dy},dz={dz}".format(**sd))
input_kw,btn_kw={},{}
for i1 in "xyz":
  for i2 in "12":
    input_kw[i1+i2]={
      "anchor":CENTER,
      "height":20,
      "width":75,
      }
    input_kw[i1+i2]["x"]={"x":(SIZE_X/2)-75,"y":(SIZE_X/2),"z":(SIZE_X/2)+75}[i1]
    input_kw[i1+i2]["y"]={"1":20,"2":40}[i2]
for i1 in ["ft","sd"]:
  for i2 in "12":
    btn_kw[i1+i2]={
      "anchor":CENTER,
      "height":40,
      "width":120,
      }
    btn_kw[i1+i2]["x"]={"ft":(SIZE_X/2)-75,"sd":(SIZE_X/2)+75}[i1]
    btn_kw[i1+i2]["y"]={"1":SIZE_Y-80,"2":SIZE_Y-40}[i2]
input_x1=Entry(root,justify=CENTER)
input_y1=Entry(root,justify=CENTER)
input_z1=Entry(root,justify=CENTER)
input_x2=Entry(root,justify=CENTER)
input_y2=Entry(root,justify=CENTER)
input_z2=Entry(root,justify=CENTER)
input_x1.place(**input_kw["x1"])
input_y1.place(**input_kw["y1"])
input_z1.place(**input_kw["z1"])
input_x2.place(**input_kw["x2"])
input_y2.place(**input_kw["y2"])
input_z2.place(**input_kw["z2"])
text_error=Label(root,justify=CENTER)
text_error.place(x=SIZE_X/2,y=60,anchor=CENTER)
btn_ft1=Button(root,justify=CENTER,command=copy_ft1)
btn_ft2=Button(root,justify=CENTER,command=copy_ft2)
btn_sd1=Button(root,justify=CENTER,command=copy_sd1)
btn_sd2=Button(root,justify=CENTER,command=copy_sd2)
btn_ft1.place(btn_kw["ft1"])
btn_ft2.place(btn_kw["ft2"])
btn_sd1.place(btn_kw["sd1"])
btn_sd2.place(btn_kw["sd2"])
while True:
  try:
    root.winfo_exists()
  except:
    break
  ft={}
  valuesOK=True
  for k,i in {"x1":input_x1,"y1":input_y1,"z1":input_z1,"x2":input_x2,"y2":input_y2,"z2":input_z2}.items():
    v=i.get().strip()
    if v in ["","-"]:v="0"
    try:
      ft[k]=int(v)
    except:
      valuesOK=False
  if valuesOK:
    text_error["text"]=""
    ft=format_ft(**ft)
    sd=ft2sd(**ft)
    btn_ft1["text"]="{x1} {y1} {z1}\n{x2} {y2} {z2}".format(**ft)
    btn_ft2["text"]="x1={x1},y1={y1},z1={z1}\nx2={x2},y2={y2},z2={z2}".format(**ft)
    btn_sd1["text"]="{x} {y} {z}\n{dx} {dy} {dz}".format(**sd)
    btn_sd2["text"]="x={x},y={y},z={z}\ndx={dx},dy={dy},dz={dz}".format(**sd)
  else:
    text_error["text"]="Ошибка: координаты введены неправильно"
    btn_ft1["text"]="- - -\n- - -"
    btn_ft2["text"]="- - -\n- - -"
    btn_sd1["text"]="- - -\n- - -"
    btn_sd2["text"]="- - -\n- - -"
  root.update()
  sleep(1/FPS)