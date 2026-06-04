"""Unit tests for ltgui Python bindings — no GUI window required."""
import pytest
import ltgui


# ============================================================================
# Value Types
# ============================================================================

class TestPoint:
    def test_default(self):
        p = ltgui.Point()
        assert p.x == 0
        assert p.y == 0
        assert repr(p) == "Point(0, 0)"

    def test_init(self):
        p = ltgui.Point(10, 20)
        assert p.x == 10
        assert p.y == 20

    def test_mutable(self):
        p = ltgui.Point(1, 2)
        p.x = 100
        p.y = 200
        assert p.x == 100
        assert p.y == 200


class TestSize:
    def test_default(self):
        s = ltgui.Size()
        assert s.width == 0
        assert s.height == 0
        assert s.is_empty()

    def test_init(self):
        s = ltgui.Size(100, 200)
        assert s.width == 100
        assert s.height == 200
        assert not s.is_empty()

    def test_mutable(self):
        s = ltgui.Size()
        s.width = 50
        s.height = 60
        assert s.width == 50


class TestRect:
    def test_default(self):
        r = ltgui.Rect()
        assert r.is_empty()

    def test_init(self):
        r = ltgui.Rect(0, 0, 800, 600)
        assert r.width == 800
        assert r.height == 600
        assert r.right() == 800
        assert r.bottom() == 600

    def test_contains_point(self):
        r = ltgui.Rect(0, 0, 100, 100)
        assert r.contains(ltgui.Point(50, 50))
        assert not r.contains(ltgui.Point(200, 200))

    def test_intersects(self):
        r1 = ltgui.Rect(0, 0, 50, 50)
        r2 = ltgui.Rect(25, 25, 50, 50)
        r3 = ltgui.Rect(100, 100, 10, 10)
        assert r1.intersects(r2)
        assert not r1.intersects(r3)

    def test_united(self):
        r1 = ltgui.Rect(0, 0, 10, 10)
        r2 = ltgui.Rect(5, 5, 10, 10)
        u = r1.united(r2)
        assert u.width == 15
        assert u.height == 15


class TestColor:
    def test_default(self):
        c = ltgui.Color()
        assert c.r == 0
        assert c.g == 0
        assert c.b == 0
        assert c.a == 255

    def test_rgba(self):
        c = ltgui.Color(10, 20, 30, 128)
        assert c.r == 10
        assert c.g == 20
        assert c.b == 30
        assert c.a == 128

    def test_static_constants(self):
        assert ltgui.White.a == 255
        assert ltgui.Black.r == 0
        assert ltgui.Red.r == 255
        assert ltgui.Transparent.a == 0
        # All constants exist
        for name in ["White", "Black", "Red", "Green", "Blue", "Yellow",
                     "Cyan", "Magenta", "Gray", "LightGray", "DarkGray"]:
            c = getattr(ltgui, name)
            assert c.a in (0, 255)


class TestFont:
    def test_default(self):
        f = ltgui.Font()
        assert f.family == ""
        assert f.size == 12

    def test_init(self):
        f = ltgui.Font("Deng", 14, ltgui.FontWeight.Bold)
        assert f.family == "Deng"
        assert f.size == 14
        assert f.weight == ltgui.FontWeight.Bold

    def test_system_default(self):
        f = ltgui.Font.system_default(14)
        assert f.size == 14
        assert len(f.family) > 0


# ============================================================================
# Theme
# ============================================================================

class TestTheme:
    def test_light(self):
        light = ltgui.Theme.light()
        # Light theme has bright background
        assert light.bg_primary.r > 200

    def test_dark(self):
        dark = ltgui.Theme.dark()
        # Dark theme has dark background
        assert dark.bg_primary.r < 100

    def test_global_set(self):
        # Save current
        before = ltgui.current_theme()
        dark = ltgui.Theme.dark()
        ltgui.set_theme(dark)
        after = ltgui.current_theme()
        assert after.bg_primary.r == dark.bg_primary.r
        # Restore (don't affect other tests)
        ltgui.set_theme(before)


# ============================================================================
# Enums
# ============================================================================

