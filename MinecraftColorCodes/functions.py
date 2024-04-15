import os,json
with open("MC-colors.json","rb") as f:
  colors=json.loads(f.read().decode("utf-8"))
codes={
  "mc:ansi":{},
  }
for id,color in colors.items():
  if "ansi" in color:
    codes["mc:ansi"][color["text"]]=color["ansi"]
def mc_remove(text):
  for id,color in colors.items():
    text=text.replace(color["text"],"")
  return text
def mc2ansi(text):
  for mc,ansi in codes["mc:ansi"].items():
    text=text.replace(mc,ansi)
  return text
def ansi2mc(text):
  for mc,ansi in codes["mc:ansi"].items():
    text=text.replace(ansi,mc)
  return text
