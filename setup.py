from setuptools import setup
from pathlib import Path
from termtyper.term_typer import VERSION_NUMBER
import platform

def installRequires():
    if platform.system() == 'Windows':
        return ['windows-curses']
    else:
        return []

setup(
    name="termtyper",
    version=VERSION_NUMBER,
    description="A Terminal based typing practice application",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/nagesh1805/termtyper.git",

    author="Naegsh Talagani",
    author_email="nageshmath@gmail.com",
    packages=["termtyper"],
    install_requires= installRequires(),
    package_data = {
        "termtyper":["data/words.json","config.json"]
    },
    entry_points={
        "console_scripts": [
            "termtyper=termtyper.term_typer:run",
        ]
    },
    python_requires=">=3.6",
)