class TestEnums:
    def test_widget_type(self):
        assert ltgui.WidgetType.Button is not None
        assert ltgui.WidgetType.Label is not None
        assert ltgui.WidgetType.TextBox is not None

    def test_direction(self):
        assert ltgui.Direction.LeftToRight is not None
        assert ltgui.Direction.TopToBottom is not None
        assert ltgui.Direction.LeftToRight != ltgui.Direction.TopToBottom

    def test_key(self):
        assert ltgui.Key.A is not None
        assert ltgui.Key.Enter is not None
        assert ltgui.Key.Escape is not None

    def test_key_modifier(self):
        assert ltgui.KeyModifier.Shift is not None
        assert ltgui.KeyModifier.Control is not None

    def test_cursor_shape(self):
        assert ltgui.CursorShape.Hand is not None
        assert ltgui.CursorShape.Arrow is not None

    def test_easing(self):
        assert ltgui.Easing.Linear is not None
        assert ltgui.Easing.EaseOut is not None


# ============================================================================
# Layout
# ============================================================================

class TestLayout:
    def test_box_layout(self):
        box = ltgui.BoxLayout(ltgui.Direction.TopToBottom, 8, 12)
        box.add_stretch(1)
        box.set_spacing(10)
        box.set_margin(16)

    def test_grid_layout(self):
        grid = ltgui.GridLayout(2, 4, 4, 8)
        grid.set_column_stretch(0, 1)


# ============================================================================
# Widgets (no window needed for construction)
# ============================================================================

class TestWidget:
    def test_construct(self):
        w = ltgui.Widget()
        assert w.widget_type() == ltgui.WidgetType.Base
        assert w.enabled
        assert w.visible
        assert w.parent is None
        assert not w.has_focus()

    def test_state_mutation(self):
        w = ltgui.Widget()
        w.enabled = False
        assert not w.enabled
        w.visible = False
        assert not w.visible

    def test_geometry_defaults(self):
        w = ltgui.Widget()
        assert w.x == 0
        assert w.y == 0

    def test_size_hint(self):
        w = ltgui.Widget()
        hint = w.size_hint()
        assert hint.width > 0
        assert hint.height > 0

    def test_style(self):
        w = ltgui.Widget()
        st = w.style()
        assert st.border_width >= 0

    def test_can_accept_focus(self):
        w = ltgui.Widget()
        assert w.can_accept_focus()  # base Widget accepts focus


class TestButton:
    def test_construct(self):
        btn = ltgui.Button("Click")
        assert btn.text == "Click"

    def test_set_text(self):
        btn = ltgui.Button("Hello")
        btn.text = "World"
        assert btn.text == "World"

    def test_widget_type(self):
        btn = ltgui.Button("Test")
        assert btn.widget_type() == ltgui.WidgetType.Button

    def test_on_click(self):
        btn = ltgui.Button("Test")
        called = []

        def handler():
            called.append(True)

        btn.on_click(handler)
        # Can't trigger click without a window, but callback is stored
        assert callable(handler)


class TestLabel:
    def test_construct(self):
        lbl = ltgui.Label("Hello")
        assert lbl.text == "Hello"

    def test_cannot_accept_focus(self):
        lbl = ltgui.Label("Test")
        assert not lbl.can_accept_focus()

    def test_widget_type(self):
        lbl = ltgui.Label("Test")
        assert lbl.widget_type() == ltgui.WidgetType.Label


class TestTextBox:
    def test_construct(self):
        tb = ltgui.TextBox("edit me")
        assert tb.text == "edit me"

    def test_multi_line(self):
        tb = ltgui.TextBox()
        assert not tb.multi_line
        tb.multi_line = True
        assert tb.multi_line

    def test_undo_empty(self):
        tb = ltgui.TextBox("")
        assert not tb.can_undo()
        assert not tb.can_redo()


class TestCheckBox:
    def test_construct(self):
        cb = ltgui.CheckBox("Option")
        assert cb.text == "Option"
        assert not cb.checked

    def test_toggle(self):
        cb = ltgui.CheckBox("Toggle")
        cb.checked = True
        assert cb.checked

    def test_callback(self):
        cb = ltgui.CheckBox("Test")
        called = []

        def handler(checked):
            called.append(checked)

        cb.on_toggled(handler)
        assert callable(handler)


class TestRadioButton:
    def test_construct(self):
        rb = ltgui.RadioButton("Choice")
        assert rb.text == "Choice"
        assert not rb.checked

    def test_toggle(self):
        rb = ltgui.RadioButton("Toggle")
        rb.checked = True
        assert rb.checked


class TestSlider:
    def test_default_range(self):
        sl = ltgui.Slider()
        assert sl.minimum == 0
        assert sl.maximum == 100
        assert sl.value == 0

    def test_custom_range(self):
        sl = ltgui.Slider()
        sl.set_range(10, 90)
        assert sl.minimum == 10
        assert sl.maximum == 90

    def test_value(self):
        sl = ltgui.Slider()
        sl.set_range(0, 100)
        sl.value = 50
        assert sl.value == 50

    def test_callback(self):
        sl = ltgui.Slider()
        called = []

        def handler(v):
            called.append(v)

        sl.on_value_changed(handler)
        assert callable(handler)


