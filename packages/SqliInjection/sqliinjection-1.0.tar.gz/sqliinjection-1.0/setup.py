from setuptools import setup

VERSION = '1.0'
DESCRIPTION = 'A Tool to find an Easy Bounty - SQL Injection'
LONG_DESCRIPTION = 'This is a tool used by several security researchers to find SQL Injection.'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SqliInjection",
    version=VERSION,
    author="@Umasankar",
    author_email="<sankar3102004@gmail.com>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'SqliInjection = SqliInjection.main:main',
        ],
    },
    install_requires=['argparse', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)