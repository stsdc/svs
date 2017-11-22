from box import Box


class ManipulatorBox(Box):
    def __init__(self, h, w, y, x):
        super(ManipulatorBox, self).__init__(h, w, y, x)

        # self._thread = None

        self.title("Manipulator")
        self.set_colors_scheme()

        self.add(0, 11, "%13s" % "MOTOR 1", self.bold)
        self.add(0, 29, "%9s" % "MOTOR 2",self.bold)
        self.add(0, 49, "%9s" % "MOTOR 3", self.bold)
        self.add(0, 67, "%9s" % "MOTOR 4", self.bold)

        self.add(0, 0, "0x21", self.bold)
        self.add(1, 0, "CURRENT:", self.bold)
        self.add(2, 0, "VELOCITY:", self.bold)
        self.add(3, 0, "POSITION:", self.bold)

        self.add(5, 0, "0x22", self.bold)
        self.add(6, 0, "CURRENT:", self.bold)
        self.add(7, 0, "VELOCITY:", self.bold)
        self.add(8, 0, "POSITION:", self.bold)

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

    def update(self, data):
        if data[0] is not None:
            self.add(1, 11, "%13s" % data[0]["current1"], self.default_colors)
            self.add(2, 11, "%13s" % data[0]["velocity1"], self.default_colors)
            self.add(3, 11, "%13s" % data[0]["position1"], self.default_colors)

            self.add(1, 28, "%10s" % data[0]["current2"], self.default_colors)
            self.add(2, 28, "%10s" % data[0]["velocity2"], self.default_colors)
            self.add(3, 28, "%10s" % data[0]["position2"], self.default_colors)

            self.add(1, 48, "%10s" % data[0]["current3"], self.default_colors)
            self.add(2, 48, "%10s" % data[0]["velocity3"], self.default_colors)
            self.add(3, 48, "%10s" % data[0]["position3"], self.default_colors)

            self.add(1, 66, "%10s" % data[0]["current4"], self.default_colors)
            self.add(2, 66, "%10s" % data[0]["velocity4"], self.default_colors)
            self.add(3, 66, "%10s" % data[0]["position4"], self.default_colors)

        if data[1] is not None:
            self.add(6, 11, "%13s" % data[1]["current1"], self.default_colors)
            self.add(7, 11, "%13s" % data[1]["velocity1"], self.default_colors)
            self.add(8, 11, "%13s" % data[1]["position1"], self.default_colors)

            self.add(6, 28, "%10s" % data[1]["current2"], self.default_colors)
            self.add(7, 28, "%10s" % data[1]["velocity2"], self.default_colors)
            self.add(8, 28, "%10s" % data[1]["position2"], self.default_colors)

            self.add(6, 48, "%10s" % data[1]["current3"], self.default_colors)
            self.add(7, 48, "%10s" % data[1]["velocity3"], self.default_colors)
            self.add(8, 48, "%10s" % data[1]["position3"], self.default_colors)

            self.add(6, 66, "%10s" % data[1]["current4"], self.default_colors)
            self.add(7, 66, "%10s" % data[1]["velocity4"], self.default_colors)
            self.add(8, 66, "%10s" % data[1]["position4"], self.default_colors)
        else:
            self.add(1, 11, "%13s" % "N/A", self.default_colors)



