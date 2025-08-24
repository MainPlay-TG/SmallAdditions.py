import hashlib
import os
from aiohttp.web import FileResponse,Response,Request,json_response
from argparse import ArgumentParser
from MainPlaySoft import MPSoft
from MainShortcuts2 import ms
from MainShortcuts2.core import NoLogger
from MPL.aiohttp_web import AppWrapper,auth_header
FORMAT_VERSION=1
SERVER_VERSION=1
mps=MPSoft("MainPlay_TG","SendFolderWithHTTP")
cfg=ms.cfg(mps.dir.localdata+"/cfg-server.json")
cfg.default["auth.token"]=ms.utils.randstr(32)
cfg.default["hash.type"]="sha512"
cfg.default["listen.host"]="0.0.0.0"
cfg.default["listen.port"]=52374
cfg.default["send.follow_links"]=False
cfg.dload(True)
argp=ArgumentParser()
argp.add_argument("dir",help="папка для отправки")
argp.add_argument("--auth",default=cfg["auth.token"],help="токен для авторизации")
argp.add_argument("--follow-links",action="store_true",default=cfg["send.follow_links"],help="следовать по символическим ссылкам")
argp.add_argument("--hash",default=cfg["hash.type"],help="алгоритм для создания контрольных сумм")
argp.add_argument("--host",default=cfg["listen.host"],help="интерфейс для запуска сервера")
argp.add_argument("--port",default=cfg["listen.port"],type=int,help="порт для запуска сервера")
def get_hash(hash_cls:type[hashlib._Hash],path):
  with open(path,"rb") as f:
    hash=hash_cls()
    for i in f:
      hash.update(i)
  return hash.digest()
def scan_dir(hash_type:str,follow_links:bool):
  files:dict[str,tuple[int,bytes]]={}
  hash_cls=getattr(hashlib,hash_type)
  for root,dirnames,filenames in os.walk(".",followlinks=follow_links):
    for filename in filenames:
      path=root[2:]+"/"+filename
      files[path]=os.path.getsize(path),get_hash(hash_cls,path)
  return files
@ms.utils.main_func(__name__)
def main(args):
  if args is None:
    args=argp.parse_args()
  elif isinstance(args,(list,tuple)):
    args=argp.parse_args(list(args))
  os.chdir(args.dir)
  app=AppWrapper.create(args.host,args.port,log=NoLogger(__name__))
  files=scan_dir(args.hash,args.follow_links)
  @app.on_request("GET","/")
  @auth_header(value=args.auth)
  async def _(req:Request):
    data={}
    data["files"]={}
    data["format.version"]=FORMAT_VERSION
    data["hash"]=args.hash
    data["server.version"]=SERVER_VERSION
    for path in files:
      data["files"][path]=[files[path][0],files[path][1].hex()]
    return json_response(data)
  @app.on_request("GET")
  @auth_header(value=args.auth)
  async def _(req:Request):
    if not req.path[1:] in files:
      return Response(404)
    return FileResponse(req.path[1:])
  app.run()