import json
from math import sqrt, pow
from os import walk

from matplotlib.pyplot import plot, ylabel, title, legend, savefig, clf, close, bar

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
        if 'animal' in value.keys():
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
        else:
            continue
        bug = None
        if 'bug' in value.keys():
            bug = Point(value['bug']['x'], value['bug']['y'], value['bug']['z'],
                        timeStamp, classifier)
        classifierResults.append(DataInFrame(animal, bug, timeStamp, classifier))
    return classifierResults


if __name__ == '__main__':
    with open('readerConfig.json', 'r') as f:
        config = json.load(f)
    jsonDir = config['pathToJsonsDir']
    allStacks = {}
    timeStampStackSize = 25 * 60 * 5  # 5 minutes
    for (dirpath, dirnames, jsonFiles) in walk(jsonDir):
        for jsonFile in jsonFiles:
            miceNumber = jsonFile.split('_')[0]
            weekNumber = jsonFile.split('_')[1].split('.')[0]
            if miceNumber not in allStacks.keys():
                allStacks[miceNumber] = {}

            jsonFile = jsonDir + jsonFile
            results = readJsonFile(jsonFile)
            stacks = []
            for result in results:
                if result.timeStamp % timeStampStackSize == 0:
                    stacks.append([0, 0])
                if result.animal.tail.x < result.animal.nose.x < 200:
                    stacks[-1][0] += 1
                elif result.animal.tail.x > result.animal.nose.x > 470:
                    stacks[-1][0] += 1
                elif result.animal.nose.x < result.animal.tail.x < 250:
                    stacks[-1][1] += 1
                elif result.animal.nose.x > result.animal.tail.x > 470:
                    stacks[-1][1] += 1
            allStacks[miceNumber][weekNumber] = stacks
            with open("../datasets/resultExp4.txt", "a") as file:
                print("reading file: " + jsonFile, file=file)
                print("max time stamp: " + str(results[-1].timeStamp), file=file)
                for index, stack in enumerate(stacks):
                    print(
                        "stack range: " + str(index * timeStampStackSize) + "-" + str((index + 1) * timeStampStackSize),
                        file=file)
                    print("amount of looking in side: " + str(stack[0]), file=file)
                    print("amount of looking out side: " + str(stack[1]), file=file)
                    print("not in corners: " + str(timeStampStackSize - stack[0] - stack[1]), file=file)
                    print("###############################################",file=file)
                print("\n\n\n", file=file)
