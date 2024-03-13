import html
__all__=[
  "bold",
  "code",
  "hide",
  "italic",
  "link",
  "mono",
  "quote",
  "spoiler",
  "strike",
  "underline",
  "url",
  "user",
  "userlink",
  "text_mention",
  ]
def _id_bot2client(id):
  t=str(id)
  if t.startswith("-1"):
    t=t[2:]
  return int(t)
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
