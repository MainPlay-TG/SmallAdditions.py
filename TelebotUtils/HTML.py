import html
from typing import Union
__all__ = [
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
  id = str(id)
  if id.startswith("-100"):
    return int(id[4:])
  elif id.startswith("-"):
    return int(id[1:])
  else:
    return int(id)


def normal(text: str, escape: bool = True):
  """\u041d\u0435 \u0438\u0437\u043c\u0435\u043d\u044f\u0435\u0442 \u0442\u0435\u043a\u0441\u0442"""
  if escape:
    text = html.escape(text)
  return text


def bold(text: str, escape: bool = True):
  """\u0416\u0438\u0440\u043d\u044b\u0439"""
  if escape:
    text = html.escape(text)
  return "<b>{}</b>".format(text)


def code(text: str, lang: str = "", escape: bool = True):
  """\u0411\u043b\u043e\u043a \u043a\u043e\u0434\u0430"""
  if escape == True:
    escape = (True, True)
  elif escape == False:
    escape = (False, True)
  elif type(escape) == dict:
    escape = (escape["text"], escape["lang"])
  if escape[0]:
    text = html.escape(text)
  if escape[1]:
    lang = html.escape(lang)
  return '<pre><code class="{}">{}</code></pre>'.format(lang.lower(), text)


def italic(text: str, escape: bool = True):
  """\u041a\u0443\u0440\u0441\u0438\u0432"""
  if escape:
    text = html.escape(text)
  return "<i>{}</i>".format(text)


def link(text: str, url: str, escape: bool = True):
  """\u0421\u0441\u044b\u043b\u043a\u0430 \u0432 \u0442\u0435\u043a\u0441\u0442\u0435"""
  if escape == True:
    escape = (True, True)
  elif escape == False:
    escape = (False, True)
  elif type(escape) == dict:
    escape = (escape["text"], escape["url"])
  if escape[0]:
    text = html.escape(text)
  if escape[1]:
    url = html.escape(url)
  return '<a href="{}">{}</a>'.format(url, text)


url = link


def mono(text: str, escape: bool = True):
  """\u041c\u043e\u043d\u043e\u0448\u0438\u0440\u0438\u043d\u043d\u044b\u0439 \u0442\u0435\u043a\u0441\u0442"""
  if escape:
    text = html.escape(text)
  return "<code>{}</code>".format(text)


def quote(text: str, escape: bool = True):
  """\u0426\u0438\u0442\u0430\u0442\u0430"""
  if escape:
    text = html.escape(text)
  return "<blockquote>{}</blockquote>".format(text)


def spoiler(text: str, escape: bool = True):
  """\u0421\u043a\u0440\u044b\u0442\u044b\u0439 \u0442\u0435\u043a\u0441\u0442"""
  if escape:
    text = html.escape(text)
  return "<tg-spoiler>{}</tg-spoiler>".format(text)


hide = spoiler


def strike(text: str, escape: bool = True):
  """\u0417\u0430\u0447\u0451\u0440\u043a\u043d\u0443\u0442\u044b\u0439 \u0442\u0435\u043a\u0441\u0442"""
  if escape:
    text = html.escape(text)
  return "<s>{}</s>".format(text)


def underline(text: str, escape: bool = True):
  """\u041f\u043e\u0434\u0447\u0451\u0440\u043a\u043d\u0443\u0442\u044b\u0439 \u0442\u0435\u043a\u0441\u0442"""
  if escape:
    text = html.escape(text)
  return "<u>{}</u>".format(text)


def user(text: str, id: int, *args, **kw):
  """\u0423\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u0435 \u0432 \u0442\u0435\u043a\u0441\u0442\u0435 \u043f\u043e ID"""
  id = _id_bot2client(id)
  return link(text, f"tg://user?id={id}", *args, **kw)


text_mention = user


def userlink(text: str, id: int, *args, **kw):
  """\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f \u0432 \u0442\u0435\u043a\u0441\u0442\u0435 (\u0431\u0435\u0437 \u0443\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f)"""
  id = _id_bot2client(id)
  return link(text, f"tg://openmessage?user_id={id}", *args, **kw)


__dict__ = locals()


def from_list(l: Union[str, tuple, list]):
  """\u041f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u043f\u0438\u0441\u043a\u0430 \u043e\u0431\u044a\u0435\u043a\u0442\u043e\u0432 \u0432 \u043e\u0442\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u0442\u0435\u043a\u0441\u0442"""
  if type(l) == str:
    return normal(l)
  text = ""
  for i in l:
    if type(i) == str:
      text += normal(i)
      continue
    if type(i) == list:
      text += from_list(i)
      continue
    if not "type" in i:
      i["type"] = "normal"
    if not "text" in i:
      i["text"] = ""
    if not "args" in i:
      i["args"] = ()
    if not "kwargs" in i:
      i["kwargs"] = {}
    if i["type"] in __all__:
      text += __dict__[i["type"]](i["text"], *i["args"], **i["kwargs"])
  return text
