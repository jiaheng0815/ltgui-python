// ltgui pybind11 bindings — single translation unit
#include "ltgui/ltgui.h"
#include "ltgui/log.h"
#include "ltgui/timer.h"
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace ltgui;

// ============================================================================
// Widget Trampoline — enables Python subclassing of Widget
// ============================================================================

class PyWidget : public Widget {
public:
    using Widget::Widget;

    Size sizeHint() const override {
        PYBIND11_OVERRIDE(Size, Widget, sizeHint);
    }
    bool handleEvent(Event& event) override {
        PYBIND11_OVERRIDE(bool, Widget, handleEvent, event);
    }
    void paintSelf(NativeCanvas* canvas) override {
        PYBIND11_OVERRIDE(void, Widget, paintSelf, canvas);
    }
    WidgetType widgetType() const override {
        PYBIND11_OVERRIDE(WidgetType, Widget, widgetType);
    }
    bool canAcceptFocus() const override {
        PYBIND11_OVERRIDE(bool, Widget, canAcceptFocus);
    }
    void setGeometry(const Rect& rect) override {
        PYBIND11_OVERRIDE(void, Widget, setGeometry, rect);
    }
    Widget* hitTest(const Point& pos) override {
        PYBIND11_OVERRIDE(Widget*, Widget, hitTest, pos);
    }
    Widget* nextFocusWidget() override {
        PYBIND11_OVERRIDE(Widget*, Widget, nextFocusWidget);
    }
    Widget* previousFocusWidget() override {
        PYBIND11_OVERRIDE(Widget*, Widget, previousFocusWidget);
    }
};

// ============================================================================
// Module Definition
// ============================================================================

