"""
ltgui — cross-platform retained-mode GUI framework for Python.

Quick start:
    import ltgui
    ltgui.run(main)

Where main(window) builds the widget tree and returns.
"""

import os as _os
import sys as _sys

# Ensure _ltgui.pyd can be imported
_pkg_dir = _os.path.dirname(_os.path.abspath(__file__))
if _pkg_dir not in _sys.path:
    _sys.path.insert(0, _pkg_dir)

# Set font path before any window creates its GPU canvas
_font_path = _os.path.join(_pkg_dir, "..", "font", "Deng.ttf")
if not _os.path.exists(_font_path):
    _font_path = _os.path.join(_pkg_dir, "font", "Deng.ttf")

from _ltgui import *  # noqa: E402, F403

# ---- High-level convenience functions ----

def run(callback):
    """Create a Window, call callback(window), show, and enter the event loop.

    Example:
        def main(window):
            root = ltgui.Widget()
            ltgui.make_child(root, ltgui.Label, "Hello!")
            window.set_central_widget(root)

        ltgui.run(main)
    """
    app = Application.instance()
    window = Window()
    if not window.create(800, 600, "ltgui"):
        raise RuntimeError("Failed to create window")
    try:
        callback(window)
    except Exception:
        import traceback
        traceback.print_exc()
        return
    window.show()
    app.run()


def make_child(parent, widget_cls, *args, **kwargs):
    """Create a widget of type `widget_cls`, add it to `parent`, return it.

    Args:
        parent: The parent Widget.
        widget_cls: The widget class (e.g., ltgui.Button, ltgui.Label).
        *args, **kwargs: Passed to the widget constructor (except 'parent').

    Returns:
        The newly created widget (now a child of `parent`).

    Example:
        btn = ltgui.make_child(root, ltgui.Button, "Click Me!")
    """
    widget = widget_cls(*args, **kwargs)
    parent.add_child(widget)
    return widget
