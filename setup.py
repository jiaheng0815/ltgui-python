"""setuptools build script for ltgui Python bindings.

Uses pybind11 + CMake to build _ltgui native module.
Cross-platform: auto-detects Windows/Linux/macOS toolchains.

Usage:
    pip install .                    # build + install
    python setup.py build_ext        # build only
    python setup.py develop          # editable install

Environment variables:
    LTGUI_ROOT    — path to ltgui C++ library (default: ../ltgui)
"""

import os
import sys
import subprocess
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


def find_ltgui_root():
    """Find ltgui C++ library root directory."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.environ.get("LTGUI_ROOT"),
        os.path.join(this_dir, "..", "ltgui"),
        os.path.join(this_dir, "..", "..", "ltgui"),
    ]
    for c in candidates:
        if not c:
            continue
        c = os.path.normpath(os.path.abspath(c))
        if os.path.isfile(os.path.join(c, "ltgui.py")) and os.path.isdir(
            os.path.join(c, "include")
        ):
            return c
    tried = "\n  ".join(c for c in candidates if c)
    raise RuntimeError(
        f"Could not find ltgui C++ library. Tried:\n  {tried}\n\n"
        "Set LTGUI_ROOT environment variable or place ltgui-python next to ltgui.\n"
        "Clone: git clone https://github.com/jiaheng0815/ltgui.git"
    )


def find_pybind11_cmake_dir():
    """Locate pybind11 cmake config directory at build time."""
    try:
        import pybind11
        return pybind11.get_cmake_dir()
    except ImportError:
        pass
    # Fallback: search site-packages
    for p in sys.path:
        candidate = os.path.join(p, "pybind11", "share", "cmake", "pybind11")
        if os.path.isdir(candidate):
            return candidate
    raise RuntimeError(
        "pybind11 not found. Install with: pip install pybind11"
    )


LTGUI_ROOT = find_ltgui_root()


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        ext_dir = Path(self.get_ext_fullpath(ext.name)).parent.absolute()
        source_dir = Path(__file__).parent.absolute()
        pb11_dir = find_pybind11_cmake_dir()

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DLTGUI_ROOT={LTGUI_ROOT}",
            f"-Dpybind11_DIR={pb11_dir}",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        # On Windows, prefer Ninja+clang++ to match ltgui's own build.
        # MSVC in an isolated pip env won't find ltgui's clang++-built .lib.
        if sys.platform == "win32":
            cmake_args[0:0] = ["-G", "Ninja"]
            cmake_args += [
                "-DCMAKE_C_COMPILER=clang++",
                "-DCMAKE_CXX_COMPILER=clang++",
            ]

        build_dir = Path(self.build_temp).absolute()
        os.makedirs(build_dir, exist_ok=True)

        subprocess.run(
            ["cmake", str(source_dir)] + cmake_args,
            cwd=str(build_dir), check=True,
        )
        subprocess.run(
            ["cmake", "--build", "."],
            cwd=str(build_dir), check=True,
        )


setup(
    ext_modules=[CMakeExtension("ltgui._ltgui")],
    cmdclass={"build_ext": CMakeBuild},
)
