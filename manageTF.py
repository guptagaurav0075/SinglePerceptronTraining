from helpfulFunctions import *
from activationFunctions import *

#this function evaluates a threshold function as per given ground file
def evalTF(vector, expression):
    index = 0;
    inputX = expression['Value']
    sum = 0;
    while(index<len(vector)):
        sum += vector[index]*inputX[index]
        index +=1;
    if(sum>expression['output']-1):
        return 1;
    else:
        return 0;
# this function checks whether the provided TF is valid or not
def isValidTF(lines):
    lines[1] = lines[1].strip(" ");
    lines[2] = lines[2].strip(" ");
    matchTFregExline2 = re.match("^[+|-]\d+$", lines[1], re.X);
    matchTFregExline3 = re.match("(^[+|-]\d+(\s+[+|-]\d+)*)?$", lines[2], re.X)
    if matchTFregExline2 and matchTFregExline3:
        return True;
    else:
        return False;

# this function takes the lines of input and generate a dictonary which could be utilized to pass the
# values and check whether to fire a perceptron or not based on it's value
def TFExpression(lines):
    value = int (lines[1].strip(" "));
    line2 = lines[2].strip(" ")
    vector=[]
    index = 0;
    maxInput = 0
    while index<len(line2):
        matchDigit = re.match("[+|-]\d+", line2[index :]);
        if matchDigit:
            maxInput+=1
            vector.append(int(matchDigit.group()))
            #print matchDigit.group()
            index += len(matchDigit.group())
            continue
        index+=1;
    thresholdFunction = {'Value':vector, 'output':value, 'maxVectorSize':maxInput}
    # print thresholdFunction
    return thresholdFunction

# this function helps in fetching the
def fetchTFExpression(lines):
    if isValidTF(lines):
        return TFExpression(lines)
    else:
        # print "NOT PARSEABLE"
        return False;

#this function test against vectors, the
def testTFExamples(training_alg, num_test, activation, epsilon, expression,distribution):
    testErr = 0.0
    index = 0;
    global weightVector;
    global threshold;
    while(index<num_test):
        vector = generateVector(expression['maxVectorSize'],distribution)
        actualOutput = evalTF(vector, expression);
        intermediateOutput = predictIntermediateOutputValue(vector);
        outputY = activationFunc(inputValue=intermediateOutput-threshold,functionType=activation)
        if(outputY!=actualOutput):
            testErr += 1
        # else:
        #     print "SameOutput actual: ",actualOutput," prediction: ",outputY
        index +=1;
        printVal = printVector(vector=vector)
        printVal = printVal.strip(",")
        printVal = printVal+":"+str(outputY)+":"+str(actualOutput)+":"+str(abs(outputY-actualOutput))
        print printVal
        # writeToFile(printVal)
    avg_err = testErr / num_test;
    avg_err_str = "Average Error:" + str(avg_err)
    epsilon_str = "Epsilon:" + str(epsilon)
    result = ""
    if (avg_err < epsilon):
        result = "TRAINING SUCCEEDED"
    else:
        result = "TRAINING FAILED"

    print avg_err_str, "\n", epsilon_str, "\n", result
    # writeToFile(avg_err_str)
    # writeToFile(epsilon_str)
    # writeToFile(result)


def trainTFExamples(training_alg, num_train, activation, expression,distribution):

    index = 0;
    global weightVector;
    global threshold;
    while(index<num_train):
        vector = generateVector(expression['maxVectorSize'],distribution)
        actualOutput = evalTF(vector, expression);
        intermediateOutput = predictIntermediateOutputValue(vector);
        outputY = activationFunc(inputValue=intermediateOutput-threshold,functionType=activation)
        updateWeightBasedOnTrainingAlg(training_alg=training_alg,actualOutput=actualOutput,predictedOutput=outputY,vector=vector);
        index +=1;


def manageTFOperation(expressions,activation, training_alg, num_train, num_test, epsilon,distribution):
    expression = fetchTFExpression(expressions);
    if expression == False:
        print "NOT PARSEABLE"
        return;
    else:
        generateWeightBasedOnTrainingAlg(training_alg, expression);
        trainTFExamples(training_alg=training_alg, expression=expression, activation=activation, num_train=num_train,
                        distribution=distribution)
        testTFExamples(training_alg=training_alg, num_test=num_test, activation=activation, epsilon=epsilon,
                       expression=expression, distribution=distribution)
