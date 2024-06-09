import os
import telebot
import MainShortcuts as ms
from hashlib import sha512
from typing import Union
class Assets:
  def __init__(self,bot:telebot.TeleBot,dir:str="assets",upload_chat_id:Union[int,telebot.types.Chat]=None,auto_load:bool=True):
    if type(upload_chat_id)==telebot.types.Chat:
      self.upload_chat_id=upload_chat_id.id
    else:
      self.upload_chat_id=upload_chat_id
    self.bots={}
    self.main_bot=bot.token
    self.dir=os.path.abspath(dir).replace("\\","/")
    ms.dir.create(self.dir+"/objects")
    if auto_load:
      if os.path.isfile(f"{self.dir}/index.json"):
        self.index=ms.json.read(f"{self.dir}/index.json")
      else:
        self.index={}
  def __getitem__(self,k):
    try:
      return self.index[k]
    except KeyError:
      self.index[k]={}
      return self.index[k]
  def __hasitem__(self,k):
    return k in self.index
  def __setitem__(self,k,v):
    self.index[k]=v
  def add_bot(self,bot:telebot.TeleBot,update:bool=False):
    if not bot.token in self.bots:
      self.bots[bot.token]={}
    if (not "bot" in self.bots[bot.token]) or update:
      self.bots[bot.token]["bot"]=bot
    if (not "id" in self.bots[bot.token]) or update:
      self.bots[bot.token]["id"]=bot.get_me().id
    return bot.token
  def get_bot(self,bot:Union[dict,str,int,telebot.Telebot]=None)->dict:
    if bot==None:
      return self.get_bot(self.main_bot)
    if type(bot)==dict:
      if "bot" in bot:
        bot=bot["bot"]
    if type(bot)==telebot.TeleBot:
      self.add_bot(bot)
      bot=bot.token
    if type(bot)==str:
      return self.bots[bot]
    if type(bot)==dict:
      if "id" in bot:
        bot=bot["id"]
    if type(bot)==int:
      for i in self.bots.values():
        if i["id"]==bot:
          return i
  def copy2dir(self,path:str,file_id:str=None,bot:Union[str,int,telebot.Telebot]=None,replace:bool=True,move:bool=False):
    hash=sha512()
    with open(path,"rb") as f:
      for i in f:
        hash.update(i)
    hash_hex=hash.hexdigest()
    file=self[hash_hex]
    if not "file_id" in file:
      file["file_id"]={}
    if file_id:
      bot=self.get_bot(bot)
      try:
        file["file_id"][str(bot["id"])]=bot["bot"].get_file(file_id).file_id
      except Exception:
        pass
    if ms.path.exists(f"{self.dir}/objects/{hash_hex}") and replace:
      ms.path.rm(f"{self.dir}/objects/{hash_hex}")
    if move:
      ms.file.move(path,f"{self.dir}/objects/{hash_hex}")
    else:
      ms.file.copy(path,f"{self.dir}/objects/{hash_hex}")
    file["created"]=os.path.getctime(f"{self.dir}/objects/{hash_hex}")
    file["edited"]=os.path.getmtime(f"{self.dir}/objects/{hash_hex}")
    file["extension"]=None
    file["id"]=hash_hex
    file["name"]=os.path.basename(path)
    file["sha512"]=hash_hex
    file["size"]=os.path.getsize(f"{self.dir}/objects/{hash_hex}")
    if "." in file["name"]:
      file["extension"]=file["name"].split(".")[-1].lower()
  def move2dir(self,path:str,file_id:str=None,bot:Union[str,int,telebot.Telebot]=None,replace:bool=True,copy:bool=False):
    kw={}
    kw["bot"]=bot
    kw["file_id"]=file_id
    kw["move"]=not copy
    kw["path"]=path
    kw["replace"]=replace
    return self.copy2dir(**kw)
  def save(self,**kw):
    kw["path"]=f"{self.dir}/index.json"
    kw["data"]=self.index
    return ms.json.write(**kw)
  def load(self,**kw):
    kw["path"]=f"{self.dir}/index.json"
    self.index=ms.json.read(**kw)
    for k,v in self.index.items():
      v["id"]=k
    return self.index
  def get(self,id:Union[str,dict],bot:Union[str,int,telebot.Telebot]=None)->Union[None,dict]:
    if type(id)==dict:
      id=id.get("id")
    if self[id]!={}:
      file=self[id].copy()
      try:
        bot=self.get_bot(bot)
        file["file"]=bot["bot"].get_file(file["file_id"][str(bot["id"])]).file_id
      except Exception:
        if os.path.isfile("{}/objects/{}".format(self.dir,file["sha512"])):
          file["file"]=open("{}/objects/{}".format(self.dir,file["sha512"]),"rb")
      if "file" in file:
        return file
  def search(self,id:Union[str,dict]=None,name:str=None,file_id:str=None,bot:Union[str,int,telebot.Telebot]=None,only_first:bool=False)->Union[None,dict,list[dict]]:
    r=[]
    if type(id)==dict:
      id=id.get("id")
    if id:
      file=self.get(id,bot=bot)
      if file:
        if only_first:
          return file
        r.append(file)
    if file_id:
      bot=self.get_bot(bot)
    for k,v in self.index.items():
      if name:
        if v["name"]==name:
          file=self.get(k,bot=bot)
          if file:
            if only_first:
              return file
            r.append(file)
      if file_id:
        if v["file_id"]==file_id:
          file=self.get(k,bot=bot)
          if file:
            if only_first:
              return file
            r.append(file)
    return r
  def set_file_id(self,id:Union[str,dict],file_id:Union[str,telebot.types.File],bot:Union[str,int,telebot.Telebot]=None):
    bot=self.get_bot(bot)
    if type(id)==dict:
      id=id.get("id")
    if type(file_id)==telebot.types.File:
      file_id=file_id.file_id
    file=self.index[id]
    if not "file_id" in file:
      file["file_id"]={}
    file["file_id"][str(bot["id"])]=file_id
  def upload(self,id:Union[str,dict],chat_id:Union[int,telebot.types.Chat]=None,bot:Union[str,int,telebot.Telebot]=None,**kw)->telebot.types.Message:
    if type(id)==dict:
      id=id.get("id")
    bot=self.get_bot(bot)
    if chat_id==None:
      chat_id=self.upload_chat_id
    if type(chat_id)==telebot.types.Chat:
      chat_id=chat_id.id
    file=self[id]
    with open("{}/objects/{}".format(self.dir,file["sha512"]),"rb") as f:
      if "name" in file:
        kw["visible_file_name"]=file["name"]
      if not "disable_notification" in kw:
        kw["disable_notification"]=True
      kw["chat_id"]=chat_id
      kw["document"]=f
      msg=bot["bot"].send_document(**kw)
    self.set_file_id(file,msg.document,bot)
    return msg