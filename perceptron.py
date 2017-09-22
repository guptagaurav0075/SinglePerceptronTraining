from manageNBF import *
from manageTF import *
import sys;


arguments = sys.argv;
if(len(arguments)!=8):
    print "Number of arguments are not correct"
    exit(1);
else:
    # python perceptron.py activation training_alg ground_file distribution num_train num_test epsilon
    activation = arguments[1];
    training_alg = arguments[2];
    ground_file = arguments[3];
    distribution = arguments[4];
    num_train = int(arguments[5]);
    num_test = int(arguments[6]);
    epsilon = float(arguments[7]);
try:

    # fileObject = open('/Users/Gaurav/Projects/Python/Homework1/NBF.txt', 'r');
    # fileObject = open('/Users/Gaurav/Projects/Python/Homework1/TF.txt', 'r');
    fileObject = open(ground_file, 'r');

    lines = fileObject.readlines()
    matchNBF = re.match('(\s)*NBF(\s)*', lines[0], re.X)
    matchTF = re.match('TF', lines[0], re.X)
    if matchNBF:
        manageNBFOperation(expression=lines, activation=activation,training_alg=training_alg, num_test=num_test, num_train=num_train, epsilon=epsilon)
        # manageNBFOperation(expression=lines, activation="threshold",training_alg="perceptron", num_test=250, num_train=500, epsilon=0.2)


    elif matchTF:
        # print "Found a match in threshold function";
        manageTFOperation(expressions=lines, activation=activation,training_alg=training_alg, num_test=num_test, num_train=num_train, epsilon=epsilon,distribution=distribution)
        # manageTFOperation(expressions=lines, activation="relu",training_alg="winnow", num_test=250, num_train=500, epsilon=0.2,distribution="sphere")
        # print line

    else:
        print "NOT PARSEABLE"


except IOError:
   print("Error: can\'t find file or read data")
else:
   fileObject.close()