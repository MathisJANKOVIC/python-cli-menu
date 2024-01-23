from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme_content = readme_file.readlines()

del readme_content[4:20] # remove screen, badges and installation part
del readme_content[0:2] # remove title

long_description = "".join(readme_content)

setup(
    name = "python-cli-menu",
    version = '1.8',
    license = "MIT",
    author = "Rasting (Mathis Jankovic)",
    author_email = "mathis.jankovic@gmail.com",
    description = "A simple cross-platform module to create pretty menu in console",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    keywords = ["python", "menu", "console", "cli", "command", "line"],
    url = "https://github.com/MathisJANKOVIC/py-cli-menu",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ]
)
