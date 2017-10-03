import curses


def header_widget(h, w, y, x):
    header = curses.newwin(h, w, y, x)
    curses.init_pair(44, 43, 0)
    header.bkgd(' ', curses.color_pair(44) | curses.A_BOLD)
    text = "Synergia Vision System"
    header.addstr(0, (w/2)-len(text)/2, text)
    header.refresh()
