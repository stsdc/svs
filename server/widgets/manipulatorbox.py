from box import Box


class ManipulatorBox(Box):
    def __init__(self, h, w, y, x):
        super(ManipulatorBox, self).__init__(h, w, y, x)

        self._thread = None

        self.title("Manipulator")

        self.add(0, 0, "TIME:")
        self.add(0, 7, "%16s" % "N/A")

        self.add(1, 0, "ADC0:")
        self.add(1, 7, "%16s" % "N/A")

        self.add(2, 0, "ADC1:")
        self.add(2, 7, "%16s" % "N/A")

        self.add(3, 0, "ADC2:")
        self.add(3, 7, "%16s" % "N/A")

        self.set_colors_scheme()

    def update(self, data):
        if data is not None:
            self.add(0, 7, "%16s" % data, self.default_colors)
        else:
            self.add(0, 7, "%16s" % "N/A", self.default_colors)

