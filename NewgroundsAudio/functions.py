from urllib.request import urlopen
from urllib.error import HTTPError
from html import unescape
def find(text,start,end,include=False):
  try:
    i=text.index(start)+len(start)
    r=text[i:]
    r=r[:r.index(end)]
    if include:
      r=start+r+end
    return unescape(r)
  except:
    return "NA"
class audio:
  def __init__(self,id):
    self.id=int(id)
    try:
      self.html=urlopen(f"https://www.newgrounds.com/audio/listen/{self.id}").read().decode()
      self.exists=True
      self.name=find(self.html,"<title>","<")
      self.author=find(self.html,'"artist":"','"')
      self.genre=find(self.html[self.html.index('data-genre-for="'):],">","<")
      link_find="https:\\/\\/audio.ngfiles.com\\/",".mp3"
      self.download_link=find(self.html,link_find[0],link_find[1],True).replace("\\","")
      if self.download_link=="https://audio.ngfiles.com/NA.mp3":
        self.download_link=None
    except HTTPError as error:
      error=str(error)
      if "404" in error:
        self.exists=False
  def to_dict(self):
    d={}
    l=[
      "id",
      "exists",
      "name",
      "author",
      "genre",
      "download_link",
      ]
    for i in l:
      if hasattr(self,i):
        d[i]=getattr(self,i)
      else:
        d[i]=None
    return d
  def download(self,path):
    r=urlopen(self.download_link)
    with open(path,"wb") as f:
      s=f.write(r.read())
    return s
