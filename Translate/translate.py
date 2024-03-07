from translate_shell.translate import translate as _trans
def translate(text,target,source="auto",*args,**kwargs):
  kwargs.update({"target_lang":target,"source_lang":source})
  return _trans(text,*args,**kwargs).results[0].paraphrase