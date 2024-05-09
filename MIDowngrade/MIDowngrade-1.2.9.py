import os
from MainShortcuts.MainCore import ms, _MainCore, dictplus
from tkinter import filedialog
mcore = _MainCore(__name__=__name__, __file__=__file__)
cprint = mcore.cprint
file = None
try:
  if len(mcore.args) > 1:
    if os.path.isfile(mcore.args[1]):
      file = mcore.args[1]
  if file == None:
    file = filedialog.askopenfilename(
        title="Open project",
        initialdir=os.getcwd(),
        filetypes=(
            ("Mine-imator file", ["*.miproject", "*.miobject"]),
            ("All files", ["*.*"]),
        ),
    )
  cprint(f'Reading file "{file}"...')
  json = ms.json.read(file)
  cprint("Version check...")
  if json["format"] < 32:
    raise Exception("This project is too old")
  cprint("Change version...")
  json["format"] = 32
  if "created_in" in json:
    json["created_in"] = json["created_in"] + " -> 1.2.9"
  else:
    json["created_in"] = "unknown -> 1.2.9"
  cprint("Saving a file...")
  ms.json.write(file, json)
  cprint("Completed!", start="GREEN")
except Exception as e:
  cprint(e, start="RED")
if len(mcore.args) == 1:
  input("Press Enter to close")
