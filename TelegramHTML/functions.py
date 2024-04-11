import html
__all__=[
  "bold",
  "code",
  "from_list",
  "hide",
  "italic",
  "link",
  "mono",
  "normal",
  "quote",
  "spoiler",
  "strike",
  "text_mention",
  "underline",
  "url",
  "user",
  "userlink",
  ]
def _id_bot2client(id):
  id=str(id)
  if id.startswith("-100"):
    return int(id[4:])
  elif id.startswith("-"):
    return int(id[1:])
  else:
    return int(id)
def normal(text,escape=True):
  if escape:
    text=html.escape(text)
  return text
def bold(text,escape=True):
  if escape:
    text=html.escape(text)
  return "<b>{}</b>".format(text)
def code(text,lang="",escape=True):
  if escape==True:
    escape=(True,True)
  elif escape==False:
    escape=(False,True)
  elif type(escape)==dict:
    escape=(escape["text"],escape["lang"])
  if escape[0]:
    text=html.escape(text)
  if escape[1]:
    lang=html.escape(lang)
  return '<pre><code class="{}">{}</code></pre>'.format(lang,text)
def italic(text,escape=True):
  if escape:
    text=html.escape(text)
  return "<i>{}</i>".format(text)
def link(text,url,escape=True):
  if escape==True:
    escape=(True,True)
  elif escape==False:
    escape=(False,True)
  elif type(escape)==dict:
    escape=(escape["text"],escape["url"])
  if escape[0]:
    text=html.escape(text)
  if escape[1]:
    url=html.escape(url)
  return '<a href="{}">{}</a>'.format(url,text)
url=link
def mono(text,escape=True):
  if escape:
    text=html.escape(text)
  return "<code>{}</code>".format(text)
def quote(text,escape=True):
  if escape:
    text=html.escape(text)
  return "<blockquote>{}</blockquote>".format(text)
def spoiler(text,escape=True):
  if escape:
    text=html.escape(text)
  return "<tg-spoiler>{}</tg-spoiler>".format(text)
hide=spoiler
def strike(text,escape=True):
  if escape:
    text=html.escape(text)
  return "<s>{}</s>".format(text)
def underline(text,escape=True):
  if escape:
    text=html.escape(text)
  return "<u>{}</u>".format(text)
def user(text,id,*args,**kwargs):
  id=_id_bot2client(id)
  return link(text,f"tg://user?id={id}",*args,**kwargs)
text_mention=user
def userlink(text,id,*args,**kwargs):
  id=_id_bot2client(id)
  return link(text,f"tg://openmessage?user_id={id}",*args,**kwargs)
__dict__=locals()
def from_list(l):
  if type(l)==str:
    return l
  text=""
  for i in l:
    if type(i)==str:
      text+=i
      continue
    if type(i)==list:
      text+=from_list(i)
      continue
    if not "type" in i:
      i["type"]="normal"
    if not "text" in i:
      i["text"]=""
    if not "args" in i:
      i["args"]=()
    if not "kwargs" in i:
      i["kwargs"]={}
    if i["type"] in __all__:
      text+=__dict__[i["type"]](i["text"],*i["args"],**i["kwargs"])
  return text