PYBIND11_MODULE(_ltgui, m) {
    m.doc() = "ltgui — cross-platform retained-mode GUI framework for Python";

    // ========================================================================
    // Geometry types
    // ========================================================================

    py::class_<Point>(m, "Point")
        .def(py::init<>())
        .def(py::init<int, int>(), py::arg("x")=0, py::arg("y")=0)
        .def_readwrite("x", &Point::x)
        .def_readwrite("y", &Point::y)
        .def("__repr__", [](const Point& p) {
            return "Point(" + std::to_string(p.x) + ", " + std::to_string(p.y) + ")";
        });

    py::class_<Size>(m, "Size")
        .def(py::init<>())
        .def(py::init<int, int>(), py::arg("width")=0, py::arg("height")=0)
        .def_readwrite("width", &Size::width)
        .def_readwrite("height", &Size::height)
        .def("is_empty", &Size::isEmpty)
        .def("__repr__", [](const Size& s) {
            return "Size(" + std::to_string(s.width) + ", " + std::to_string(s.height) + ")";
        });

    py::class_<Rect>(m, "Rect")
        .def(py::init<>())
        .def(py::init<int, int, int, int>(), py::arg("x")=0, py::arg("y")=0,
             py::arg("width")=0, py::arg("height")=0)
        .def_readwrite("x", &Rect::x)
        .def_readwrite("y", &Rect::y)
        .def_readwrite("width", &Rect::width)
        .def_readwrite("height", &Rect::height)
        .def("left", &Rect::left)
        .def("top", &Rect::top)
        .def("right", &Rect::right)
        .def("bottom", &Rect::bottom)
        .def("contains", py::overload_cast<const Point&>(&Rect::contains, py::const_))
        .def("intersects", &Rect::intersects)
        .def("united", &Rect::united)
        .def("is_empty", &Rect::isEmpty)
        .def("__repr__", [](const Rect& r) {
            return "Rect(" + std::to_string(r.x) + ", " + std::to_string(r.y) +
                   ", " + std::to_string(r.width) + ", " + std::to_string(r.height) + ")";
        });

    // ========================================================================
    // Color
    // ========================================================================

    py::class_<Color>(m, "Color")
        .def(py::init<>())
        .def(py::init<uint8_t, uint8_t, uint8_t, uint8_t>(),
             py::arg("r")=0, py::arg("g")=0, py::arg("b")=0, py::arg("a")=255)
        .def_readwrite("r", &Color::r)
        .def_readwrite("g", &Color::g)
        .def_readwrite("b", &Color::b)
        .def_readwrite("a", &Color::a)
        .def_static("from_rgb", &Color::fromRGB)
        .def("__repr__", [](const Color& c) {
            return "Color(" + std::to_string(c.r) + "," + std::to_string(c.g) +
                   "," + std::to_string(c.b) + "," + std::to_string(c.a) + ")";
        });

    // Color constants
    m.attr("Transparent") = Color::Transparent;
    m.attr("Black")       = Color::Black;
    m.attr("White")       = Color::White;
    m.attr("Red")         = Color::Red;
    m.attr("Green")       = Color::Green;
    m.attr("Blue")        = Color::Blue;
    m.attr("Yellow")      = Color::Yellow;
    m.attr("Cyan")        = Color::Cyan;
    m.attr("Magenta")     = Color::Magenta;
    m.attr("Gray")        = Color::Gray;
    m.attr("LightGray")   = Color::LightGray;
    m.attr("DarkGray")    = Color::DarkGray;

    // ========================================================================
    // Font
    // ========================================================================

    py::enum_<FontWeight>(m, "FontWeight")
        .value("Thin", FontWeight::Thin)
        .value("ExtraLight", FontWeight::ExtraLight)
        .value("Light", FontWeight::Light)
        .value("Normal", FontWeight::Normal)
        .value("Medium", FontWeight::Medium)
        .value("SemiBold", FontWeight::SemiBold)
        .value("Bold", FontWeight::Bold)
        .value("ExtraBold", FontWeight::ExtraBold)
        .value("Black", FontWeight::Black);

    py::enum_<FontStyle>(m, "FontStyle")
        .value("Normal", FontStyle::Normal)
        .value("Italic", FontStyle::Italic);

    py::class_<Font>(m, "Font")
        .def(py::init<>())
        .def(py::init<const std::string&, int, FontWeight, FontStyle>(),
             py::arg("family")="", py::arg("size")=12,
             py::arg("weight")=FontWeight::Normal,
             py::arg("style")=FontStyle::Normal)
        .def_readwrite("family", &Font::family)
        .def_readwrite("size", &Font::size)
        .def_readwrite("weight", &Font::weight)
        .def_readwrite("style", &Font::style)
        .def_static("system_default", &Font::systemDefault, py::arg("size")=12)
        .def("__repr__", [](const Font& f) {
            return "Font('" + f.family + "', " + std::to_string(f.size) + ")";
        });

    // ========================================================================
    // Style
    // ========================================================================

    py::class_<Style>(m, "Style")
        .def(py::init<>())
        .def_readwrite("bg_color", &Style::bgColor)
        .def_readwrite("fg_color", &Style::fgColor)
        .def_readwrite("border_color", &Style::borderColor)
        .def_readwrite("border_width", &Style::borderWidth)
        .def_readwrite("border_radius", &Style::borderRadius)
        .def_readwrite("font", &Style::font)
        .def_readwrite("padding_left", &Style::paddingLeft)
        .def_readwrite("padding_top", &Style::paddingTop)
        .def_readwrite("padding_right", &Style::paddingRight)
        .def_readwrite("padding_bottom", &Style::paddingBottom)
        .def("set_padding", py::overload_cast<int>(&Style::setPadding), py::arg("all"))
        .def("set_padding_hv", py::overload_cast<int, int>(&Style::setPadding),
             py::arg("h"), py::arg("v"))
        .def("set_margin", py::overload_cast<int>(&Style::setMargin), py::arg("all"))
        .def("set_margin_hv", py::overload_cast<int, int>(&Style::setMargin),
             py::arg("h"), py::arg("v"))
        .def_static("default", &Style::defaultStyle);

    // ========================================================================
    // Theme
    // ========================================================================

    py::class_<Theme>(m, "Theme")
        .def(py::init<>())
        .def_readwrite("bg_primary", &Theme::bgPrimary)
        .def_readwrite("bg_secondary", &Theme::bgSecondary)
        .def_readwrite("bg_tertiary", &Theme::bgTertiary)
        .def_readwrite("text_primary", &Theme::textPrimary)
        .def_readwrite("text_secondary", &Theme::textSecondary)
        .def_readwrite("text_disabled", &Theme::textDisabled)
        .def_readwrite("accent", &Theme::accent)
        .def_readwrite("accent_hover", &Theme::accentHover)
        .def_readwrite("accent_pressed", &Theme::accentPressed)
        .def_readwrite("border", &Theme::border)
        .def_readwrite("border_focus", &Theme::borderFocus)
        .def_readwrite("scrollbar_track", &Theme::scrollbarTrack)
        .def_readwrite("scrollbar_thumb", &Theme::scrollbarThumb)
        .def_readwrite("selection_bg", &Theme::selectionBg)
        .def_static("light", &Theme::Light)
        .def_static("dark", &Theme::Dark);

    m.def("current_theme", &currentTheme);
    m.def("set_theme", &setTheme);

    // ========================================================================
    // Enums
    // ========================================================================

    py::enum_<WidgetType>(m, "WidgetType")
        .value("Base", WidgetType::Base)
        .value("Button", WidgetType::Button)
        .value("Label", WidgetType::Label)
        .value("TextBox", WidgetType::TextBox)
        .value("CheckBox", WidgetType::CheckBox)
        .value("RadioButton", WidgetType::RadioButton)
        .value("Slider", WidgetType::Slider)
        .value("ListBox", WidgetType::ListBox)
        .value("ScrollArea", WidgetType::ScrollArea)
        .value("ComboBox", WidgetType::ComboBox)
        .value("ProgressBar", WidgetType::ProgressBar)
        .value("Tooltip", WidgetType::Tooltip)
        .value("TabWidget", WidgetType::TabWidget)
        .value("Image", WidgetType::Image)
        .value("TreeView", WidgetType::TreeView)
        .value("ContextMenu", WidgetType::ContextMenu);

    py::enum_<EventType>(m, "EventType")
        .value("None_", EventType::None)
        .value("MouseDown", EventType::MouseDown)
        .value("MouseUp", EventType::MouseUp)
        .value("MouseMove", EventType::MouseMove)
        .value("MouseWheel", EventType::MouseWheel)
        .value("KeyDown", EventType::KeyDown)
        .value("KeyUp", EventType::KeyUp)
        .value("Paint", EventType::Paint)
        .value("Resize", EventType::Resize)
        .value("Close", EventType::Close)
        .value("FocusIn", EventType::FocusIn)
        .value("FocusOut", EventType::FocusOut)
        .value("ImeComposition", EventType::ImeComposition);

    py::enum_<MouseButton>(m, "MouseButton")
        .value("NoButton", MouseButton::None)
        .value("Left", MouseButton::Left)
        .value("Right", MouseButton::Right)
        .value("Middle", MouseButton::Middle);

    py::enum_<KeyModifier>(m, "KeyModifier")
        .value("NoModifier", KeyModifier::None)
        .value("Shift", KeyModifier::Shift)
        .value("Control", KeyModifier::Control)
        .value("Alt", KeyModifier::Alt);

    py::enum_<Key>(m, "Key")
        .value("Unknown", Key::Unknown)
        .value("A", Key::A).value("B", Key::B).value("C", Key::C).value("D", Key::D)
        .value("E", Key::E).value("F", Key::F).value("G", Key::G).value("H", Key::H)
        .value("I", Key::I).value("J", Key::J).value("K", Key::K).value("L", Key::L)
        .value("M", Key::M).value("N", Key::N).value("O", Key::O).value("P", Key::P)
        .value("Q", Key::Q).value("R", Key::R).value("S", Key::S).value("T", Key::T)
        .value("U", Key::U).value("V", Key::V).value("W", Key::W).value("X", Key::X)
        .value("Y", Key::Y).value("Z", Key::Z)
        .value("Num0", Key::Num0).value("Num1", Key::Num1).value("Num2", Key::Num2)
        .value("Num3", Key::Num3).value("Num4", Key::Num4).value("Num5", Key::Num5)
        .value("Num6", Key::Num6).value("Num7", Key::Num7).value("Num8", Key::Num8)
        .value("Num9", Key::Num9)
        .value("F1", Key::F1).value("F2", Key::F2).value("F3", Key::F3)
        .value("F4", Key::F4).value("F5", Key::F5).value("F6", Key::F6)
        .value("F7", Key::F7).value("F8", Key::F8).value("F9", Key::F9)
        .value("F10", Key::F10).value("F11", Key::F11).value("F12", Key::F12)
        .value("Escape", Key::Escape).value("Enter", Key::Enter)
        .value("Space", Key::Space).value("Backspace", Key::Backspace)
        .value("Tab", Key::Tab).value("Shift", Key::Shift)
        .value("Control", Key::Control).value("Alt", Key::Alt)
        .value("Left", Key::Left).value("Right", Key::Right)
        .value("Up", Key::Up).value("Down", Key::Down)
        .value("Home", Key::Home).value("End", Key::End)
        .value("PageUp", Key::PageUp).value("PageDown", Key::PageDown)
        .value("Insert", Key::Insert).value("Delete", Key::Delete);

    py::enum_<Easing>(m, "Easing")
        .value("Linear", Easing::Linear)
        .value("EaseIn", Easing::EaseIn)
        .value("EaseOut", Easing::EaseOut)
        .value("EaseInOut", Easing::EaseInOut);

    py::enum_<CursorShape>(m, "CursorShape")
        .value("Arrow", CursorShape::Arrow)
        .value("IBeam", CursorShape::IBeam)
        .value("Wait", CursorShape::Wait)
        .value("Crosshair", CursorShape::Crosshair)
        .value("SizeWE", CursorShape::SizeWE)
        .value("SizeNS", CursorShape::SizeNS)
        .value("SizeAll", CursorShape::SizeAll)
        .value("Hand", CursorShape::Hand)
        .value("Denied", CursorShape::Denied);

    // ========================================================================
    // Event struct
    // ========================================================================

    py::class_<Event>(m, "Event")
        .def(py::init<>())
        .def_readwrite("type", &Event::type)
        .def_readwrite("pos", &Event::pos)
        .def_readwrite("button", &Event::button)
        .def_readwrite("key", &Event::key)
        .def_readwrite("modifiers", &Event::modifiers)
        .def_readwrite("wheel_delta", &Event::wheelDelta)
        .def_readwrite("char_code", &Event::charCode)
        .def_readwrite("width", &Event::width)
        .def_readwrite("height", &Event::height)
        .def_readwrite("accepted", &Event::accepted)
        .def("__repr__", [](const Event& e) {
            return "Event(type=" + std::to_string(static_cast<int>(e.type)) + ")";
        });

    // ========================================================================
    // Shortcut
    // ========================================================================

    py::class_<Shortcut>(m, "Shortcut")
        .def(py::init<>())
        .def(py::init<Key, KeyModifier>(), py::arg("key"), py::arg("modifiers")=KeyModifier::None)
        .def_readwrite("key", &Shortcut::key)
        .def_readwrite("modifiers", &Shortcut::modifiers)
        .def("__repr__", [](const Shortcut& sc) {
            return "Shortcut(key=" + std::to_string(static_cast<int>(sc.key)) + ")";
        });

    // ========================================================================
    // Layout
    // ========================================================================

    py::class_<Layout>(m, "Layout");

    py::class_<BoxLayout, Layout>(m, "BoxLayout")
        .def(py::init<BoxLayout::Direction, int, int>(),
             py::arg("direction"), py::arg("spacing")=4, py::arg("margin")=8)
        .def("add_stretch", &BoxLayout::addStretch, py::arg("factor")=1)
        .def("set_spacing", &BoxLayout::setSpacing)
        .def("set_margin", &BoxLayout::setMargin)
        .def("set_direction", &BoxLayout::setDirection);

    py::enum_<BoxLayout::Direction>(m, "Direction")
        .value("LeftToRight", BoxLayout::LeftToRight)
        .value("TopToBottom", BoxLayout::TopToBottom);

    py::class_<GridLayout, Layout>(m, "GridLayout")
        .def(py::init<int, int, int, int>(),
             py::arg("cols"), py::arg("row_spacing")=4,
             py::arg("col_spacing")=4, py::arg("margin")=8)
        .def("set_column_stretch", &GridLayout::setColumnStretch)
        .def("set_row_stretch", &GridLayout::setRowStretch);

    // ========================================================================
    // Timer
    // ========================================================================

    py::class_<Timer>(m, "Timer")
        .def(py::init<>())
        .def("start", [](Timer& t, int ms, bool repeat, py::function cb) {
            t.start(ms, repeat, cb);
        }, py::arg("ms"), py::arg("repeating")=false, py::arg("callback"))
        .def("stop", &Timer::stop)
        .def("is_active", &Timer::isActive)
        .def_static("single_shot", [](int ms, py::function cb) -> Timer* {
            auto* t = new Timer();
            t->start(ms, false, cb);
            return t;
        }, py::arg("ms"), py::arg("callback"), py::return_value_policy::take_ownership);

    // ========================================================================
    // Application (singleton)
    // ========================================================================

    py::class_<Application, std::unique_ptr<Application, py::nodelete>>(m, "Application")
        .def_static("instance", &Application::instance,
                    py::return_value_policy::reference)
        .def("run", &Application::run)
        .def("quit", &Application::quit)
        .def_property("dpi_scale", &Application::dpiScale, &Application::setDpiScale);

    // ========================================================================
    // Window
    // ========================================================================

    py::class_<Window>(m, "Window")
        .def(py::init<>())
        .def("create", &Window::create, py::arg("width")=800, py::arg("height")=600,
             py::arg("title")="ltgui")
        .def("close", &Window::close)
        .def("show", &Window::show)
        .def("hide", &Window::hide)
        .def("set_title", &Window::setTitle)
        .def("set_size", &Window::setSize)
        .def("get_size", &Window::getSize)
        .def("is_gpu_accelerated", &Window::isGpuAccelerated)
        .def_property_readonly("dpi_scale", &Window::dpiScale)
        .def("set_cursor", &Window::setCursor)
        .def("register_shortcut", &Window::registerShortcut)
        .def("set_central_widget", [](Window& w, Widget* widget) {
            w.setCentralWidget(std::unique_ptr<Widget>(widget));
        }, py::arg("widget"), py::keep_alive<1, 0>())  // window keeps widget alive
        .def("central_widget", &Window::centralWidget,
             py::return_value_policy::reference)
        .def("update", &Window::update);

    // ========================================================================
    // Widget base class (py::nodelete — C++ parent tree owns all widgets)
    // ========================================================================

    py::class_<Widget, PyWidget, std::unique_ptr<Widget, py::nodelete>> widget_cls(m, "Widget");
    widget_cls
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        // Tree
        .def_property_readonly("parent", &Widget::parent, py::return_value_policy::reference)
        .def("add_child", [](Widget& self, Widget* child) {
            self.addChild(std::unique_ptr<Widget>(child));
        }, py::arg("child"), py::keep_alive<1, 0>())  // parent keeps child alive
        .def("remove_child", [](Widget& self, Widget* child) {
            auto ptr = self.removeChild(child);
            if (ptr) ptr.release(); // give ownership back to Python
        }, py::arg("child"))
        .def("child_at", &Widget::childAt, py::return_value_policy::reference)
        .def_property_readonly("children", [](Widget& self) -> py::list {
            py::list result;
            for (auto& c : self.children())
                result.append(py::cast(c.get(), py::return_value_policy::reference));
            return result;
        })
        // Geometry
        .def("geometry", &Widget::geometry)
        .def("set_geometry", &Widget::setGeometry)
        .def("size_hint", &Widget::sizeHint)
        .def("absolute_rect", &Widget::absoluteRect)
        .def_property_readonly("x", &Widget::x)
        .def_property_readonly("y", &Widget::y)
        .def_property_readonly("width", &Widget::width)
        .def_property_readonly("height", &Widget::height)
        // Layout
        .def("set_layout", [](Widget& w, Layout* layout) {
            w.setLayout(std::unique_ptr<Layout>(layout));
        }, py::arg("layout"), py::keep_alive<1, 0>())  // widget keeps layout alive
        // Style — return writable reference so Python can modify in-place
        .def("style", py::overload_cast<>(&Widget::style),
             py::return_value_policy::reference)
        .def("set_style", &Widget::setStyle)
        // State
        .def_property("enabled", &Widget::isEnabled, &Widget::setEnabled)
        .def_property("visible", &Widget::isVisible, &Widget::setVisible)
        .def("has_focus", &Widget::hasFocus)
        .def("claim_focus", &Widget::claimFocus)
        .def("raise_to_top", &Widget::raiseToTop)
        // Painting
        .def("update", [](Widget& w) { w.update(); })
        // Events
        .def("handle_event", &Widget::handleEvent, py::arg("event"),
             "Handle an event. Returns True if consumed.\n"
             "Override in Python subclasses for custom behavior.\n"
             "Event types: MouseDown, MouseUp, MouseMove, MouseWheel, "
             "KeyDown, KeyUp, FocusIn, FocusOut, ImeComposition.")
        .def("widget_type", &Widget::widgetType)
        .def("can_accept_focus", &Widget::canAcceptFocus)
        // Window
        .def_property_readonly("window", &Widget::window, py::return_value_policy::reference);

    // ========================================================================
    // Widget subclasses
    // ========================================================================

    // --- Button ---
    py::class_<Button, Widget>(m, "Button")
        .def(py::init<const std::string&, Widget*>(),
             py::arg("text")="", py::arg("parent")=nullptr)
        .def_property("text", &Button::text, &Button::setText)
        .def("set_text", &Button::setText)
        .def("on_click", &Button::onClick);

    // --- Label ---
    py::class_<Label, Widget>(m, "Label")
        .def(py::init<const std::string&, Widget*>(),
             py::arg("text")="", py::arg("parent")=nullptr)
        .def_property("text", &Label::text, &Label::setText)
        .def("set_text", &Label::setText);

    // --- TextBox ---
    py::class_<TextBox, Widget>(m, "TextBox")
        .def(py::init<const std::string&, Widget*>(),
             py::arg("text")="", py::arg("parent")=nullptr)
        .def_property("text", &TextBox::text, &TextBox::setText)
        .def("set_text", &TextBox::setText)
        .def_property("multi_line", &TextBox::isMultiLine, &TextBox::setMultiLine)
        .def("copy", &TextBox::copy)
        .def("cut", &TextBox::cut)
        .def("paste", &TextBox::paste)
        .def("select_all", &TextBox::selectAll)
        .def("undo", &TextBox::undo)
        .def("redo", &TextBox::redo)
        .def("can_undo", &TextBox::canUndo)
        .def("can_redo", &TextBox::canRedo)
        .def("on_text_changed", &TextBox::onTextChanged);

    // --- CheckBox ---
    py::class_<CheckBox, Widget>(m, "CheckBox")
        .def(py::init<const std::string&, Widget*>(),
             py::arg("text")="", py::arg("parent")=nullptr)
        .def_property("text", &CheckBox::text, &CheckBox::setText)
        .def("set_text", &CheckBox::setText)
        .def_property("checked", &CheckBox::isChecked, &CheckBox::setChecked)
        .def("set_checked", &CheckBox::setChecked)
        .def("on_toggled", &CheckBox::onToggled);

    // --- RadioButton ---
    py::class_<RadioButton, Widget>(m, "RadioButton")
        .def(py::init<const std::string&, Widget*>(),
             py::arg("text")="", py::arg("parent")=nullptr)
        .def_property("text", &RadioButton::text, &RadioButton::setText)
        .def("set_text", &RadioButton::setText)
        .def_property("checked", &RadioButton::isChecked, &RadioButton::setChecked)
        .def("set_checked", &RadioButton::setChecked)
        .def("on_toggled", &RadioButton::onToggled);

    // --- Slider ---
    py::class_<Slider, Widget>(m, "Slider")
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        .def_property("value", &Slider::value, &Slider::setValue)
        .def("set_value", &Slider::setValue)
        .def("set_range", &Slider::setRange)
        .def_property_readonly("minimum", &Slider::minimum)
        .def_property_readonly("maximum", &Slider::maximum)
        .def("on_value_changed", &Slider::onValueChanged);

    // --- ListBox ---
    py::class_<ListBox, Widget>(m, "ListBox")
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        .def("add_item", &ListBox::addItem)
        .def("remove_item", &ListBox::removeItem)
        .def("clear", &ListBox::clear)
        .def_property_readonly("count", &ListBox::count)
        .def("item", &ListBox::item)
        .def_property("selected_index", &ListBox::selectedIndex, &ListBox::setSelected)
        .def("set_selected", &ListBox::setSelected)
        .def("on_selection_changed", &ListBox::onSelectionChanged);

    // --- ComboBox ---
    py::class_<ComboBox, Widget>(m, "ComboBox")
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        .def("add_item", &ComboBox::addItem)
        .def("remove_item", &ComboBox::removeItem)
        .def("clear", &ComboBox::clear)
        .def_property_readonly("count", &ComboBox::count)
        .def("current_text", &ComboBox::currentText)
        .def_property("current_index", &ComboBox::currentIndex, &ComboBox::setCurrentIndex)
        .def("set_current_index", &ComboBox::setCurrentIndex)
        .def("on_selection_changed", &ComboBox::onSelectionChanged);

    // --- ProgressBar ---
    py::class_<ProgressBar, Widget>(m, "ProgressBar")
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        .def_property("value", &ProgressBar::value, &ProgressBar::setValue)
        .def("set_value", &ProgressBar::setValue)
        .def("set_range", &ProgressBar::setRange)
        .def_property("indeterminate", &ProgressBar::indeterminate,
                      &ProgressBar::setIndeterminate);

    // --- TabWidget ---
    py::class_<TabWidget, Widget>(m, "TabWidget")
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        .def("add_tab", &TabWidget::addTab)
        .def("remove_tab", &TabWidget::removeTab)
        .def_property_readonly("count", &TabWidget::count)
        .def_property("current_index", &TabWidget::currentIndex,
                      &TabWidget::setCurrentIndex)
        .def("tab_content", &TabWidget::tabContent, py::return_value_policy::reference)
        .def("current_content", &TabWidget::currentContent,
             py::return_value_policy::reference);

    // --- Image ---
    py::class_<Image, Widget>(m, "Image")
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        .def("load", &Image::load)
        .def_property_readonly("path", &Image::path);


    // --- ContextMenu, MenuBar, Tooltip — TODO: fix unique_ptr issues ---

    // --- ScrollArea ---
    py::class_<ScrollArea, Widget>(m, "ScrollArea")
        .def(py::init<Widget*>(), py::arg("parent")=nullptr)
        .def("set_widget", [](ScrollArea& sa, Widget* widget) {
            sa.setWidget(std::unique_ptr<Widget>(widget));
        }, py::arg("widget"), py::keep_alive<1, 0>())
        .def("widget", &ScrollArea::widget, py::return_value_policy::reference);

    // ========================================================================
    // Logging
    // ========================================================================

    m.def("log_info", [](const std::string& cat, const std::string& msg) {
        Logger::instance().log(LogLevel::Info, cat.c_str(), "%s", msg.c_str());
    });
    m.def("log_warn", [](const std::string& cat, const std::string& msg) {
        Logger::instance().log(LogLevel::Warn, cat.c_str(), "%s", msg.c_str());
    });
    m.def("log_error", [](const std::string& cat, const std::string& msg) {
        Logger::instance().log(LogLevel::Error, cat.c_str(), "%s", msg.c_str());
    });
}
