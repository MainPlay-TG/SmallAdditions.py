import os,requests,sys
from progressbar import ProgressBar,Percentage,Bar,ETA
from urllib.parse import urlparse,unquote
pbar_widgets=[Percentage(),Bar(marker="█",fill="░",left="⟨",right="⟩"),ETA()]
class NoBar:
  def __init__(self):
    for i in ["start","update","finish"]: setattr(self,i,self.none)
  def none(*args,**kwargs): pass
def get_filename(r):
  name=unquote(urlparse(r.url).path).split("/")[-1]
  for k,v in r.headers.items():
    if k.lower()=="content-disposition":
      if "filename=" in v:
        name=v.split("filename=",1)[1].split(";")[0]
  if name.strip()=="":
    name="unnamed.download"
  return os.path.basename(name).strip()
def download_file(url,path=None,*,cli=False,**kwargs):
  kwargs["stream"]=True
  if cli:
    print("Receiving the information...")
  with requests.get(url,**kwargs) as r:
    r.raise_for_status()
    if path==None:
      path=get_filename(r)
    l=0
    name=os.path.basename(path)
    if cli:
      print(f"Downloading file {name}...")
      if "Content-Length" in r.headers:
        file_size=int(r.headers["Content-Length"])
        pbar=ProgressBar(maxval=file_size,widgets=pbar_widgets).start()
      else:
        print("WARN: Could not determine file size",file=sys.stderr)
        file_size=0
        pbar=NoBar()
    with open(path,"wb") as f:
      for chunk in r.iter_content(chunk_size=1024*8): # 8 KB
        if chunk:
          f.write(chunk)
          l+=len(chunk)
          if cli:
            pbar.update(min(file_size,l))
  if cli:
    pbar.finish()
    print("Download complete")
  return r
