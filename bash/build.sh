pyinstaller -y --onefile bash.py
cp assets/* dist/bash/
echo 'Скопируйте все файлы из папки "dist/bash" в папку "C:/Windows/System32"'