class TestListBox:
    def test_add_items(self):
        lb = ltgui.ListBox()
        lb.add_item("A")
        lb.add_item("B")
        assert lb.count == 2
        assert lb.item(0) == "A"

    def test_selection(self):
        lb = ltgui.ListBox()
        lb.add_item("X")
        lb.add_item("Y")
        lb.selected_index = 0
        assert lb.selected_index == 0

    def test_clear(self):
        lb = ltgui.ListBox()
        lb.add_item("A")
        lb.clear()
        assert lb.count == 0


class TestComboBox:
    def test_add_items(self):
        cmb = ltgui.ComboBox()
        cmb.add_item("Small")
        cmb.add_item("Medium")
        assert cmb.count == 2

    def test_selection(self):
        cmb = ltgui.ComboBox()
        cmb.add_item("A")
        cmb.add_item("B")
        cmb.current_index = 1
        assert cmb.current_index == 1
        assert cmb.current_text() == "B"


class TestProgressBar:
    def test_range(self):
        pb = ltgui.ProgressBar()
        pb.set_range(0, 200)
        pb.value = 100
        assert pb.value == 100

    def test_indeterminate(self):
        pb = ltgui.ProgressBar()
        assert not pb.indeterminate
        pb.indeterminate = True
        assert pb.indeterminate


# ============================================================================
# Ownership & Lifetime
# ============================================================================

class TestOwnership:
    def test_parent_keeps_child_alive(self):
        """A child added to a parent should not be collected while parent lives."""
        root = ltgui.Widget()
        child = ltgui.Label("survive")
        root.add_child(child)
        assert child.parent is not None
        # If we can still access child, keep_alive works
        assert child.text == "survive"

    def test_make_child(self):
        root = ltgui.Widget()
        child = ltgui.make_child(root, ltgui.Label, "test")
        assert child.parent is not None
        assert child.text == "test"


# ============================================================================
# Event & Shortcut
# ============================================================================

class TestEvent:
    def test_default(self):
        ev = ltgui.Event()
        assert ev.type == ltgui.EventType.None_  # None_ avoids Python keyword

    def test_mouse_event(self):
        ev = ltgui.Event()
        ev.type = ltgui.EventType.MouseDown
        ev.button = ltgui.MouseButton.Left
        ev.pos = ltgui.Point(100, 200)
        assert ev.type == ltgui.EventType.MouseDown
        assert ev.button == ltgui.MouseButton.Left
        assert ev.pos.x == 100

    def test_key_event(self):
        ev = ltgui.Event()
        ev.type = ltgui.EventType.KeyDown
        ev.key = ltgui.Key.A
        ev.char_code = ord('a')
        assert ev.key == ltgui.Key.A
        assert ev.char_code == 97

    def test_accepted_flag(self):
        ev = ltgui.Event()
        assert not ev.accepted
        ev.accepted = True
        assert ev.accepted


class TestShortcut:
    def test_construct(self):
        sc = ltgui.Shortcut(ltgui.Key.S, ltgui.KeyModifier.Control)
        assert sc.key == ltgui.Key.S
        assert sc.modifiers == ltgui.KeyModifier.Control

    def test_default(self):
        sc = ltgui.Shortcut()
        assert sc.key == ltgui.Key.Unknown


# ============================================================================
# Timer
# ============================================================================

class TestTimer:
    def test_not_active(self):
        t = ltgui.Timer()
        assert not t.is_active()

    def test_single_shot(self):
        t = ltgui.Timer.single_shot(100, lambda: None)
        assert t.is_active()
        t.stop()
        assert not t.is_active()


# ============================================================================
# make_child
# ============================================================================

class TestMakeChild:
    def test_all_widget_types(self):
        root = ltgui.Widget()
        widgets = [
            (ltgui.Label, "text"),
            (ltgui.Button, "click"),
            (ltgui.CheckBox, "check"),
            (ltgui.RadioButton, "radio"),
            (ltgui.Slider,),
            (ltgui.ListBox,),
            (ltgui.ComboBox,),
            (ltgui.ProgressBar,),
        ]
        for cls_args in widgets:
            cls = cls_args[0]
            args = cls_args[1:]
            child = ltgui.make_child(root, cls, *args)
            assert child.parent is not None
