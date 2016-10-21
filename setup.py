
"""
setup.py
"""

import cx_Freeze

cx_Freeze.setup(
    name="PyRPG2",
    version="0.1",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["resources"]}},
    executables=[cx_Freeze.Executable("main.py")]
)
