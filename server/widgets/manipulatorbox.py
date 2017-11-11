from box import Box


class ManipulatorBox(Box):
    def __init__(self, h, w, y, x):
        super(ManipulatorBox, self).__init__(h, w, y, x)

        self._thread = None

        self.title("Manipulator")

        self.add(0, 11, "%13s" % "MOTOR 1", self.bold)
        self.add(0, 29, "%9s" % "MOTOR 2",self.bold)
        self.add(0, 49, "%9s" % "MOTOR 3", self.bold)
        self.add(0, 67, "%9s" % "MOTOR 4", self.bold)
        #
        # self.add(0, 7, "%16s" % "N/A")
        #
        self.add(1, 0, "CURRENT:")
        # self.add(1, 7, "%16s" % "N/A")
        #
        self.add(2, 0, "VELOCITY:")
        # self.add(2, 7, "%16s" % "N/A")
        #
        self.add(3, 0, "POSITION:")
        # self.add(3, 7, "%16s" % "N/A")

        # self.add(4, 0, "ADC4:")
        #
        # self.add(4, 0, "CURRENT:")
        # self.add(4, 9, "%14s" % "N/A")
        #
        # self.add(5, 0, "VELOCITY:")
        # self.add(5, 11, "%12s" % "N/A")
        #
        # self.add(6, 0, "POSITION:")
        # self.add(6, 11, "%12s" % "N/A")

        self.set_colors_scheme()

    def update(self, data):
        if data is not None:
            self.add(1, 11, "%13s" % data["current1"], self.default_colors)
            self.add(2, 11, "%13s" % data["velocity1"], self.default_colors)
            self.add(3, 11, "%13s" % data["position1"], self.default_colors)

            self.add(1, 29, "%9s" % data["current2"], self.default_colors)
            self.add(2, 29, "%9s" % data["velocity2"], self.default_colors)
            self.add(3, 29, "%9s" % data["position2"], self.default_colors)

            self.add(1, 49, "%9s" % data["current3"], self.default_colors)
            self.add(2, 49, "%9s" % data["velocity3"], self.default_colors)
            self.add(3, 49, "%9s" % data["position3"], self.default_colors)

            self.add(1, 67, "%9s" % data["current4"], self.default_colors)
            self.add(2, 67, "%9s" % data["velocity4"], self.default_colors)
            self.add(3, 67, "%9s" % data["position4"], self.default_colors)
        else:
            self.add(0, 7, "%16s" % "N/A", self.default_colors)

