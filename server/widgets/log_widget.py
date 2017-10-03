import curses
from log import setup_log


def log_box(h, w, y, x):
    wrapper = curses.newwin(h, w, y, x)
    wrapper.box()
    wrapper.addstr(0, 2, "Logs")
    box = wrapper.derwin(h - 2, w - 2, 1, 1)
    wrapper.refresh()
    box.refresh()
    box.scrollok(True)
    box.idlok(True)
    box.leaveok(True)
    setup_log(box)
    return box
