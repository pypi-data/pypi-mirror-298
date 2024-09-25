from dearpygui.dearpygui import *
from screeninfo import get_monitors
from screeninfo.screeninfo import Monitor


def get_current_monitor() -> Monitor:
    """Determines the monitor on which the Dear PyGui window is currently displayed."""
    viewport_pos = get_viewport_pos()  # Get the current position of the viewport
    vp_x, vp_y = viewport_pos
    vp_width = get_viewport_width()
    vp_height = get_viewport_height()

    # Calculate the window's bounds
    window_left = vp_x
    window_right = vp_x + vp_width
    window_top = vp_y
    window_bottom = vp_y + vp_height

    # Check which monitor the window is on
    for index, monitor in enumerate(get_monitors()):
        monitor_left = monitor.x
        monitor_right = monitor.x + monitor.width
        monitor_top = monitor.y
        monitor_bottom = monitor.y + monitor.height

        # Check if the window's top-left corner is within this monitor's bounds
        if (window_left >= monitor_left and window_right <= monitor_right and
                window_top >= monitor_top and window_bottom <= monitor_bottom):
            return monitor

    print("Window position could not be determined within monitor bounds.")
    return None


def get_item_prop(id, prop: str | list[str]):
    config = get_item_configuration(id)
    if config is None:
        return None

    if isinstance(prop, str):
        return config.get(prop, None)
    elif isinstance(prop, list):
        props = {}
        for p in prop:
            props[p] = config.get(p, None)
        return props
    else:
        return None
