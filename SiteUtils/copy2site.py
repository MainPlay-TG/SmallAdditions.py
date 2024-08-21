import argparse
import os
import sys
try:
  from MainShortcuts2 import ms
except ImportError:
  print("Модуль MainShortcuts2 не установлен. Установите его с помощью команды\n%s -m pip install -U MainShortcuts2"%sys.executable,file=sys.stderr)
  exit(1)
exec(ms.import_code)
DEFAULT_CFG_PATH=os.path.expanduser("~/.config/MainPlaySoft/copy2site.json")
cprint=ms.term.cprint
argp_kw={}
argp_kw["description"]="Копирование файла в папку с сайтом"
argp_kw["epilog"]="от MainPlay TG"
argp_kw["formatter_class"]=argparse.RawTextHelpFormatter
argp_kw["prog"]="copy2site"
argp=argparse.ArgumentParser(**argp_kw)
argp.add_argument("path",
                  help="путь к файлу")
argp.add_argument("-m","--move",
                  action="store_true",
                  help="перемещать файл, а не копировать")
argp.add_argument("-f","--config",
                  default=DEFAULT_CFG_PATH,
                  help="путь к конфиг файлу. По умолчанию %r"%DEFAULT_CFG_PATH,
                  )
args=argp.parse_args()
CFG_PATH=ms.path.Path(args.config)
cfg=ms.cfg(CFG_PATH,type="json")
cfg.default["format"]="%(root)s/files/objects/%(hash)s/%(base_name)s%(ext)s"
cfg.default["hash_type"]="sha1"
cfg.default["site_root"]=None
cfg.default["url"]=None
cfg.dload()
if cfg["site_root"] is None:
  cprint("Отсутствует параметр 'site_root'",file=sys.stderr,start="RED")
  cprint("Запишите в него путь к корневой папке вашего сайта",file=sys.stderr)
  ms.dir.create(CFG_PATH.parent_dir)
  cfg.save()
  cprint("Конфиг файл сохранён в %r"%cfg.path,file=sys.stderr)
  exit(1)
if cfg["url"] is None:
  url="http://127.0.0.1/%(path)s"
  cprint("Отсутствует параметр 'url'",file=sys.stderr,start="YELLOW")
  cprint("Будет использовано значение %r"%url,file=sys.stderr)
else:
  url=cfg["url"]
path=ms.path.Path(args.path)
if not path.is_file:
  cprint("%r не является файлом",file=sys.stderr,start="RED")
  exit(1)
if path.in_dir(cfg["site_root"]):
  relpath=os.path.relpath(path.path,cfg["site_root"])
else:
  import hashlib
  hash=getattr(hashlib,cfg["hash_type"])()
  with open(path.path,"rb") as f:
    for i in f:
      hash.update(i)
  format_data={}
  format_data["base_name"]=path.base_name
  format_data["ext"]=path.ext
  format_data["full_name"]=path.full_name
  format_data["hash"]=hash.hexdigest()
  format_data["root"]=cfg["site_root"]
  dest=cfg["format"]%format_data
  if not os.path.isfile(dest):
    ms.dir.create(os.path.dirname(dest))
    if args.move:
      ms.path.move(path,dest)
    else:
      ms.path.copy(path,dest)
  relpath=os.path.relpath(dest,cfg["site_root"])
print(url%{"path":relpath})
exit(0)
