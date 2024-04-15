import ANSI
import MainShortcuts as ms
add={
  "name":"",
  "versions":["bedrock","java"],
  "foreground":{
    "rgb":[],
    "hex":"#",
    },
  "background":{
    "rgb":[],
    "hex":"#",
    },
  "type":"color",
  }
remove=[
  "markdown",
  ]
rgb2hex=lambda r,g,b:"#%02x%02x%02x"%(r,g,b)
def hex2rgb(hex):
  if hex[0]=="#":hex=hex[1:]
  rgb=[]
  for i in [0,2,4]:
    rgb.append(int(hex[i:i+2],16))
  return rgb
def prep_color(color):
  if color["rgb"]==[] and color["hex"]=="#":
    return color
  if color["rgb"]==[]:
    color["rgb"]=hex2rgb(color["hex"])
  if color["hex"]=="#":
    color["hex"]=rgb2hex(*color["rgb"])
  return color
colors=ms.json.read("colors.json")
for id,color in colors.items():
  for k,v in add.items():
    if not k in color:
      color[k]=v
  if color["type"]=="color":
    for k in ["foreground","background"]:
      if k in color:
        color[k]=prep_color(color[k])
    if not "ansi" in color:
      color["ansi"]=ANSI.rgb(*color["foreground"]["rgb"])
    if not "ansi_bg" in color:
      if color["background"]["rgb"]!=[]:
        color["ansi_bg"]=ANSI.rgb_bg(*color["background"]["rgb"])
    if not "html" in color:
      color["html"]=[
        '<font color="{}">'.format(color["foreground"]["hex"]),
        "</font>",
        ]
  else:
    for k in ["foreground","background"]:
      if k in color:
        color.pop(k)
    if hasattr(ANSI,color["name"]):
      v=getattr(ANSI,color["name"])
      if type(v)==str:
        color["ansi"]=v
  color["text"]=f"§{id}"
  for k in remove:
    if k in color:
      color.pop(k)
  colors[id]=color
ms.json.write("colors.json",colors,mode="p")
