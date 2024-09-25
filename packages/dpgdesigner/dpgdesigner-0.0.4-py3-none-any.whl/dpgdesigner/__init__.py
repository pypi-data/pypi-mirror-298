from dearpygui.dearpygui import *
from . import style_theme
from . import utils


class PlacerBase:
    def __init__(self, name: str, color: tuple[int, int, int, int] = (0, 0, 0, 255)) -> None:
        with window(label=f"add_{name.lower()}", width=130, height=40, min_size=(130, 40), collapsed=True, no_close=True, no_resize=True, no_title_bar=True, no_scrollbar=True) as self.id:
            self.x = 0
            self.y = 0
            self.rest_x = 0
            self.rest_y = 0
            self.mox = 0
            self.moy = 0
            self.first_press = False
            self.text = add_text(name)
        self.color = color
        self.theme = style_theme.create_placer_item_theme(color)
        bind_item_theme(self.id, self.theme)


class PlacerWidget(PlacerBase):
    def __init__(self, name: str, color: tuple[int, int, int, int] = (0, 0, 0, 255)) -> None:
        super().__init__(name, color)


class PlacerItem(PlacerBase):
    def __init__(self, name: str, color: tuple[int, int, int, int], widget_type: type) -> None:
        super().__init__(name, color)
        self.widget_type = widget_type


class PlacerChildWindow(PlacerWidget):
    def __init__(self) -> None:
        super().__init__(name="", color=(43, 89, 27, 255))


class PlacerButton(PlacerWidget):
    def __init__(self) -> None:
        super().__init__(name="", color=(27, 61, 89, 255))


class PlacerSlider(PlacerWidget):
    def __init__(self) -> None:
        super().__init__(name="", color=(105, 75, 19, 255))


