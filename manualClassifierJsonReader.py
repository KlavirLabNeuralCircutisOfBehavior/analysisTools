import json
import math
from time import sleep
from Point import Point
from animal import Animal
from dataInFrame import DataInFrame


def readJsonFile(jsonFileName: str):
    result = None
    with open(jsonFileName, "r") as f:
        result = json.load(f)
    classifierResults = []
    for value in result:
        timeStamp = value['timeStamp']
        classifier = value['classification']
        nose = Point(value['animal']['nose']['x'], value['animal']['nose']['y'], value['animal']['nose']['z'],
                     timeStamp, classifier)
        leftEar = Point(value['animal']['leftEar']['x'], value['animal']['leftEar']['y'],
                        value['animal']['leftEar']['z'],
                        timeStamp, classifier)
        rightEar = Point(value['animal']['rightEar']['x'], value['animal']['rightEar']['y'],
                         value['animal']['rightEar']['z'],
                         timeStamp, classifier)
        tail = Point(value['animal']['tail']['x'], value['animal']['tail']['y'], value['animal']['tail']['z'],
                     timeStamp, classifier)
        animal = Animal(nose, leftEar, rightEar, tail, timeStamp)
        bug = None
        if 'bug' in value.keys():
            bug = Point(value['bug']['x'], value['bug']['y'], value['bug']['z'],
                        timeStamp, classifier)
        classifierResults.append(DataInFrame(animal, bug, timeStamp, classifier))
    return classifierResults


if __name__ == '__main__':
    with open('readerConfig.json', 'r') as f:
        config = json.load(f)
    results = readJsonFile(config['pathToJsonFile'])
    for result in results:
        print(result)
