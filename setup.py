"""from distutils.core import setup
import py2exe
setup(console=['subtitle-downloader.py'])

"""

import sys
from subdown_version import __version__
from cx_Freeze import setup, Executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(
    name = "SubDown",
    version=__version__,
    description='Subtitle Downloader',
    long_description='Small program to download subtitles for video',
    url='https://github.com/sainyamkapoor/SubDown',
    author='Sainyam Kapoor',
    author_email='sainyamkapoor@yahoo.com',
    options = {'build_exe': {'init_script':'Console','optimize':'2'}},
    executables = [Executable("subdown.py", base=base)])