class DPGDesigner:
    def __init__(self) -> None:

        self.width = 1400
        self.height = 900

        create_context()

        create_viewport(
            title="DPG Designer",
            width=self.width,
            height=self.height,
            min_width=900,
        )

        set_viewport_resize_callback(
            lambda sender, app_data: self.on_viewport_resize(app_data[0], app_data[1]))

        self.frame_count = 0

        def runner():
            self.frame_count += 1
            self.on_viewport_resize(
                get_viewport_width(), get_viewport_height())
            set_frame_callback(self.frame_count + 1, runner)

        set_frame_callback(1, runner)

        monitor = utils.get_current_monitor()
        if monitor:
            set_viewport_pos(
                (monitor.width * 0.5 - self.width * 0.5,
                 monitor.height * 0.5 - self.height * 0.5)
            )

        setup_dearpygui()
        show_viewport()
        bind_theme(style_theme.create_theme_modern())
        self.create_interface()
        start_dearpygui()

    def create_interface(self):
        with window(label="Menu Bar", tag="menu_bar", no_resize=True, no_collapse=True, no_move=True, no_close=True, no_title_bar=True, min_size=(0, 0), no_scrollbar=True, no_bring_to_front_on_focus=True) as self.window_menu_bar:
            with group(horizontal=True, horizontal_spacing=2):
                self.file_menu = add_combo(default_value="File", items=[
                    "New", "Open", "Save", "--", "Settings"
                ], width=75, no_arrow_button=True, callback=lambda sender, data: self.on_menu_item_selected(id=sender, menu="File", item=data))
                self.help_menu = add_combo(default_value="Help", items=[
                    "Documentation"
                ], width=75, no_arrow_button=True, callback=lambda sender, data: self.on_menu_item_selected(id=sender, menu="Help", item=data))

        with window(label="Tool Box", tag="tool_box", no_resize=True, no_collapse=True, no_move=True, no_close=True, no_scrollbar=True, no_bring_to_front_on_focus=True) as self.window_tool_box:
            with child_window(label="mini_menu") as self.child_window_mini_menu:
                add_text("Mini Menu")
            with child_window(label="item box") as self.child_window_item_box:
                add_text("Item Box")

        with window(label="Properties", tag="properties", no_resize=True, no_collapse=True, no_move=True, no_close=True, no_scrollbar=True, no_bring_to_front_on_focus=True) as self.window_properties:
            pass

        with window(label="Designer Window", tag="designer_window", no_resize=True, no_collapse=True, no_move=True, no_close=True, no_scrollbar=True, no_bring_to_front_on_focus=True) as self.window_designer_window:
            pass

        self.placers: list[PlacerItem] = []

        self.placers.append(PlacerItem(
            "Child Window", (43, 89, 27, 255), PlacerChildWindow))
        self.placers.append(PlacerItem(
            "Button", (27, 61, 89, 255), PlacerButton))
        self.placers.append(PlacerItem(
            "Slider", (105, 75, 19, 255), PlacerSlider))

        self.is_mouse_down = False
        with handler_registry():
            add_mouse_down_handler(
                0, callback=self.on_mouse_down)
            add_mouse_drag_handler(
                0, 10, callback=self.on_mouse_drag)
            add_mouse_release_handler(
                0, callback=self.on_mouse_release)

        self.on_viewport_resize(get_viewport_width(), get_viewport_height())

    def on_viewport_resize(self, width, height):
        view_height = height - 40

        window_menu_bar_width = width
        window_menu_bar_height = 40
        configure_item(
            self.window_menu_bar,
            width=window_menu_bar_width,
            height=window_menu_bar_height,
            pos=(0, 0)
        )

        window_tool_box_width = 300
        window_tool_box_height = view_height - window_menu_bar_height
        configure_item(
            self.window_tool_box,
            width=window_tool_box_width,
            height=window_tool_box_height,
            pos=(0, window_menu_bar_height)
        )

        window_properties_width = 400
        window_properties_height = view_height - window_menu_bar_height
        configure_item(
            self.window_properties,
            width=window_properties_width,
            height=window_properties_height,
            pos=(width - window_properties_width, window_menu_bar_height)
        )

        window_designer_window_width = width - \
            window_tool_box_width - window_properties_width - 50
        window_designer_window_height = view_height - 50 - window_menu_bar_height
        configure_item(
            self.window_designer_window,
            width=window_designer_window_width,
            height=window_designer_window_height,
            pos=(window_tool_box_width + 25, 25 + window_menu_bar_height)
        )

        child_window_mini_menu_height = 200
        configure_item(
            self.child_window_mini_menu,
            width=window_tool_box_width - 20,
            height=child_window_mini_menu_height,
            pos=(10, 33)
        )

        configure_item(
            self.child_window_item_box,
            width=window_tool_box_width - 20,
            height=window_tool_box_height - child_window_mini_menu_height - 33 - 20,
            pos=(10, 33 + child_window_mini_menu_height + 10)
        )

        for i, placer in enumerate(self.placers):
            placer.rest_x = 20
            placer.rest_y = 33 + child_window_mini_menu_height + \
                10 + 40 + i * 45 + window_menu_bar_height
            placer.x = placer.rest_x
            placer.y = placer.rest_y
            configure_item(
                placer.id,
                pos=(placer.x, placer.y)
            )

    def on_mouse_down(self, sender, data):
        pos = get_mouse_pos(local=False)
        for placer in self.placers:
            if placer.first_press == False:
                placer.first_press = True
                placer.mox = placer.x - pos[0]
                placer.moy = placer.y - pos[1]

    def on_mouse_drag(self, sender, data):
        des_win_pos = get_item_pos(self.window_designer_window)
        pos = get_mouse_pos(local=False)
        self.is_mouse_down = True
        for placer in self.placers:
            if is_item_hovered(placer.id):
                placer_pos = get_item_pos(placer.id)
                placer_pos[0] = snap(pos[0] + placer.mox,
                                     10) + des_win_pos[0] % 10
                placer_pos[1] = snap(pos[1] + placer.moy,
                                     10) + des_win_pos[1] % 10 + 3
                configure_item(
                    placer.id,
                    pos=placer_pos
                )

    def on_mouse_release(self, sender, data):
        self.is_mouse_down = False
        for placer in self.placers:
            placer.first_press = False
            if is_item_hovered(placer.id):
                placer.x = placer.rest_x
                placer.y = placer.rest_y
                set_item_pos(placer.id,
                             (placer.x, placer.y))

    def on_menu_item_selected(self, id: int | str, menu: str, item: str):
        set_value(id, menu)
        print(menu)
        print(item)


def snap(value, size=1):
    return round(value / size) * size

