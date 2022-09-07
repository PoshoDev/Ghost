:: Batch file to build a release.

Echo Managing directories...
rmdir /s /q build
mkdir build
cd build

Echo Auto-Py-to-EXE Stuff...
pyinstaller --noconfirm --onefile --windowed --icon "../icon.ico"  "../ghost.py

Echo Copying icon files...
copy ..\icon.ico dist\icon.ico
copy ..\icon.png dist\icon.png