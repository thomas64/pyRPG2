
"""
setup.py
"""

from distutils.core import setup
import py2exe

setup(console=['main.py'], requires=['aenum', 'pygame', 'pytmx', 'pyscroll', 'py2exe'])
