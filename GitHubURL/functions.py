import os
import requests
from urllib.parse import urlparse


class parse:
  def __init__(self, url: str):
    for i in ["host", "owner", "name", "view", "branch", "file"]:
      setattr(self, i, None)
    parsed = urlparse(url)
    split = parsed.path.split("/")
    self.host = parsed.hostname
    if len(split) > 1:
      self.owner = split[1]
    if len(split) > 2:
      self.name = split[2]
    if len(split) > 3:
      self.view = split[3]
    if len(split) > 4:
      self.branch = split[4]
    if len(split) > 5:
      self.file = "/".join(split[5:])

  def __getitem__(self, k: str):
    return getattr(self, k)

  def __getattr__(self, k: str):
    if k == "repo":
      return f"{self.owner}/{self.name}"
    if k == "args":
      return self.getargs()
    if k == "kwargs":
      return self.getkwargs()
    if k == "url":
      return self.geturl()
    return self.__dict__[k]

  def geturl(self) -> str:
    return "http://{}/{}/{}/{}/{}".format(self.host, self.repo, self.branch, self.view, self.file)

  def getargs(self) -> tuple[str, str, str]:
    return self.repo, self.branch, self.file

  def getkwargs(self) -> dict:
    return {"repo": self.repo, "branch": self.branch, "file": self.file}


class _download:
  def __init__(self):
    self.url = "https://github.com/{r}/raw/{b}/{f}"
    self.chunk_size = 1024 * 8  # 8 КБ
    self.ignore_error = False
    self.request_kwargs = {}

  def _request(self, repo: str, branch: str = None, file: str = None, *, ignore_error: bool = None, **kwargs):
    if type(repo) == parse:
      parsed = repo
      repo = parsed.repo
      branch = parsed.branch
      file = parsed.file
    if branch == None or file == None:
      raise TypeError('provide "branch" and "file" arguments')
    if ignore_error == None:
      ignore_error = self.ignore_error
    request_kwargs = self.request_kwargs
    request_kwargs.update(kwargs)
    r = requests.get(self.url.format(r=repo, b=branch, f=file), **request_kwargs)
    if not ignore_error:
      r.raise_for_status()
    return r

  def bytes(self, *args, **kw):
    return self._request(*args, **kw).content

  def file(self, *args, path: str = None, chunk_size: int = None, **kwargs):
    if path == None:
      if "file" in kwargs:
        path = os.path.basename(kwargs["file"])
      else:
        path = os.path.basename(args[2])
    if chunk_size == None:
      chunk_size = self.chunk_size
    kwargs["stream"] = True
    with open(path, "wb") as f:
      r = self._request(*args, **kwargs)
      for i in r.iter_content(chunk_size):
        if i:
          f.write(i)
    return os.path.getsize(path)


download = _download()
