from setuptools import setup, find_packages

setup(
    name="pyconsolemenu",
    version='0.1',
    author="Rasting (Mathis Jankovic)",
    author_email="mathis.jankovic@gmail.com",
    description="A module for console GUI menu creation and customization",
    long_description="""py-console-menu is a module for Windows that allows you to easilly create custom graphical user interface menu in the console,
    customize the title, options, cursor color, title/options colors and much more.""",
    packages=find_packages(),
    keywords=['python', 'menu', 'console', 'gui'],
    url="https://github.com/MathisJANKOVIC/Py-Console-Menu",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        "Operating System :: Microsoft :: Windows"
    ]
)
