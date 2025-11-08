#!/bin/env python3
import hashlib
import os
import requests
from argparse import ArgumentParser
from base64 import b85decode
from MainShortcuts2 import ms
CHUNK_SIZE=1024*1024*4
ERROR_DESC="Коды ошибок:\n0 - успешно\n1 - не удалось скачать часть файлов\n2 - не удалось скачать все файлы"
FORMAT=["MainPlay-TG/DirIndex",1]
INDEX_NAME="mptg-dir-index.json"
SCRIPT_EXTS=["bash","sh"]
log=ms.utils.mini_log
class FakeProgressBar(ms.ObjectBase):
  def increment(self):
    pass
  def update(self,a):
    pass
def get_pbar(enable:bool,completed:int,total:int,**kw):
  if not enable:
    return FakeProgressBar()
  from progressbar import ProgressBar,widgets
  kw["initial_value"]=completed
  kw["max_value"]=total
  kw["min_poll_interval"]=0.5
  kw["widgets"]=[
    widgets.Percentage(),
    " ",
    widgets.SimpleProgress("%(value_s)s/%(max_value_s)s"),
    " ",
  ]
  if ms.advanced.PlatformInfo().is_windows:
    kw["widgets"].append(widgets.Bar("█",left="[",right="]"))
  else:
    kw["widgets"].append(widgets.GranularBar(left="[",right="]"))
  kw["widgets"]+=[
    " ",
    widgets.Timer("%(elapsed)s"),
    " | ",
    widgets.SmoothingETA(
      format_finished='00:00:00',
      format_na='     N/A',
      format_not_started='--:--:--',
      format_zero='00:00:00',
      format='%(eta)08s',
    ),
  ]
  return ProgressBar(**kw)
exist_dirs=set()
class FileInfo:
  session=requests.Session()
  def __init__(self,url:str,path:str,size:int,sha256:bytes):
    self.path:str=path
    self.sha256:bytes=b85decode(sha256) if isinstance(sha256,str) else sha256
    self.size:int=size
    self.url:str=url
  def check(self,check_hash=True):
    if not ms.path.exists(self.path):
      return False
    if os.path.getsize(self.path)!=self.size:
      return False
    if check_hash:
      with open(self.path,"rb") as f:
        hash=hashlib.sha256()
        rf=f.read
        uf=hash.update
        while True:
          chunk=rf(CHUNK_SIZE)
          if not chunk:
            break
          uf(chunk)
        if f.tell()!=self.size:
          return False
      if hash.digest()!=self.sha256:
        return False
    return True
  def download(self,check_hash=True,**kw):
    if self.size==0:
      # Зачем скачивать пустой файл?
      if ms.path.exists(self.path):
        return True
      else:
        with open(self.path,"wb"):
          return True
    if self.check(check_hash):
      return True
    kw.setdefault("session",self.session)
    ms.dir.create(os.path.dirname(self.path),_exists=exist_dirs)
    ms.utils.download_file(self.url+self.path,self.path,**kw)
    return self.check(check_hash)
def download_index(url:str,try_gzip=True,try_lzma=True,**kw)->list[FileInfo]:
  full_url=url+INDEX_NAME
  kw.setdefault("session",FileInfo.session)
  kw["method"]="GET"
  json=None
  if try_lzma:
    try:
      import lzma
      with ms.utils.request(url=full_url+".lzma",**kw) as resp:
        json=lzma.decompress(resp.content)
    except Exception:
      pass
  if try_gzip:
    if json is None:
      try:
        import gzip
        with ms.utils.request(url=full_url+".gz",**kw) as resp:
          json=gzip.decompress(resp.content)
      except Exception:
        pass
  if json is None:
    with ms.utils.request(url=full_url,**kw) as resp:
      json=resp.content
  data=ms.json.decode(json.decode("utf-8"))
  if data["format"][0]!=FORMAT[0]:
    raise Exception("Неподдерживаемый формат %s"%data["format"][0])
  if data["format"][1]>FORMAT[1]:
    raise Exception("Неподдерживаемая версия формата %s"%data["format"][1])
  return [FileInfo(url,*i) for i in data["files"]]
