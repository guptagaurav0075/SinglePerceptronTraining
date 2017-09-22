import re;
import random;
import math;



threshold = 0;
weightVector = []
alphaValue = 2.5;


# This function in determining wether the compliment of the function is supposed to be calculated or not.
def getValueOfIndex(valueAtIndex, indexValue):
    if(indexValue<0):
        # print "XORVAlue : ",(valueAtIndex ^ 1)," Normal Value : ", valueAtIndex
        return (valueAtIndex ^ 1);
    else:
        return valueAtIndex;

#function helps in fetching the digit and removing the sign from in front of the digit
def getMaxValue(val):
    val = val.strip(" ");
    val = val.strip("+");
    return int(val)

#this functions takes the whole line, fetches the first digit and calls getMaxValue function to retrieve the digit after that it removes that digit.
def getValueAndAppend(lineCopy, values):
    tempMatch = re.match("^[+|-]\d+", lineCopy[0:])
    if tempMatch:
        values.append(getMaxValue(tempMatch.group()))
        return len(tempMatch.group())

#this function helps in retrieving the operation from the line, operations like AND or OR from nested boolean function line
def getOperatorAndAppend(lineCopy, operations):
    tempMatch = re.match("^(:?AND|OR)", lineCopy[0:])
    if tempMatch:
        operations.append(tempMatch.group().lower())
        return len(tempMatch.group())




def generateVector(vectorSize, type):
    singleVector = []
    index = 0;
    if(type =="bool"):
        while(index<vectorSize):
            index+=1;
            singleVector.append(random.randint(0,1))
    elif(type=="sphere"):
        singleVector =  getVectorForSphere(vectorSize=vectorSize)
    return singleVector
def getVectorForSphere(vectorSize):
    singleVector = []
    index = 0;
    while (index < vectorSize):
        index += 1;
        singleVector.append(random.random())
    return generateNormalizedVector(vector=singleVector)

def generateNormalizedVector(vector):
    index = 0;
    sum1 = 0
    while(index<len(vector)):
        sum1 += pow(vector[index], 2);
        index +=1;
    sum1 = math.sqrt(sum1)
    index=0;
    while(index<len(vector)):
        vector[index] = vector[index]/sum1
        index+=1;
    return vector;

def generateWeightBasedOnTrainingAlg(trainingAlg, line):
    if (trainingAlg == "perceptron"):
        isPerceptron(line['maxVectorSize'])
    elif (trainingAlg == "winnow"):
        isWinnow(line['maxVectorSize'])
    else:
        print "Training algorithm should be winnow or perceptron"
        exit(1)


def updateThresholdPerceptron(operation):
    global threshold;
    if(operation=="add"):
        threshold +=1
    elif(operation == "sub"):
        threshold -=1


def updateWeightVectorPerceptron(xVector, operation):
    global weightVector;
    index =0;
    while(index<len(xVector)):
        if(operation == "add"):
            weightVector[index]+=xVector[index]
        elif(operation == "sub"):
            weightVector[index]-=xVector[index]
        index+=1


def updateWeightVectorWinnow(xVector, operation):
    global weightVector;
    global alphaValue;
    index =0;
    while(index<len(xVector)):
        if(operation == "add"):
            weightVector[index]=pow(alphaValue,xVector[index])*weightVector[index];
        elif(operation == "sub"):
            weightVector[index]=pow(alphaValue,-xVector[index])*weightVector[index];
        index+=1

#this function helps in calculating sigma, i.e., wixi
def predictIntermediateOutputValue(xVector):
    global weightVector;
    sum = 0;
    index = 0;
    while(index<len(xVector)):
        sum += xVector[index]*weightVector[index];
        index+=1
    return sum;

#this function helps in generating a weight vector with random values with value greater than 1
def generateWeightVector(vectorSize):
    global weightVector;
    index = 0;
    while(index<vectorSize):
        val = random.randint(1, 100);
        weightVector.append(val)
        index +=1


#this function gerates a vector with all values assigned to 0
def generateZeroWeightVector(vectorSize):
    global weightVector;
    index = 0;
    while(index<vectorSize):
        weightVector.append(0)
        index+=1;


def isWinnow(vectorSize):
    global threshold
    threshold = 40;
    generateWeightVector(vectorSize)


def isPerceptron(vectorSize):
    global threshold;
    threshold = 0
    generateZeroWeightVector(vectorSize);

def writeToFile(stringValue):
    fo = open("output.txt",'a');
    fo.write(stringValue)
    fo.write("\n")
    fo.close();

def updateWeightBasedOnTrainingAlg(training_alg, actualOutput, predictedOutput, vector):
    printVal = printVector(vector);
    printVal = printVal.strip(",")
    if(training_alg=="perceptron"):
        if (predictedOutput != actualOutput):
            # update weight and threshold
            if (predictedOutput > actualOutput):
                # false Positive prediction
                updateThresholdPerceptron("add");
                # print "False Positive Prediction"
                # print "Old weight : ", weightVector
                updateWeightVectorPerceptron(xVector=vector, operation="sub");
                # print "New Weight : ", weightVector
            elif (predictedOutput < actualOutput):
                # false Negative prediction
                # print "False Negative Prediction"
                # print "Old Weight : ", weightVector
                updateThresholdPerceptron(operation="sub");
                updateWeightVectorPerceptron(xVector=vector, operation="add")
            printVal = printVal+":"+str(actualOutput)+":update"
        else:
            # printVector(vector);
            printVal = printVal + ":" + str(actualOutput) + ":no update"
    elif(training_alg=="winnow"):

        if (predictedOutput != actualOutput):
            # update weight and threshold
            if (predictedOutput > actualOutput):
                # false Positive prediction
                # print "False Positive Prediction"
                # print "Old weight : ", weightVector
                updateWeightVectorWinnow(xVector=vector, operation="sub");
                # print "New Weight : ", weightVector
            elif (predictedOutput < actualOutput):
                # false Negative prediction
                # print "False Negative Prediction"
                # print "Old Weight : ", weightVector
                updateWeightVectorWinnow(xVector=vector, operation="add")
                # print "New Weight : ", weightVector
            printVal = printVal + ":" + str(actualOutput) + ":update"
        else:
            # printVector(vector);
            printVal = printVal + ":" + str(actualOutput) + ":no update"
    print printVal
    # writeToFile(printVal)



def printVector(vector):
    returnVal = ""
    index = 0;
    while(index<len(vector)):
        returnVal += str(vector[index])
        returnVal += ","
        index +=1
    return returnVal