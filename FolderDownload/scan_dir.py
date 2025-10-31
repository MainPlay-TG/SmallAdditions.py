#!/bin/env python3
import hashlib
import os
from argparse import ArgumentParser
from base64 import b85encode
from MainShortcuts2 import ms
CHUNK_SIZE=1024*1024*4
ERROR_DESC="Коды ошибок:\n0 - успешно\n1 - не удалось просканировать часть папок\n2 - не удалось просканировать ни одну папку"
FORMAT=["MainPlay-TG/DirIndex",1]
INDEX_NAME="mptg-dir-index.json"
class FileInfo:
  def __init__(self,index:"dict[str,FileInfo]",path:str):
    self._sha256=None
    self.index=index
    self.path=path
    self.size=os.path.getsize(path)
    index[path]=self
  @property
  def sha256(self)->bytes:
    if self._sha256 is None:
      with open(self.path,"rb") as f:
        hash=hashlib.sha256()
        rf=f.read
        uf=hash.update
        while True:
          chunk=rf(CHUNK_SIZE)
          if not chunk:
            break
          uf(chunk)
        self.size=f.tell()
      self._sha256=hash.digest()
    return self._sha256
  @property
  def sha256_b85(self)->str:
    return b85encode(self.sha256).decode("utf-8")
  def to_dict(self)->dict:
    self.sha256
    return {"path":self.path,"sha256":self.sha256_b85,"size":self.size}
  def to_tuple(self)->tuple[str,int,str]:
    self.sha256
    return self.path,self.size,self.sha256_b85
def scan_dir(dir:str,*,
             delete_old=True,
             follow_links=False,
             sort_files=False,
             write_gzip=False,
             write_lzma=False,
             write_raw=True,
             ):
  index:dict[str,FileInfo]={}
  ms.path.cwd(dir,True)
  for root,dirs,files in os.walk(".",followlinks=follow_links):
    for i in files:
      if not i.startswith(INDEX_NAME):
        FileInfo(index,root[2:]+i)
  data={"format":FORMAT}
  data["files"]=[]
  for i in index.values():
    data["files"].append(i.to_tuple())
  if sort_files:
    data["files"].sort(key=lambda i:i[0])
  json=ms.json.encode(data,ensure_ascii=False,sort_keys=True).encode("utf-8")
  index_path=dir+"/"+INDEX_NAME
  if delete_old:
    for i in ("",".gz",".lzma"):
      ms.file.delete(index_path+i)
  if write_raw:
    ms.file.save(index_path,json)
  if write_gzip:
    import gzip
    ms.file.save(index_path+".gz",gzip.compress(json))
  if write_lzma:
    import lzma
    ms.file.save(index_path+".lzma",lzma.compress(json))
@ms.utils.main_func(__name__)
def main(args=None,**kw):
  if args is None:
    argp=ArgumentParser(description="Сканирование папки и сохранение списка файлов",epilog=ERROR_DESC)
    argp.add_argument("--gzip",action="store_true",help="добавить %s.gz (сжатие)"%INDEX_NAME)
    argp.add_argument("--lzma",action="store_true",help="добавить %s.lzma (сильное сжатие)"%INDEX_NAME)
    argp.add_argument("--no-delete-old",action="store_true",help="не удалять старые индексы")
    argp.add_argument("--no-raw",action="store_true",help="не записывать без сжатия")
    argp.add_argument("-f","--follow-links",action="store_true",help="сделовать по символьным ссылкам")
    argp.add_argument("-s","--sort",action="store_true",help="сортировать список файлов")
    argp.add_argument("dirs",help="пути к папкам для сканирования",nargs="+")
    args=argp.parse_args()
  kw["delete_old"]=not args.no_delete_old
  kw["follow_links"]=args.follow_links
  kw["sort_files"]=args.sort
  kw["write_gzip"]=args.gzip
  kw["write_lzma"]=args.lzma
  kw["write_raw"]=not args.no_raw
  log=ms.utils.mini_log
  if args.no_raw:
    if not args.gzip:
      if not args.lzma:
        log("Нужно выбрать хотя бы один способ записи индекса")
        return 2
  errored=0
  scanned=0
  for i in set(args.dirs):
    i=os.path.realpath(i)
    log("Сканирование папки %s",i)
    try:
      scan_dir(i,**kw)
      log("Сканирование завершено!")
      scanned+=1
    except Exception as exc:
      log("Ошибка сканирования: %r",exc)
      errored+=1
  if errored:
    if scanned:
      return 1
    return 2
  return 0