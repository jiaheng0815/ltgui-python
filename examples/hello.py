"""Minimal ltgui example — two buttons, a label, a counter."""
import ltgui


def main(window):
    window.set_title("Hello ltgui!")

    root = ltgui.Widget()
    root.style().bg_color = ltgui.White

    layout = ltgui.BoxLayout(ltgui.Direction.TopToBottom, 8, 12)

    label = ltgui.make_child(root, ltgui.Label, "Welcome to ltgui (Python)!")
    label.style().font = ltgui.Font("Deng", 18, ltgui.FontWeight.Bold)
    label.style().fg_color = ltgui.Color(0, 0, 128)

    click_count = 0

    def on_btn_click():
        nonlocal click_count
        click_count += 1
        btn.set_text(f"Clicked: {click_count} times")

    btn = ltgui.make_child(root, ltgui.Button, "Click Me!")
    btn.on_click(on_btn_click)

    quit_btn = ltgui.make_child(root, ltgui.Button, "Quit")
    quit_btn.on_click(lambda: window.close())

    layout.add_stretch(0)
    layout.add_stretch(0)
    layout.add_stretch(0)

    root.set_layout(layout)
    window.set_central_widget(root)


if __name__ == "__main__":
    ltgui.run(main)
