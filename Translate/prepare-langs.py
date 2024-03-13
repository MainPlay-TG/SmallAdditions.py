import MainShortcuts as ms
from progressbar import ProgressBar,Percentage,Bar,ETA
from functions import translate
class pbar_w:
  def __init__(self,text=""):
    self.text=text
  def update(self,pbar):
    return self.text
pbw=pbar_w()
w=[Percentage(),Bar(marker="█",fill="░",left="⟨",right="⟩"),pbw,ETA()]
old=ms.json.read("langs.json")
bl=ms.json.read("bl.json")
new=[]
codes=[]
for i in old:
  codes.append(i["code"])
pbar=ProgressBar(maxval=len(codes)**2,widgets=w)
exit=False
c=-1
print(f"Обработка {len(codes)**2} строк")
pbar.start()
for i in old:
  for code in codes:
    c+=1
    if (code in i["names"]) or ([i["code"],code] in bl):
      pbw.text=" skip "
    else:
      pbw.text=" {}/{} ".format(i["code"],code)
    try:
      pbar.update(c)
    except:
      pass
    if exit:break
    if (code in i["names"]) or ([i["code"],code] in bl):
      pass
    else:
      try:
        i["names"][code]=translate(i["names"]["en"],code,source="en")
      except KeyboardInterrupt:
        exit=True
      except:
        bl.append([i["code"],code])
  new.append(i)
pbar.finish()
new.sort(key=lambda i:i["code"])
ms.json.write("langs.json",new,mode="p")
print('"langs.json" saved')
ms.json.write("bl.json",bl)
