Notepad Remote App - Compressed Image Build
================================================

What changed
------------
- Pasted and dropped images are auto-compressed before embedding:
  - max width: 800 px
  - JPEG quality: 70 for non-transparent images
  - PNG for transparent images
- Ctrl+Enter / Ctrl+NumpadEnter sends content
- App icon uses notepad_icon.ico

Important
---------
I could not build a real Windows .exe in this environment.
Use the included build_exe.bat on your Windows PC to create it.

How to build the .exe on Windows
--------------------------------
1. Open Command Prompt in this folder
2. Install dependencies:
   pip install -r requirements.txt
3. Install PyInstaller:
   pip install pyinstaller
4. Edit desktop_app.py and set SERVER_URL correctly
5. Build:
   build_exe.bat

Output will be created in:
- dist\NotepadRemote.exe

If you only want to run it with Python
--------------------------------------
1. pip install -r requirements.txt
2. Update SERVER_URL in desktop_app.py
3. Run:
   python desktop_app.py
