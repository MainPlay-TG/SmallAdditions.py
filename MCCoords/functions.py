from typing import Union


def format_sd(x: Union[int, float], y: Union[int, float], z: Union[int, float], dx: Union[int, float], dy: Union[int, float], dz: Union[int, float]) -> dict:
  '''Изменяет формат "x,y,z,dx,dy,dz" так, чтоб dx, dy и dz были положительными'''
  r = {}
  if dx < 0:
    r["x"] = x + dx
    r["dx"] = dx * (-1)
  else:
    r["x"] = x
    r["dx"] = dx
  if dy < 0:
    r["y"] = y + dy
    r["dy"] = dy * (-1)
  else:
    r["y"] = y
    r["dy"] = dy
  if dz < 0:
    r["z"] = z + dz
    r["dz"] = dz * (-1)
  else:
    r["z"] = z
    r["dz"] = dz
  return r


def format_ft(x1: Union[int, float], y1: Union[int, float], z1: Union[int, float], x2: Union[int, float], y2: Union[int, float], z2: Union[int, float]) -> dict:
  '''Изменяет формат "x1,y1,z1,x2,y2,z2" так, чтоб начальные координаты были минимальными'''
  r = {}
  r["x1"] = min(x1, x2)
  r["y1"] = min(y1, y2)
  r["z1"] = min(z1, z2)
  r["x2"] = max(x1, x2)
  r["y2"] = max(y1, y2)
  r["z2"] = max(z1, z2)
  return r


def ft2sd(x1: Union[int, float], y1: Union[int, float], z1: Union[int, float], x2: Union[int, float], y2: Union[int, float], z2: Union[int, float], format: bool = True) -> dict:
  '''Переводит формат "x1,y1,z1,x2,y2,z2" в формат "x,y,z,dx,dy,dz"'''
  r = {}
  r["x"] = x1
  r["y"] = y1
  r["z"] = z1
  r["dx"] = x2 - x1
  r["dy"] = y2 - y1
  r["dz"] = z2 - z1
  if format:
    return format_sd(**r)
  return r


def sd2ft(x: Union[int, float], y: Union[int, float], z: Union[int, float], dx: Union[int, float], dy: Union[int, float], dz: Union[int, float], format: bool = True) -> dict:
  '''Переводит формат "x,y,z,dx,dy,dz" в формат "x1,y1,z1,x2,y2,z2"'''
  r = {}
  r["x1"] = x
  r["y1"] = y
  r["z1"] = z
  r["x2"] = x + dx
  r["y2"] = y + dy
  r["z2"] = z + dz
  if format:
    return format_ft(**r)
  return r
