from distutils.core import setup
import py2exe

setup(
    console=["main.py"],
    name="Tangente Neomatik",
    version="1.0",
    author="Leopold Michael",
    # author_email=""
    url="https://github.com/MrHxID/Watch",
    download_url="https://github.com/MrHxID/Watch",
    packages=["src"],
    data_files=[
        ("bitmaps", ["assets/logo.ico", "assets/Sprites.png"]),
    ],
)
