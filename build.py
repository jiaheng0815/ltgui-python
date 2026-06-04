#!/usr/bin/env python3
"""ltgui-python build script — python build.py [build|run <name>|clean] [--ltgui-root <path>]"""

import os
import sys
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(SCRIPT_DIR, "build")

# ---- LTGUI_ROOT resolution ----
# Search order: 1) --ltgui-root flag  2) LTGUI_ROOT env var
#               3) ../ltgui sibling   4) ../../ltgui
#               5) D:/code/ltgui (fallback, prints warning)

def _find_ltgui_root(explicit=None):
    """Resolve the path to the ltgui C++ library."""
    candidates = []

    # 1) Explicit flag
    if explicit:
        candidates.append(explicit)

    # 2) Environment variable
    env_root = os.environ.get("LTGUI_ROOT")
    if env_root:
        candidates.append(env_root)

    # 3) Sibling ../ltgui
    candidates.append(os.path.join(SCRIPT_DIR, "..", "ltgui"))

    # 4) Grandparent ../../ltgui (if this repo is nested)
    candidates.append(os.path.join(SCRIPT_DIR, "..", "..", "ltgui"))

    # 5) Legacy fallback
    candidates.append("D:/code/ltgui")

    for c in candidates:
        c = os.path.normpath(os.path.abspath(c))
        ltgui_py = os.path.join(c, "ltgui.py")
        include_dir = os.path.join(c, "include")
        if os.path.isfile(ltgui_py) and os.path.isdir(include_dir):
            if c == candidates[-1]:
                cprint(f"WARNING: using fallback path {c}", "yellow")
                cprint("  Set LTGUI_ROOT env var or use --ltgui-root to override.", "yellow")
            return c

    cprint("Error: could not find ltgui C++ library.", "red", bold=True)
    cprint("  Tried:", "yellow")
    for c in candidates:
        cprint(f"    {c}", "yellow")
    cprint("  Set LTGUI_ROOT environment variable or use --ltgui-root flag.", "white")
    cprint("  Clone ltgui: git clone https://github.com/jiaheng0815/ltgui.git", "white")
    sys.exit(1)


LTGUI_ROOT = None  # resolved lazily on first use


def cprint(msg, color="", bold=False):
    colors = {"red": "91", "green": "92", "yellow": "93", "blue": "94",
              "cyan": "96", "white": "97", "magenta": "95"}
    prefix = "\033[1m" if bold else ""
    code = colors.get(color, "97")
    print(f"{prefix}\033[{code}m{msg}\033[0m")


