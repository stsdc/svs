import curses


def log_box(h, w, y, x):
    wrapper = curses.newwin(h, w, y, x)
    wrapper.box()
    box = wrapper.derwin(h - 2, w - 2, 1, 1)
    wrapper.refresh()
    box.refresh()
    box.scrollok(True)
    box.idlok(True)
    box.leaveok(True)
    return box
