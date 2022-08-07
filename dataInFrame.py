from analysisTools.Point import Point
from analysisTools.animal import Animal


class DataInFrame:
    def __init__(self, animal: Animal, bug: Point, timeStamp: int, classification=''):
        """
        param animal: the animal data in this time stamp
        :param bug: the bug data in this time stamp
        :param timeStamp: the measurement time stamp
        """
        self.animal = animal
        self.bug = bug
        self.timeStamp = timeStamp
        self.classification = classification

    def __dict__(self):
        if self.bug is not None:
            return {'animal': self.animal.__dict__(), 'bug': self.bug.__dict__(), 'timeStamp': self.timeStamp,
                    'classification': self.classification}
        else:
            return {'animal': self.animal.__dict__(), 'timeStamp': self.timeStamp, 'classification': self.classification}