def download_dir(url:str,*,
                 check_hash=True,
                 enable_pbar=False,
                 try_gzip=True,
                 try_lzma=True,
                 ):
  all_files=download_index(url.rstrip("/")+"/",try_gzip,try_lzma)
  downloaded=0
  errored:list[FileInfo]=[]
  need_download:list[FileInfo]=[]
  print("Всего файлов: %s"%len(all_files))
  print("Проверка файлов...")
  with get_pbar(enable_pbar,downloaded,len(all_files)) as pbar:
    for file in all_files:
      try:
        if file.check(check_hash):
          downloaded+=1
        else:
          need_download.append(file)
      except Exception:
        errored.append(file)
      pbar.increment()
  if downloaded:
    print("Загружено: %s"%downloaded)
  if need_download:
    print("Осталось: %s"%len(need_download))
  if errored:
    print("Ошибки: %s"%len(errored))
  if need_download:
    print("Скачивание файлов...")
    with get_pbar(enable_pbar,downloaded,len(all_files)) as pbar:
      for file in need_download:
        try:
          if not file.download(check_hash):
            errored.append(file)
        except Exception:
          errored.append(file)
        downloaded+=1
        pbar.update(downloaded)
  return all_files,errored
def make_script(url:str,path:str,*,
                check_hash=True,
                try_gzip=True,
                try_lzma=True,
                **kw):
  # Проверка формата
  ext=path.split(".")[-1].lower()
  if not ext in SCRIPT_EXTS:
    print("Не поддерживаемый формат скрипта %s"%ext)
    return False
  # Составление списка файлов и папок
  _all_dirs:set[str]=set()
  all_files=download_index(url.rstrip("/")+"/",try_gzip,try_lzma)
  for file in all_files:
    dir=os.path.dirname(file.path)
    if dir:
      _all_dirs.add(dir)
  all_dirs=sorted(_all_dirs,key=lambda i:len(i))
  # Создание скрипта
  import shlex
  lines=[]
  def add_cmd(*args,tabs=0):
    lines.append((" "*tabs*2)+shlex.join(args))
  # Bash
  if ext in ("bash","sh"):
    lines.append("#!/bin/env bash")
    lines.append("# Сгенерировано через https://github.com/MainPlay-TG/SmallAdditions.py/blob/master/FolderDownload/download.py")
    lines.append("# URL: %s"%url)
    lines.append("# Проверка sha256: %s"%str(check_hash).lower())
    add_cmd("echo","Создание папок...")
    for dir in all_dirs:
      add_cmd("mkdir","-p",dir)
    add_cmd("echo","Скачивание файлов...")
    for file in all_files:
      add_cmd("wget","-c","-O",file.path,file.url+file.path)
    if check_hash:
      lines.append('check=true')
      lines.append('for i in "$@";do')
      lines.append('  if [[ "$i" == "--no-check" ]];then')
      lines.append('    check=false')
      lines.append('    break')
      lines.append('  fi')
      lines.append('done')
      lines.append('if [[ "$check" == "true" ]];then')
      add_cmd("echo","Проверка целостности файлов...",tabs=1)
      add_cmd("rm","-f","sha256sums",tabs=1)
      for file in all_files:
        lines.append("  "+shlex.join(["echo","%s  %s"%(file.sha256.hex(),file.path)])+" >> sha256sums")
      add_cmd("sha256sum","-c","sha256sums","--quiet",tabs=1)
      lines.append('else')
      add_cmd("echo","Проверка целостности файлов отключена агрументом",tabs=1)
      lines.append('fi')
    else:
      add_cmd("echo","Проверка целостности файлов отключена при генерации скрипта")
  ms.file.write(path,"\n".join(lines))
  return True
@ms.utils.main_func(__name__)
def main(args=None,**kw):
  if args is None:
    argp=ArgumentParser(description="Скачивание папки по списку файлов в ней",epilog=ERROR_DESC)
    argp.add_argument("--make-script",help="создать скрипт для скачивания (указать путь)")
    argp.add_argument("--no-gzip",action="store_true",help="не скачивать индекс GZIP")
    argp.add_argument("--no-hash",action="store_true",help="не проверять контрольные суммы")
    argp.add_argument("--no-lzma",action="store_true",help="не скачивать индекс LZMA")
    argp.add_argument("-b","--bar",action="store_true",help="отобразить прогресс")
    argp.add_argument("url",help="ссылка на папку для скачивания")
    args=argp.parse_args()
  kw["check_hash"]=not args.no_hash
  kw["try_gzip"]=not args.no_gzip
  kw["try_lzma"]=not args.no_lzma
  if args.make_script:
    if args.bar:
      print("Аргумент -b/--bar не поддерживается с генерацией скрипта")
      return 2
    ok=make_script(args.url,args.make_script,**kw)
    return 0 if ok else 2
  else:
    kw["enable_pbar"]=args.bar
    try:
      all_files,errored=download_dir(args.url,**kw)
    except Exception as exc:
      log("Ошибка скачивания: %s",exc)
      return 2
    if errored:
      if len(all_files)==len(errored):
        log("Не удалось скачать ни один файл")
        return 2
      log("Не удалось скачать файлы:")
      for file in errored:
        log("- %s",file.path)
      log("Попробуйте ещё раз")
      return 1
  return 0