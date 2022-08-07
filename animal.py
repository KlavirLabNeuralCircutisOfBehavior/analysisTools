from Point import Point


class Animal:
    def __init__(self, nose: Point, leftEar: Point, rightEar: Point, tail: Point, timeStamp: int):
        """
        param x: the axis x
        :param y: the axis y
        :param z: the axis z
        :param timeStamp: the measurement time stamp
        :param label: in order to find clusters
        """
        self.nose = nose
        self.leftEar = leftEar
        self.rightEar = rightEar
        self.timeStamp = timeStamp
        self.tail = tail

    def __dict__(self):
        return {'nose': self.nose.__dict__(), 'leftEar': self.leftEar.__dict__(), 'rightEar': self.rightEar.__dict__(),
                'timeStamp': self.timeStamp, 'tail': self.tail.__dict__()}

    def __eq__(self, other):
        return (self.nose, self.leftEar, self.rightEar) == (other.nose, other.leftEar, other.rightEar)

    def copy(self):
        return Animal(self.nose, self.leftEar, self.rightEar, self.tail, self.timeStamp)
