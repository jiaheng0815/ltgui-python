"""Full ltgui widget showcase — 14+ widgets, callbacks, theme toggle."""
import ltgui


def main(window):
    window.set_title("ltgui Python Demo")
    window.create(680, 520, "ltgui Python Demo")

    root = ltgui.Widget()
    root.style().bg_color = ltgui.White

    main_layout = ltgui.BoxLayout(ltgui.Direction.TopToBottom, 6, 10)

    # ---- Title ----
    title = ltgui.make_child(root, ltgui.Label, "ltgui Widget Demo (Python)")
    title.style().font = ltgui.Font("Deng", 20, ltgui.FontWeight.Bold)
    title.style().fg_color = ltgui.Color(0, 0, 128)

    # ---- Button Row ----
    btn_row = ltgui.make_child(root, ltgui.Widget)
    btn_row.style().bg_color = ltgui.Transparent
    btn_layout = ltgui.BoxLayout(ltgui.Direction.LeftToRight, 8, 4)

    btn1 = ltgui.make_child(btn_row, ltgui.Button, "Normal")
    btn2 = ltgui.make_child(btn_row, ltgui.Button, "Disabled")
    btn2.enabled = False

    clicks = 0
    btn3 = ltgui.make_child(btn_row, ltgui.Button, "Counter: 0")
    btn3.on_click(lambda: _inc_counter(btn3))

    btn_row.set_layout(btn_layout)

    # ---- TextBox Row ----
    text_row = ltgui.make_child(root, ltgui.Widget)
    text_row.style().bg_color = ltgui.Transparent
    text_layout = ltgui.BoxLayout(ltgui.Direction.LeftToRight, 8, 4)

    ltgui.make_child(text_row, ltgui.Label, "Text:")
    textbox = ltgui.make_child(text_row, ltgui.TextBox, "Edit me!")
    text_layout.add_stretch(0)
    text_layout.add_stretch(1)
    text_row.set_layout(text_layout)

    # ---- CheckBox + RadioButton Row ----
    check_row = ltgui.make_child(root, ltgui.Widget)
    check_row.style().bg_color = ltgui.Transparent
    check_layout = ltgui.BoxLayout(ltgui.Direction.LeftToRight, 12, 4)

    cb1 = ltgui.make_child(check_row, ltgui.CheckBox, "Option A")
    cb2 = ltgui.make_child(check_row, ltgui.CheckBox, "Option B")
    cb2.checked = True
    cb3 = ltgui.make_child(check_row, ltgui.CheckBox, "Option C")

    rb_group = ltgui.make_child(check_row, ltgui.Widget)
    rb_group.style().bg_color = ltgui.Transparent
    rb_layout = ltgui.BoxLayout(ltgui.Direction.LeftToRight, 4, 0)
    rb1 = ltgui.make_child(rb_group, ltgui.RadioButton, "Red")
    rb2 = ltgui.make_child(rb_group, ltgui.RadioButton, "Green")
    rb3 = ltgui.make_child(rb_group, ltgui.RadioButton, "Blue")
    rb1.checked = True
    rb_group.set_layout(rb_layout)

    check_row.set_layout(check_layout)

    # ---- Slider Row ----
    slider_row = ltgui.make_child(root, ltgui.Widget)
    slider_row.style().bg_color = ltgui.Transparent
    sl_layout = ltgui.BoxLayout(ltgui.Direction.LeftToRight, 8, 4)

    ltgui.make_child(slider_row, ltgui.Label, "Volume:")
    slider = ltgui.make_child(slider_row, ltgui.Slider)
    slider.set_range(0, 100)
    slider.value = 50
    sl_value = ltgui.make_child(slider_row, ltgui.Label, "50")
    slider.on_value_changed(lambda v: sl_value.set_text(str(v)))

    sl_layout.add_stretch(0)
    sl_layout.add_stretch(1)
    sl_layout.add_stretch(0)
    slider_row.set_layout(sl_layout)

    # ---- Progress Bar Row ----
    pb_row = ltgui.make_child(root, ltgui.Widget)
    pb_row.style().bg_color = ltgui.Transparent
    pb_layout = ltgui.BoxLayout(ltgui.Direction.LeftToRight, 8, 4)

    ltgui.make_child(pb_row, ltgui.Label, "Progress:")
    pb = ltgui.make_child(pb_row, ltgui.ProgressBar)
    pb.set_range(0, 100)
    pb.value = 65

    pb_layout.add_stretch(0)
    pb_layout.add_stretch(1)
    pb_row.set_layout(pb_layout)

    # ---- List + Combo Row ----
    list_row = ltgui.make_child(root, ltgui.Widget)
    list_row.style().bg_color = ltgui.Transparent
    list_layout2 = ltgui.BoxLayout(ltgui.Direction.LeftToRight, 8, 4)

    listbox = ltgui.make_child(list_row, ltgui.ListBox)
    for fruit in ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]:
        listbox.add_item(fruit)
    listbox.selected_index = 0

    combo = ltgui.make_child(list_row, ltgui.ComboBox)
    combo.add_item("Small")
    combo.add_item("Medium")
    combo.add_item("Large")
    combo.add_item("Extra Large")
    combo.current_index = 1

    list_layout2.add_stretch(1)
    list_layout2.add_stretch(0)
    list_row.set_layout(list_layout2)

    # ---- Theme toggle button ----
    theme_btn = ltgui.make_child(root, ltgui.Button, "Toggle Dark/Light Theme")

    dark_mode = False

    def toggle_theme():
        nonlocal dark_mode
        dark_mode = not dark_mode
        ltgui.set_theme(ltgui.Theme.dark() if dark_mode else ltgui.Theme.light())
        theme_btn.set_text("Light Theme" if dark_mode else "Dark Theme")

    theme_btn.on_click(toggle_theme)

    # ---- Quit button ----
    quit_btn = ltgui.make_child(root, ltgui.Button, "Quit")
    quit_btn.on_click(lambda: window.close())

    # ---- Stretch factors ----
    for _ in range(8):
        main_layout.add_stretch(0)

    root.set_layout(main_layout)
    window.set_central_widget(root)


def _inc_counter(btn):
    """Closure helper for the counter button."""
    current = btn.text()
    count = 0
    try:
        count = int(current.split(":")[-1].strip()) + 1
    except ValueError:
        pass
    btn.set_text(f"Counter: {count}")


if __name__ == "__main__":
    ltgui.run(main)
