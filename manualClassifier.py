import json
import math
from time import sleep

from pynput import keyboard
import cv2

from Point import Point
from animal import Animal
from dataInFrame import DataInFrame


def readFileRowToObject(fileName: str, lineNumber: int, desiredLikelihood=0.9) -> DataInFrame:
    with open(fileName) as file:
        row = file.readlines()[lineNumber].split(',')
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
                print("bad likelihood in animal data on line " + str(lineNumber))
            if float(row[15]) > desiredLikelihood:
                bug = Point(float(row[13]), float(row[14]), 0, timeStamp)
            return DataInFrame(animal, bug, timeStamp)

        except Exception as e:
            print("error in file: " + e.args[0])
    return DataInFrame(None, None, 0)


def on_press(key):
    global classification
    classification = key.char


def on_release(key):
    global classification
    classification = ''


classification = ''
if __name__ == '__main__':
    results = []
    print("welcome to the manual classifier")
    print("please make sure you filled the path's in the config.json file correctly")
    print("press 'q' to quit")
    print("press 'b' to hold the programmer if you need a break")
    print("every time you press and hold a key, the object will be classified with the key you pressed")
    print("at the end we will save the results to a json file")
    print("and than we will create a dictionary for the classification")
    print("press enter to start classifying")
    input()
    with open('config.json', 'r') as f:
        config = json.load(f)
    capture = cv2.VideoCapture(config['videoPath'])
    dataSet = config['pathToDataSetCsv']
    desiredLikelihood = config['desiredLikelihood']
    if desiredLikelihood == '':
        desiredLikelihood = 0.9
    fps = math.floor(capture.get(cv2.CAP_PROP_FPS))
    rowNumber = 3
    animalObject = readFileRowToObject(dataSet, rowNumber)
    adjustToVideo = animalObject.timeStamp
    keyboardListener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    keyboardListener.start()
    userSignals = []
    ret = True
    while adjustToVideo > 1:
        ret, frame = capture.read()
        adjustToVideo -= 1
    while ret:
        ret, frame = capture.read()
        if not ret:
            break
        cv2.imshow('frame', frame)
        cv2.waitKey(1000 // fps)
        animalObject = readFileRowToObject(dataSet, rowNumber, desiredLikelihood)
        rowNumber += 1
        if animalObject.animal is not None:
            userSignal = classification
            if userSignal == 'b':
                print("entering break mode, press 'n' to continue")
                sleep(1)
                userSignal = classification
                while userSignal == '':
                    sleep(0.1)
                    userSignal = classification
            if userSignal == 'q':
                break
            if userSignal != 'n' or userSignal != 'b':
                animalObject.classification = userSignal
            results.append(animalObject)
            userSignals.append(animalObject.classification)

    capture.release()
    cv2.destroyAllWindows()
    keyboardListener.stop()
    print("we are saving results to json, this may take a while, do not shut down the program")
    with open(config['saveResultsPath'], 'w') as f:
        json.dump([result.__dict__() for result in results], f)
    print("please create dictionary for the values of the classification")
    userDictionary = {}
    userSignalsSet = set(userSignals)
    for userSignal in userSignalsSet:
        if userSignal == '':
            userDictionary[userSignal] = "not classified"
            continue
        print("what is the value of the classification: " + str(userSignal))
        userValue = input()
        userDictionary[userSignal] = userValue
        print(userValue)
    with open(config['saveDictionaryPath'], 'w') as f:
        json.dump(userDictionary, f)
    print("thank you, the results saved to " + config['saveResultsPath'] + " and the dictionary to " + config[
        'saveDictionaryPath'])
