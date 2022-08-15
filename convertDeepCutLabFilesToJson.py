import json
from os import walk
from typing import List

from Point import Point
from animal import Animal
from dataInFrame import DataInFrame


def readFileToObjectsList(fileName: str, desiredLikelihood=0.9) -> List[DataInFrame]:
    results = []
    with open(fileName) as file:
        for index,rawRow in enumerate(file.readlines()[3:]):
            row = rawRow.split(',')
            try:
                animal = None
                bug = None
                timeStamp = int(row[0])
                if float(row[3]) > desiredLikelihood and float(row[6]) > desiredLikelihood and float(
                        row[9]) > desiredLikelihood and float(row[12]) > desiredLikelihood:
                    nose = Point(float(row[1]), float(row[2]), 0, timeStamp)
                    leftEar = Point(float(row[4]), float(row[5]), 0, timeStamp)
                    rightEar = Point(float(row[7]), float(row[8]), 0, timeStamp)
                    tail = Point(float(row[10]), float(row[11]), 0, timeStamp)
                    timeStamp = timeStamp
                    animal = Animal(nose, leftEar, rightEar, tail, timeStamp)
                else:
                    print("bad likelihood in animal data on line " + str(index))
                if float(row[15]) > desiredLikelihood:
                    bug = Point(float(row[13]), float(row[14]), 0, timeStamp)
                results.append(DataInFrame(animal, bug, timeStamp))
            except Exception as e:
                print("error in file: " + e.args[0])
                results.append(DataInFrame(None, None, 0))
    return results


if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    desiredLikelihood = config['desiredLikelihood']
    dataSetsDir = "../datasets/exp4/"
    for (dirpath, dirnames, filenames) in walk(dataSetsDir):
        for dataSet in filenames:
            results = readFileToObjectsList(dirpath+dataSet,desiredLikelihood)
            with open("../datasets/exp4jsons/"+dataSet.split('.')[0]+".json", 'w') as f:
                json.dump([result.__dict__() for result in results], f)