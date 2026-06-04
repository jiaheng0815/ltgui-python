# ltgui-python

Python bindings for [ltgui](https://github.com/jiaheng0815/ltgui) — a from-scratch, cross-platform retained-mode C++17 GUI framework.
基于 [ltgui](https://github.com/jiaheng0815/ltgui) 的 Python 绑定——从零构建的跨平台保留模式 C++17 GUI 框架。

[English](#english) | [中文](#中文)

---

# English

## Install

```bash
# Prerequisites
pip install pybind11

# Build (requires ltgui at D:/code/ltgui)
git clone https://github.com/jiaheng0815/ltgui-python.git
cd ltgui-python
python build.py build
```

## Quick Start

```python
import ltgui

def main(window):
    window.set_title("Hello ltgui")
    root = ltgui.Widget()
    root.style().bg_color = ltgui.White

    label = ltgui.make_child(root, ltgui.Label, "Welcome to ltgui!")
    btn = ltgui.make_child(root, ltgui.Button, "Click Me!")
    btn.on_click(lambda: btn.set_text("Clicked!"))

    layout = ltgui.BoxLayout(ltgui.Direction.TopToBottom, 8, 12)
    root.set_layout(layout)
    window.set_central_widget(root)

ltgui.run(main)
```

## API Coverage

| Category | Classes |
|----------|---------|
| Value Types | Point, Size, Rect, Color, Font, FontWeight, FontStyle, Style, Event |
| Theme | Theme (Light/Dark), current_theme()/set_theme() |
| Enums | WidgetType, EventType, MouseButton, Key, KeyModifier, CursorShape, Easing, Direction |
| Layout | BoxLayout (LeftToRight/TopToBottom), GridLayout |
| Timer | Timer (start/stop/single_shot) |
| Core | Application (singleton), Window, Shortcut |

**14 Widgets:** Widget, Button, Label, TextBox, CheckBox, RadioButton, Slider, ListBox, ComboBox, ProgressBar, TabWidget, Image, ScrollArea

## Commands

```bash
python build.py build          # Build _ltgui.pyd
python build.py run hello      # Build + run examples/hello.py
python build.py run demo       # Build + run examples/demo.py
python build.py clean          # Remove build/ and .pyd
```

## Requirements

- Python 3.8+
- pybind11 3.0+
- [ltgui](https://github.com/jiaheng0815/ltgui) built at `D:/code/ltgui`
- Windows: clang++ (LLVM) + Ninja

---

# 中文

## 安装

```bash
# 前置
pip install pybind11

# 编译（需要 ltgui 位于 D:/code/ltgui）
git clone https://github.com/jiaheng0815/ltgui-python.git
cd ltgui-python
python build.py build
```

## 快速开始

```python
import ltgui

def main(window):
    window.set_title("Hello ltgui")
    root = ltgui.Widget()
    root.style().bg_color = ltgui.White

    label = ltgui.make_child(root, ltgui.Label, "Welcome to ltgui!")
    btn = ltgui.make_child(root, ltgui.Button, "Click Me!")
    btn.on_click(lambda: btn.set_text("Clicked!"))

    layout = ltgui.BoxLayout(ltgui.Direction.TopToBottom, 8, 12)
    root.set_layout(layout)
    window.set_central_widget(root)

ltgui.run(main)
```

## API 覆盖

| 类别 | 类 |
|------|-----|
| 值类型 | Point, Size, Rect, Color, Font, FontWeight, FontStyle, Style, Event |
| 主题 | Theme (Light/Dark), current_theme()/set_theme() |
| 枚举 | WidgetType, EventType, MouseButton, Key, KeyModifier, CursorShape, Easing, Direction |
| 布局 | BoxLayout (LeftToRight/TopToBottom), GridLayout |
| 计时器 | Timer (start/stop/single_shot) |
| 核心 | Application (单例), Window, Shortcut |

**14 个控件:** Widget, Button, Label, TextBox, CheckBox, RadioButton, Slider, ListBox, ComboBox, ProgressBar, TabWidget, Image, ScrollArea

## 命令

```bash
python build.py build          # 编译 _ltgui.pyd
python build.py run hello      # 编译 + 运行 examples/hello.py
python build.py run demo       # 编译 + 运行 examples/demo.py
python build.py clean          # 清理 build/ 和 .pyd
```

## 依赖

- Python 3.8+
- pybind11 3.0+
- [ltgui](https://github.com/jiaheng0815/ltgui) 已编译于 `D:/code/ltgui`
- Windows: clang++ (LLVM) + Ninja
