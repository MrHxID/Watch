pyinstaller installer.py --clean ^
    --windowed ^
    --onefile ^
    --name "Installer" ^
    --add-data "assets\icon.ico;assets" ^
    --add-data "assets\Sprites.png;assets" ^
    --add-data "settings\settings.json;settings" ^
    --icon "assets\icon.ico" ^
