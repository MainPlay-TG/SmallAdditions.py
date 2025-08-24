import os
import subprocess
import sys
from MainShortcuts2 import ms
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from PyQt6.QtWidgets import *
BUTTON_SIZE=QSize(28,28)
NAME="MinecraftSoundBrowser"
VERSION="1.0"
plat=ms.advanced.get_platform()
cfg=ms.cfg("%s/MainPlay_TG/%s/cfg.json"%(plat.user_config_dir,NAME))
cfg.default["assets_dir"]=os.path.expanduser("~/AppData/Roaming/.minecraft/assets").replace("\\","/")
cfg.dload(True)
class MainWindow(QMainWindow):
  class HeaderBar(QHBoxLayout):
    def __init__(self,mw:"MainWindow"):
      QBoxLayout.__init__(self)
      self.dir_button=QPushButton()
      self.mw=mw
      self.search_line=QLineEdit()
      # Кнопка выбора папки
      self.addWidget(self.dir_button)
      self.dir_button.clicked.connect(self.mw.select_dir)
      self.dir_button.setFixedSize(BUTTON_SIZE)
      self.dir_button.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
      self.dir_button.setToolTip('Выбрать папку "assets"')
      # Строка поиска
      self.addWidget(self.search_line)
      self.search_line.setClearButtonEnabled(True)
      self.search_line.setFixedHeight(BUTTON_SIZE.height())
      self.search_line.setPlaceholderText("Поиск")
      self.search_line.setToolTip("Поиск по названию звука")
      self.search_line.textChanged.connect(self.mw.search)
  class ScrollArea(QScrollArea):
    class ErrorText(QLabel):
      def __init__(self,sa:"MainWindow.ScrollArea"):
        QLabel.__init__(self)
        sa.lt.addWidget(self)
        self.hide()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Arial",18))
        self.setWordWrap(True)
      def show(self,text):
        self.setText(text)
        QLabel.show(self)
    def __init__(self,mw:"MainWindow"):
      QScrollArea.__init__(self)
      self.container=QWidget()
      self.lt=QVBoxLayout(self.container)
      self.error_text=self.ErrorText(self)
      self.mw=mw
      self.lt.setAlignment(Qt.AlignmentFlag.AlignTop)
      self.lt.setContentsMargins(0,0,0,0)
      self.lt.setSpacing(1)
      self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
      self.setWidget(self.container)
      self.setWidgetResizable(True)
  class AudioWidget(QWidget):
    widgets:"dict[str,MainWindow.AudioWidget]"={}
    def __init__(self,mw:"MainWindow",name:str,path:str):
      QWidget.__init__(self)
      self.ao=mw.ao
      self.dir_button=QPushButton()
      self.export_button=QPushButton()
      self.lt=QHBoxLayout(self)
      self.name=name
      self.path=path
      self.play_button=QPushButton()
      self.player=QMediaPlayer()
      self.text=QLabel()
      self.widgets[name]=self
      # Виджет
      self.lt.setContentsMargins(0,0,0,0)
      self.set_background()
      self.setFixedHeight(BUTTON_SIZE.height())
      # Плеер
      self.on_changed(False)
      self.player.playingChanged.connect(self.on_changed)
      self.player.setSource(QUrl.fromLocalFile(path))
      # Кнопка играть/пауза
      self.lt.addWidget(self.play_button)
      self.play_button.clicked.connect(self.play_pause)
      self.play_button.setFixedSize(BUTTON_SIZE)
      self.play_button.setToolTip("Играть/пауза")
      # Название
      self.lt.addWidget(self.text)
      self.text.setText(name)
      self.text.setToolTip(self.path)
      # Кнопка открытия папки
      self.dir_button.clicked.connect(self.open_dir)
      self.dir_button.setFixedSize(BUTTON_SIZE)
      self.dir_button.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
      self.dir_button.setToolTip("Открыть папку с файлом")
      self.lt.addWidget(self.dir_button)
      # Кнопка экспорта
      self.export_button.clicked.connect(self.export)
      self.export_button.setFixedSize(BUTTON_SIZE)
      self.export_button.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditCopy))
      self.export_button.setToolTip("Экспортировать в файл (ffmpeg)")
      self.lt.addWidget(self.export_button)
    @classmethod
    def get(cls,mw:"MainWindow",name:str,path:str):
      if name in cls.widgets:
        return cls.widgets[name]
      return cls(mw,name,path)
    def set_background(self):
      if len(self.widgets)%2==0:
        return
      h,s,l,a=self.palette().color(self.backgroundRole()).getHsl()
      if l>128:
        l-=20
      else:
        l+=20
      self.setStyleSheet("background-color:%s"%QColor.fromHsl(h,s,l,a).name())
    def on_changed(self,status):
      self.play_button.setIcon(QIcon.fromTheme(getattr(QIcon.ThemeIcon,"MediaPlaybackStop" if status else "MediaPlaybackStart")))
    def play_pause(self):
      if self.player.isPlaying():
        self.player.stop()
      else:
        for i in self.widgets.values():
          i.player.stop()
        self.player.setAudioOutput(self.ao)
        self.player.play()
    def open_dir(self,file:str=None):
      if not file:
        file=self.path
      # if sys.platform=="win32":
      #   return subprocess.call(["explorer","/select",file.replace("/","\\")])
      QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(file)))
    def export(self):
      formats=["Все файлы (*)","AAC (*.aac)","FLAC (*.flac)","MP3 (*.mp3)","OGG (*.ogg)","WAV (*.wav)"]
      dest,_=QFileDialog.getSaveFileName(None,"Сохранить аудиофайл","",";;".join(formats))
      if not dest:
        return
      try:
        ms.file.delete(dest)
        subprocess.run(["ffmpeg","-i",self.path,dest],check=True)
        QMessageBox.information(None,"Готово","Файл успешно экспортирован!")
      except Exception as exc:
        QMessageBox.critical(None,"Ошибка","Не удалось экспортировать файл\n%r"%exc)
    def unload(self):
      self.widgets.pop(self.name,None)
      self.dir_button.deleteLater()
      self.export_button.deleteLater()
      self.lt.deleteLater()
      self.play_button.deleteLater()
      self.player.deleteLater()
      self.text.deleteLater()
      self.deleteLater()
  class ShowAllThread(QThread):
    showSignal=pyqtSignal(QWidget)
    def run(self):
      for i in MainWindow.AudioWidget.widgets.values():
        self.showSignal.emit(i)
  class ReloadAudioThread(ShowAllThread):
    addAudioSignal=pyqtSignal(str,str)
    showErrorSignal=pyqtSignal(str)
    def run(self):
      files:dict[str,str]={}
      try:
        for file in ms.dir.list_iter(cfg["assets_dir"]+"/indexes",exts=["json"],type="file"):
          data=ms.json.read(file)
          for name,obj in data["objects"].items():
            if name.startswith("minecraft/sounds/"):
              if name.endswith(".ogg"):
                path=cfg["assets_dir"]+"/objects/"+obj["hash"][:2]+"/"+obj["hash"]
                if os.path.isfile(path):
                  files[name.replace("/",".")[17:-4]]=path
        if not files:
          return self.showErrorSignal.emit("Список пуст. Может лаунчер ещё не скачивал их?")
        for name in sorted(files):
          self.addAudioSignal.emit(name,files[name])
      except Exception as exc:
        return self.showErrorSignal.emit("Ошибка загрузки\n%r"%exc)
  def __init__(self,app:QApplication):
    QMainWindow.__init__(self)
    self.ao=QAudioOutput()
    self.app=app
    self.cw=QWidget()
    self.header=self.HeaderBar(self)
    self.lt=QVBoxLayout(self.cw)
    self.sa=self.ScrollArea(self)
    self.lt.addLayout(self.header)
    self.lt.addWidget(self.sa)
    self.lt.setSpacing(0)
    self.setCentralWidget(self.cw)
    self.setMinimumSize(500,300)
    self.setWindowIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioCard))
    self.setWindowTitle("%s v%s"%(NAME,VERSION))
  @property
  def error_text(self):
    return self.sa.error_text
  def addAudio(self,name:str,path:str):
    self.sa.lt.addWidget(self.AudioWidget.get(self,name,path))
  def search(self,text):
    if not text:
      self.show_all()
    else:
      for i in self.AudioWidget.widgets.values():
        if text.lower() in i.name.lower():
          i.show()
        else:
          i.hide()
  def show_all(self):
    self._show_all_thread=self.ShowAllThread()
    self._show_all_thread.showSignal.connect(self.AudioWidget.show)
    self._show_all_thread.start()
  def select_dir(self):
    new_dir=QFileDialog.getExistingDirectory(None,'Выберите папку "assets" от вашего лаунчера',cfg["assets_dir"])
    if not new_dir:
      return
    if not os.path.isdir(new_dir):
      QMessageBox.critical(None,"Папка не существует","Эта папка не существует. Выберите другую.")
      return self.select_dir()
    if not os.path.isdir(new_dir+"/indexes"):
      QMessageBox.critical(None,"Папка индексов не существует","В этой папке нет папки с индексами. Выберите другую.")
      return self.select_dir()
    if not os.path.isdir(new_dir+"/objects"):
      QMessageBox.critical(None,"Папка объектов не существует","В этой папке нет папки с объектами. Выберите другую.")
      return self.select_dir()
    if new_dir!=cfg["assets_dir"]:
      cfg["assets_dir"]=new_dir.replace("\\","/")
      cfg.save()
    self.reload_audio()
  def reload_audio(self):
    self.error_text.hide()
    for i in list(self.AudioWidget.widgets.values()):
      i.unload()
    if not os.path.isdir(cfg["assets_dir"]):
      return self.error_text.show("Папка не существует")
    if not os.path.isdir(cfg["assets_dir"]+"/indexes"):
      return self.error_text.show("Папка индексов не существует")
    if not os.path.isdir(cfg["assets_dir"]+"/objects"):
      return self.error_text.show("Папка объектов не существует")
    self._reload_audio_thread=self.ReloadAudioThread(self)
    self._reload_audio_thread.addAudioSignal.connect(self.addAudio)
    self._reload_audio_thread.showErrorSignal.connect(self.error_text.show)
    self._reload_audio_thread.start()
@ms.utils.main_func(__name__)
def main():
  app=QApplication(sys.argv)
  mw=MainWindow(app)
  mw.show()
  mw.reload_audio()
  return app.exec()