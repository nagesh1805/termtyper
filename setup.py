from setuptools import setup
from pathlib import Path
setup(
    name="termtyper",
    version="1.0.0",
    description="A Terminal based typing practice application",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/nagesh1805/termtyper.git",

    author="Naegsh Talagani",
    author_email="nageshmath@gmail.com",
    packages=["termtyper"],
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