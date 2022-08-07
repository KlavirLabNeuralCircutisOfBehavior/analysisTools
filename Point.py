class Point:
    def __init__(self, x, y, z, timeStamp=0, label=-1):
        """
        param x: the axis x
        :param y: the axis y
        :param z: the axis z
        :param timeStamp: the measurement time stamp
        :param label: in order to find clusters
        """
        self.x = x
        self.y = y
        self.z = z
        self.timeStamp = timeStamp
        self.label = label

    def __dict__(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'timeStamp': self.timeStamp, 'label': self.label}

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def copy(self):
        return Point(self.x, self.y, self.z, self.timeStamp, self.label)
