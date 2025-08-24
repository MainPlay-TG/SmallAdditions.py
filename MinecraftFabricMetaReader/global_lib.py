import zipfile
from MainShortcuts2 import ms
from typing import IO
DONT_CHECK_DEPENDS=[
  "fabric",
  "fabricloader",
  "java",
  "minecraft",
  ]
class ENVIRONMENT:
  ALL="*"
  CLIENT="client"
  SERVER="server"
# https://wiki.fabricmc.net/documentation:fabric_mod_json
class _BaseModFile(ms.ObjectBase):
  def _init(self,loaded_mods=None):
    self._icon_bytes=None
    self._jars=None
    self.loaded_mods:dict[str,_BaseModFile]={} if loaded_mods is None else loaded_mods
    with self.open_zip() as zip:
      self.meta:dict=ms.json.decode(zip.read("fabric.mod.json").decode("utf-8"))
    assert self.meta["schemaVersion"]==1
    self.authors:list[str|dict]=self.meta.get("authors",[])
    self.custom:dict=self.meta.get("custom",{})
    self.depends:dict[str,str]=self.meta.get("depends",{})
    self.description:None|str=self.meta.get("description")
    self.environment:str=self.meta.get("environment","*")
    self.icon_path:None|str|dict[str,str]=self.meta.get("icon")
    self.id:str=self.meta["id"]
    self.name:str=self.meta.get("name",self.meta["id"])
    self.version:str=self.meta["version"]
    self.loaded_mods[self.id]=self
  @property
  def icon_bytes(self)->None|bytes:
    if self.icon_path is None:
      return
    if self._icon_bytes is None:
      assert isinstance(self.icon_path,str)
      with self.open_zip() as zip:
        self._icon_bytes=zip.read(self.icon_path)
    return self._icon_bytes
  @property
  def jars(self)->"list[NestedModFile]":
    """Вложенные моды"""
    if self._jars is None:
      jars=[]
      with self.open_zip() as zip:
        for i in self.meta.get("jars",[]):
          with zip.open(i["file"],"r") as f:
            with NestedModFile(f,loaded_mods=self.loaded_mods) as mod:
              jars.append(mod)
      self._jars=jars
    return self._jars
  def check_depends(self,*,_missing=None)->list[str]:
    missing=[] if _missing is None else _missing
    for i in self.jars:
      i.check_depends(_missing=missing)
    for i in self.depends:
      if not i in DONT_CHECK_DEPENDS:
        if not i in self.loaded_mods:
          if not i in missing:
            missing.append(i)
    return missing
  def open_zip(self,**kw)->zipfile.ZipFile:
    raise NotImplementedError()
class ModFile(_BaseModFile):
  def __init__(self,path:str,**kw):
    self.path=ms.path.Path(path,False)
    self._init(**kw)
  def open_zip(self,**kw):
    kw["file"]=self.path
    kw["mode"]="r"
    return zipfile.ZipFile(**kw)
class NestedModFile(_BaseModFile):
  def __init__(self,f,**kw):
    self.f:IO[bytes]=f
    self._init(**kw)
    _=self.jars
  def close(self):
    self.f.close()
  def open_zip(self,**kw):
    kw["file"]=self.f
    kw["mode"]="r"
    return zipfile.ZipFile(**kw)
def load_mods_dir(dir:str,**kw)->dict[str,_BaseModFile]:
  kw.setdefault("loaded_mods",{})
  for i in ms.dir.list(dir,exts=["jar"],type="file"):
    ModFile(i,**kw)
  return kw["loaded_mods"]