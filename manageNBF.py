from helpfulFunctions import *;
from activationFunctions import *


# this function checks whether the provided file has a valid NBF syntax or not
def isValidNBF(lines):
    val = lines[1].strip(" ")
    matchNBFregEx = re.match("^([+|-]\d+(\s+(:?AND|OR)\s+\d+)*?)", val, re.M)
    if matchNBFregEx:
        return True;
    else:
        return False;

def fetchNBFExpression(lines):
    if isValidNBF(lines):
        print "isTrue"
        return NBFExpression(lines[1])
    else:
        print "NOT PARSEABLE";
        return False;


def testNBFExamples(training_alg, num_test, activation, epsilon, line):
    index = 0;
    testErr = 0.0
    while (index < num_test):
        vector = generateVector(line['maxVectorSize'], "bool");
        actualOutput = evaluateNBF(line, vector)
        predictedValue = predictIntermediateOutputValue(vector)
        outputY = activationFunc(inputValue=predictedValue - threshold, functionType=activation)
        if(outputY!=actualOutput):
            testErr+=1;
        index = index + 1
        printVal = printVector(vector=vector)
        printVal = printVal.strip(",")
        printVal = printVal+":"+str(outputY)+":"+str(actualOutput)+":"+str(abs(outputY-actualOutput))
        print printVal
        # writeToFile(printVal)
    avg_err = testErr/num_test;
    avg_err_str = "Average Error:"+str(avg_err)
    epsilon_str = "Epsilon:"+str(epsilon)
    result = ""
    if(avg_err<epsilon):
        result = "TRAINING SUCCEEDED"
    else:
        result = "TRAINING FAILED"

    print avg_err_str,"\n",epsilon_str,"\n",result
    # writeToFile(avg_err_str)
    # writeToFile(epsilon_str)
    # writeToFile(result)



def trainNBFExamples(training_alg, num_train, activation, line):
    global threshold
    index = 0;
    while (index < num_train):
        vector = generateVector(line['maxVectorSize'], "bool");
        actualOutput = evaluateNBF(line, vector)
        predictedValue = predictIntermediateOutputValue(vector)
        outputY = activationFunc(inputValue=predictedValue - threshold, functionType=activation)
        updateWeightBasedOnTrainingAlg(training_alg=training_alg, actualOutput=actualOutput, predictedOutput=outputY,
                                       vector=vector)
        index = index + 1

def NBFExpression(line):
    lineCopy = line[:]
    lineCopy = lineCopy.strip(" ")
    values = [];
    operations = [];
    stripLen = getValueAndAppend(lineCopy, values)
    lineCopy = lineCopy[stripLen:]
    lineCopy = lineCopy.strip(" ")

    while(len(lineCopy)!=0):
        stripLen = getOperatorAndAppend(lineCopy, operations)
        lineCopy = lineCopy[stripLen:]
        lineCopy = lineCopy.strip(" ")
        stripLen = getValueAndAppend(lineCopy, values)
        lineCopy = lineCopy[stripLen:]
        lineCopy = lineCopy.strip(" ")

    dict = {'operations':operations, 'values':values, 'maxVectorSize':abs(max(values, key=abs))}
    return dict;

# evaluateNBFs(expressionDict, vectors) this function evaluates NBF for one single vector
# This is called from evaluateNBFs function which has list of all the vectors
def evaluateNBF(expressionDict, vector):
    values = expressionDict['values']
    operations = expressionDict['operations']
    # print values, operations, vector
    oldOutput = getValueOfIndex(vector[abs(values[0])-1], values[0])
    index = 1;
    while(index<len(values)):
        tempVal = getValueOfIndex(vector[abs(values[index]) - 1], values[index])
        if(operations[index-1]=='or'):
            # print oldOutput, " or ", tempVal
            oldOutput = oldOutput or tempVal
        else:
            # print oldOutput, " and ", tempVal
            oldOutput = oldOutput and tempVal
        index+=1;
        # print "Output : ",oldOutput
    # print values, operations, vector
    return oldOutput;

def manageNBFOperation(expression, activation,training_alg, num_test, num_train, epsilon):
    line = fetchNBFExpression(expression)
    if (line != False):
        generateWeightBasedOnTrainingAlg(training_alg, line);
        generateVector(training_alg, line)
        print line
        trainNBFExamples(line = line,training_alg=training_alg, num_train=num_train, activation=activation)
        testNBFExamples(line = line,training_alg=training_alg, num_test=num_test, activation=activation, epsilon=epsilon)
