#!/usr/bin/env python3
"""ltgui-python build script — python build.py [build|run <name>|clean]"""

import os
import sys
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LTGUI_ROOT = os.path.join(os.path.dirname(SCRIPT_DIR), "ltgui")
BUILD_DIR = os.path.join(SCRIPT_DIR, "build")

def cprint(msg, color="", bold=False):
    colors = {"red": "91", "green": "92", "yellow": "93", "blue": "94",
              "cyan": "96", "white": "97", "magenta": "95"}
    prefix = "\033[1m" if bold else ""
    code = colors.get(color, "97")
    print(f"{prefix}\033[{code}m{msg}\033[0m")

def ensure_ltgui_lib():
    """Ensure D:/code/ltgui/build/lib/ltgui.lib exists."""
    lib_path = os.path.join(LTGUI_ROOT, "build", "lib", "ltgui.lib")
    if not os.path.exists(lib_path):
        cprint("ltgui static library not found, building...", "yellow")
        result = subprocess.run(
            [sys.executable, os.path.join(LTGUI_ROOT, "ltgui.py"), "build"],
            cwd=LTGUI_ROOT, capture_output=True, text=True
        )
        if result.returncode != 0:
            cprint("Failed to build ltgui:", "red", bold=True)
            print(result.stderr)
            sys.exit(1)
    return lib_path

def cmd_build():
    ensure_ltgui_lib()

    os.makedirs(BUILD_DIR, exist_ok=True)

    cmake_cmd = [
        "cmake", "-B", BUILD_DIR, "-S", SCRIPT_DIR,
        "-G", "Ninja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_CXX_COMPILER=clang++",
    ]

    # Find pybind11 cmake dir
    try:
        import pybind11
        cmake_dir = pybind11.get_cmake_dir()
        cmake_cmd.append(f"-Dpybind11_DIR={cmake_dir}")
    except ImportError:
        cprint("pybind11 not installed. Run: pip install pybind11", "red", bold=True)
        sys.exit(1)

    cprint("Configuring CMake...", "blue", bold=True)
    result = subprocess.run(cmake_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
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
        cprint("Usage: python build.py run <example_name>", "yellow")
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
    pyd_files = [f for f in os.listdir(os.path.join(SCRIPT_DIR, "ltgui"))
                 if f.endswith(".pyd") or f.endswith(".dll")]
    for f in pyd_files:
        os.remove(os.path.join(SCRIPT_DIR, "ltgui", f))
        cprint(f"Removed {f}", "yellow")
    if not pyd_files:
        cprint("Nothing to clean.", "yellow")

def print_usage():
    cprint("ltgui-python build", "blue", bold=True)
    print("Usage: python build.py <command> [options]")
    print()
    print("Commands:")
    print("  build            Build the _ltgui.pyd binding module")
    print("  run <name>       Build and run an example from examples/")
    print("  clean            Remove build/ and .pyd files")

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print_usage()
    elif args[0] == "build":
        cmd_build()
    elif args[0] == "run":
        cmd_run(args)
    elif args[0] == "clean":
        cmd_clean()
    else:
        cprint(f"Unknown command: {args[0]}", "red")
        print_usage()

if __name__ == "__main__":
    main()
