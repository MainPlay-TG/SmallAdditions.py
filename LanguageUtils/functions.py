import locale
from MainShortcuts.MainCore import os, ms, _MainCore, dictplus
mcore = _MainCore(__name__=__name__, __file__=__file__)
print(locale.getlocale()[0])


def dict_update(old, new):
  out = old.copy()
  new = new.copy()
  for k in new:
    if k in out:
      if type(out[k]) == dict and type(new[k]) == dict:
        out[k] = dict_update(out[k], new[k])
      else:
        out[k] = new[k]
    else:
      out[k] = new[k]
  return out


def dict_flat(d, sep):
  r = {}
  for k, v in d.items():
    if type(v) == dict:
      for k2, v2 in dict_flat(v, sep).items():
        r[k + sep + k2] = v2
    else:
      r[k] = v
  return r


class lang:
  def __init__(self, dir, default={}, *, sep="/", lang=None):
    self.dir = dir
    self.sep = sep
    self.default = default
    if type(lang) == str:
      self.lang = lang
    else:
      self.lang = locale.getlocale()[0]
    ms.dir.create(dir)
    self.file = ms.cfg(f"{dir}/{self.lang}.json")
    self.file.default = {}
    self.file.dload()

  def _fill_missing(self):
    self.texts = dict_flat(dict_update(self.default, self.file.data), sep=self.sep)
