@echo off
cd /d "%~dp0"
echo ひかりメモを起動します。この画面は閉じないでください。
echo ブラウザで http://127.0.0.1:5000/ を開いてください。
echo.
python -m pip install -r requirements.txt
python app.py
pause
