import math;
def reluActivationFunction(inputValue):
    if(inputValue<1):
        return 0;
    else:
        return 1;
    
def tanhActivationFunction(inputValue):
    return math.tanh(inputValue)
def thresholdActivationFunction(inputValue):
    if(inputValue<0):
        return 0;
    else:
        return 1;
def activationFunc(inputValue, functionType):
    if(functionType == "threshold"):
        return thresholdActivationFunction(inputValue)
    elif(functionType == "relu"):
        val =reluActivationFunction(inputValue);
        if val == 0:
            return 0;
        else:
            return 1;
    elif(functionType== "tanh"):
        val = tanhActivationFunction(inputValue);
        if(val<0):
            return 0;
        else:
            return 1;
    else:
        print "Invalid Function Type";