"""setuptools build script for ltgui Python bindings.

Uses pybind11 + CMake to build _ltgui native module.
Cross-platform: auto-detects Windows/Linux/macOS toolchains.

Usage:
    pip install .                    # build + install
    python setup.py build_ext        # build only
    python setup.py develop          # editable install

Environment variables:
    LTGUI_ROOT   — path to ltgui C++ library (default: ../ltgui)
"""

import os
import sys
import subprocess
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


def find_ltgui_root():
    """Find ltgui C++ library root directory."""
    candidates = [
        os.environ.get("LTGUI_ROOT"),
        os.path.join(os.path.dirname(__file__), "..", "ltgui"),
        os.path.join(os.path.dirname(__file__), "..", "..", "ltgui"),
        "D:/code/ltgui",
    ]
    for c in candidates:
        if not c:
            continue
        c = os.path.normpath(os.path.abspath(c))
        if os.path.isfile(os.path.join(c, "ltgui.py")) and os.path.isdir(
            os.path.join(c, "include")
        ):
            if c == candidates[-1]:
                print(f"[ltgui] WARNING: using fallback path {c}")
            return c
    raise RuntimeError(
        "Could not find ltgui C++ library.\n"
        "Set LTGUI_ROOT environment variable.\n"
        "Clone: git clone https://github.com/jiaheng0815/ltgui.git"
    )


LTGUI_ROOT = find_ltgui_root()


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        ext_dir = Path(self.get_ext_fullpath(ext.name)).parent.absolute()
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DLTGUI_ROOT={LTGUI_ROOT}",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        build_dir = Path(self.build_temp).absolute()
        os.makedirs(build_dir, exist_ok=True)

        subprocess.run(
            ["cmake", str(Path(__file__).parent), *cmake_args],
            cwd=str(build_dir), check=True,
        )
        subprocess.run(
            ["cmake", "--build", ".", "--config", "Release"],
            cwd=str(build_dir), check=True,
        )


setup(
    ext_modules=[CMakeExtension("ltgui._ltgui")],
    cmdclass={"build_ext": CMakeBuild},
)
