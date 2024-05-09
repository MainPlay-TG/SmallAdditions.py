from translate_shell.translate import translate as _trans


def translate(text: str, target: str, source: str = "auto", index: int = 0, *args, **kw):
  kw.update({"target_lang": target, "source_lang": source})
  return _trans(text, *args, **kw).results[index].paraphrase
