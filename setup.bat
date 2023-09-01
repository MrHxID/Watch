pyinstaller main.py --clean ^
    --windowed ^
    --onefile ^
    --name "Tangente Neomatik" ^
    --add-data "assets\icon.ico;assets" ^
    --add-data "assets\Sprites.png;assets" ^
    --add-data "settings\settings.json;settings" ^
    --icon "assets\icon.ico" ^
    --version-file "version main.rc" ^
    --distpath "." ^
    