def ensure_ltgui_lib():
    """Ensure ltgui static library exists; build it if not."""
    lib_path = os.path.join(LTGUI_ROOT, "build", "lib", "ltgui.lib")
    if os.path.exists(lib_path):
        return lib_path

    cprint("ltgui static library not found, building...", "yellow")
    result = subprocess.run(
        [sys.executable, os.path.join(LTGUI_ROOT, "ltgui.py"), "build"],
        cwd=LTGUI_ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        cprint("Failed to build ltgui:", "red", bold=True)
        print(result.stderr)
        sys.exit(1)
    return lib_path


def cmd_build():
    global LTGUI_ROOT
    LTGUI_ROOT = _find_ltgui_root(flags.get("ltgui_root"))
    ensure_ltgui_lib()

    os.makedirs(BUILD_DIR, exist_ok=True)

    # Find pybind11 cmake dir
    try:
        import pybind11
        cmake_dir = pybind11.get_cmake_dir()
    except ImportError:
        cprint("pybind11 not installed. Run: pip install pybind11", "red", bold=True)
        sys.exit(1)

    cmake_cmd = [
        "cmake", "-B", BUILD_DIR, "-S", SCRIPT_DIR,
        "-G", "Ninja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_CXX_COMPILER=clang++",
        f"-DLTGUI_ROOT={LTGUI_ROOT}",
        f"-Dpybind11_DIR={cmake_dir}",
    ]

    cprint(f"ltgui root: {LTGUI_ROOT}", "cyan")
    cprint("Configuring CMake...", "blue", bold=True)
    result = subprocess.run(cmake_cmd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if result.returncode != 0:
        cprint("CMake configure failed:", "red", bold=True)
        print(result.stderr)
        sys.exit(1)

    cprint("Building...", "blue", bold=True)
    result = subprocess.run(
        ["cmake", "--build", BUILD_DIR],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        cprint("Build failed:", "red", bold=True)
        print(result.stderr)
        sys.exit(1)

    # Copy font
    font_src = os.path.join(LTGUI_ROOT, "font", "Deng.ttf")
    font_dst = os.path.join(SCRIPT_DIR, "font", "Deng.ttf")
    if os.path.exists(font_src):
        os.makedirs(os.path.dirname(font_dst), exist_ok=True)
        shutil.copy2(font_src, font_dst)

    cprint("Build complete.", "green", bold=True)


def cmd_run(args):
    if len(args) < 2:
        cprint("Usage: python build.py run <example_name> [--ltgui-root <path>]", "yellow")
        examples_dir = os.path.join(SCRIPT_DIR, "examples")
        if os.path.isdir(examples_dir):
            for f in sorted(os.listdir(examples_dir)):
                if f.endswith(".py"):
                    print(f"  {f[:-3]}")
        return

    cmd_build()
    name = args[1]
    example_path = os.path.join(SCRIPT_DIR, "examples", f"{name}.py")
    if not os.path.exists(example_path):
        cprint(f"Example '{name}' not found at {example_path}", "red")
        return

    cprint(f"Running {name}.py...\n", "magenta", bold=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = SCRIPT_DIR
    subprocess.run([sys.executable, example_path], env=env)


def cmd_clean():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
        cprint("Cleaned build directory.", "green")
    pkg_dir = os.path.join(SCRIPT_DIR, "ltgui")
    if os.path.isdir(pkg_dir):
        for f in os.listdir(pkg_dir):
            if f.endswith(".pyd") or f.endswith(".dll"):
                os.remove(os.path.join(pkg_dir, f))
                cprint(f"Removed {f}", "yellow")
    if not any(f.endswith(".pyd") or f.endswith(".dll")
               for f in os.listdir(pkg_dir) if os.path.isdir(pkg_dir)):
        cprint("Nothing to clean.", "yellow")


def print_usage():
    cprint("ltgui-python build", "blue", bold=True)
    print("Usage: python build.py <command> [options]")
    print()
    print("Commands:")
    print("  build            Build the _ltgui.pyd binding module")
    print("  run <name>       Build and run an example from examples/")
    print("  test             Run unit tests (pytest required)")
    print("  clean            Remove build/ and .pyd files")
    print()
    print("Options:")
    print("  --ltgui-root <path>   Path to ltgui C++ library (default: auto-detect)")
    print()
    print("ltgui root is auto-detected from: ../ltgui, ../../ltgui, LTGUI_ROOT env var")
    print("or --ltgui-root flag. Falls back to D:/code/ltgui with a warning.")
    print()
    print("For pip install:   pip install .")
    print("For editable dev:  python setup.py develop")


def parse_args(argv):
    """Parse positional args and --key value flags."""
    positional = []
    flag_map = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i][2:]
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                flag_map[key] = argv[i + 1]
                i += 2
            else:
                flag_map[key] = True
                i += 1
        else:
            positional.append(argv[i])
            i += 1
    return positional, flag_map


# Module-level flags for cross-command access
flags = {}


def main():
    global flags
    args = sys.argv[1:]
    positional, flags = parse_args(args)

    if not positional or positional[0] in ("-h", "--help", "help"):
        print_usage()
    elif positional[0] == "build":
        cmd_build()
    elif positional[0] == "run":
        cmd_run(positional)
    elif positional[0] == "test":
        cmd_build()
        env = os.environ.copy()
        env["PYTHONPATH"] = SCRIPT_DIR
        import pytest
        test_dir = os.path.join(SCRIPT_DIR, "tests")
        sys.exit(pytest.main([test_dir, "-v"]))

    elif positional[0] == "clean":
        cmd_clean()
    else:
        cprint(f"Unknown command: {positional[0]}", "red")
        print_usage()


if __name__ == "__main__":
    main()
