pyinstaller installer.py --clean ^
    --windowed ^
    --onefile ^
    --name "Installer" ^
    --add-data "assets\icon.ico;assets" ^
    --icon "assets\icon.ico" ^
    --version-file "version installer.rc" ^
    --distpath "." ^
    