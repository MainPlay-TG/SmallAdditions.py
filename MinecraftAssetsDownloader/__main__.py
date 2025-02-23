import os
import progressbar
import sys
from argparse import ArgumentParser
from hashlib import sha1
from MainShortcuts2 import ms
URL="https://resources.download.minecraft.net/"
pbar_w=[progressbar.Percentage(),progressbar.GranularBar(left="(",right=")"),progressbar.ETA(format="%(eta)8s",format_finished="%(elapsed)8s",format_na="     N/A",format_not_started="--:--:--",format_zero="00:00:00")]
argp=ArgumentParser()
argp.add_argument("--no-check",action="store_true",help="не проверять существующие файлы")
argp.add_argument("-o","--output",help="папка \"objects\", в которую нужно загружать файлы")
argp.add_argument("index",help="путь к файлу индекса")
_scheduled_logs=[]
def print_scheduled_logs():
  while len(_scheduled_logs)>0:
    msg,kw=_scheduled_logs.pop(0)
    kw.setdefault("file",sys.stderr)
    print(msg,**kw)
def log(msg,*values,**kw):
  kw.setdefault("file",sys.stderr)
  print(msg%values,**kw)
def schedule_log(msg,*values,**kw):
  _scheduled_logs.append((msg%values,kw))
class AssetFile:
  def __init__(self,raw,dest):
    self.dest:str=dest
    self.sha1:str=raw["hash"]
    self.path:str=dest+"/"+self.sha1[:2]+"/"+self.sha1
    self.size:int=raw["size"]
    self.url:str=URL+self.sha1[:2]+"/"+self.sha1
  def check(self,check_hash:bool=True)->bool:
    if os.path.isfile(self.path):
      if check_hash:
        with open(self.path,"rb") as f:
          hash=sha1()
          for i in f:
            hash.update(i)
        if hash.hexdigest()!=self.sha1:
          ms.file.delete(self.path)
          return False
      return True
    return False
  def download(self)->bool:
    with ms.utils.request("GET",self.url,stream=True) as resp:
      resp.raise_for_status()
      try:
        ms.dir.create(os.path.dirname(self.path))
        with open(self.path,"wb") as f:
          downloaded=0
          hash=sha1()
          for i in resp.iter_content(1024):
            f.write(i)
            hash.update(i)
            downloaded+=len(i)
        if downloaded!=self.size:
          raise ValueError("file size does not match")
        if hash.hexdigest()!=self.sha1:
          raise ValueError("checksum does not match")
      except Exception:
        ms.file.delete(self.path)
        return False
    return True
@ms.utils.main_func(__name__)
def main(args=None):
  if args is None:
    args=argp.parse_args()
  dest=os.path.dirname(os.path.dirname(os.path.realpath(args.index)))+"/objects" if args.output is None else args.output
  log("Папка назначения: %s",dest)
  log("Чтение индекса")
  index=ms.json.read(args.index)
  objects=[AssetFile(i,dest) for i in index["objects"].values()]
  log("Проверка файлов")
  need_download=[]
  pbar=progressbar.ProgressBar(widgets=pbar_w,max_error=False,
    max_value=len(objects),
  )
  pbar.start()
  for obj in objects:
    if not obj.check(not args.no_check):
      need_download.append(obj)
    pbar.update(pbar.value+1)
  pbar.finish()
  log("Скачивание файлов")
  pbar=progressbar.ProgressBar(widgets=pbar_w,max_error=False,
    max_value=len(need_download),
  )
  pbar.start()
  for obj in need_download:
    for i in range(3):
      if obj.download():
        schedule_log("Не удалось скачать %s"%obj.sha1)
        break
    pbar.update(pbar.value+1)
  pbar.finish()
  print_scheduled_logs()
