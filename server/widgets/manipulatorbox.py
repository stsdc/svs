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

        self.add(4, 0, "CURRENT:")
        self.add(4, 9, "%14s" % "N/A")

        self.add(5, 0, "VELOCITY:")
        self.add(5, 11, "%12s" % "N/A")

        self.add(6, 0, "POSITION:")
        self.add(6, 11, "%12s" % "N/A")

        self.set_colors_scheme()

    def update(self, data):
        if data is not None:
            self.add(0, 7, "%16s" % data["time"], self.default_colors)
            self.add(1, 7, "%16s" % data["adc0"], self.default_colors)
            self.add(2, 7, "%16s" % data["adc1"], self.default_colors)
            self.add(3, 7, "%16s" % data["adc2"], self.default_colors)
            self.add(4, 9, "%14s" % data["current"], self.default_colors)
            self.add(5, 11, "%12s" % data["velocity"], self.default_colors)
            self.add(6, 11, "%12s" % data["position"], self.default_colors)
        else:
            self.add(0, 7, "%16s" % "N/A", self.default_colors)

