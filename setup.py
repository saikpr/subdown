"""from distutils.core import setup
import py2exe
setup(console=['subtitle-downloader.py'])

"""

import sys
from cx_Freeze import setup, Executable

setup(
    name = "SubDown",
    version = "0.1",
    description = "subtitle-downloader",
    executables = [Executable("subtitle-downloader.py", base = "Win32GUI")])