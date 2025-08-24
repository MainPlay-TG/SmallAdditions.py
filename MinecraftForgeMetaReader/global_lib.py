import zipfile
from MainShortcuts2 import ms
from typing import IO
DONT_CHECK_DEPENDS=[
  "forge",
  "java",
  "minecraft",
  "minecraftforge",
  "mod_minecraftforge",
  ]
# https://mjaroslav.github.io/book/1.7.10/basics/mod-annotation/
class ModInfo(ms.ObjectBase):
  def __init__(self,meta:dict,loaded_mods=None):
    self.credits:None|str=meta.get("credits")
    self.depends:list[str]=meta.get("dependencies",[])
    self.description:None|str=meta.get("description")
    self.id:str=meta["modid"]
    self.loaded_mods:dict[str,ModInfo]={} if loaded_mods is None else loaded_mods
    self.mcversion:None|str=meta.get("mcversion")
    self.meta:dict=meta
    self.name:str=meta.get("name",self.id)
    self.url:None|str=meta.get("url")
    self.version:None|str=meta.get("version")
    self.loaded_mods[self.id]=self
  def check_depends(self,*,_missing=None)->list[str]:
    missing=[] if _missing is None else _missing
    for i in self.depends:
      if not i.lower() in DONT_CHECK_DEPENDS:
        if not i in self.loaded_mods:
          if not i in missing:
            missing.append(i)
    return missing
class ModFile(ms.ObjectBase):
  def __init__(self,path:str,loaded_mods=None):
    if loaded_mods is None:
      loaded_mods={}
    self.path=ms.path.Path(path,False)
    with self.open_zip() as zip:
      info:list[dict]=ms.json.decode(zip.read("mcmod.info").decode("utf-8"),like_json5=True)
    self.mods=[ModInfo(i,loaded_mods) for i in info if isinstance(i,dict)]
  def check_depends(self,*,_missing=None)->list[str]:
    missing=[] if _missing is None else _missing
    for i in self.mods:
      i.check_depends(_missing=missing)
    return missing
  def open_zip(self,**kw):
    kw["file"]=self.path
    kw["mode"]="r"
    return zipfile.ZipFile(**kw)
def is_mod(path:str):
  file=ms.path.Path(path)
  if file.ext!=".jar":
    return False
  with zipfile.ZipFile(file,"r") as zip:
    return "mcmod.info" in zip.namelist()
def load_mods_dir(dir:str,ignore_errors:bool=False,**kw)->dict[str,ModInfo]:
  kw.setdefault("loaded_mods",{})
  for i in ms.dir.list(dir,exts=["jar"],type="file"):
    try:
      if is_mod(i):
        ModFile(i,**kw)
    except Exception:
      if not ignore_errors:
        raise Exception("Failed to load mod %s"%i.full_name)
  return kw["loaded_mods"]