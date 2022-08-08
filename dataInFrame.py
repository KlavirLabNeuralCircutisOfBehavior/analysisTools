from Point import Point
from animal import Animal


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

    def __str__(self):
        return "timeStamp: " + str(
            self.timeStamp) + " classification: " + str(self.classification) + " animal: " + str(
            self.animal) + " bug: " + str(self.bug)

    def __dict__(self):
        result = {}
        if self.animal is not None:
            result['animal'] = self.animal.__dict__()
        if self.bug is not None:
            result['bug'] = self.bug.__dict__()
        result['timeStamp'] = self.timeStamp
        result['classification'] = self.classification
        return result
