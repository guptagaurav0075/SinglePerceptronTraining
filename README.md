# SinglePerceptronTraining

Developed a program to train on Nested Boolean Functions and Threshold Functions.
A file called ground_file could have either a Nested Boolean Funtion or Threshold Function.
A file with Nested Boolean Function should follow the following the regular epression:
NBF
([+|-]\d+(\s+(:?AND|OR)\s+\d+)*)?

In simpler terms, it means as follows:

NBF

+1 OR -2 AND +5 AND +3

This file represents the boolean function on five inputs f(x1,x2,x3,x4,x5):=(((x1∨¬x2)∧x5)∧x3).
A file containing a threshold function looks like (where the second and third line are regex):

TF

[+|-]\d+

([+|-]\d+(\s+[+|-]\d+)*)?


For example,

TF

+15

+10 -5 +30


which represents the function f:ℝ3→{0,1} given by f(x1,x2,x3)=1 if and only 10x1−5x2+30x3≥15.

While training based on the ground_file, the output would look like:
x1,x2,...,xn:y:[update|no update]\n
for example, if the weights did not change when training on the input-output example ([1,1,0,0],1) then program outputs:
1,1,0,0:1:no update
Once the function is trained, it will calculate the accuracy on test data. Here, ypred is what the trained perceptron would compute on x⃗ , yactual is when the ground function outputs on x⃗ , and error is ∣∣ypred−yactual∣∣. For example, if the test vector was [1,0,1,1] and the prediction of the perceptron on this input was 1 and this was also the ground function's value, then the line would look like:
1,0,1,1:1:1:0
After the last line output because of test data, program computes the average error on the test data, output it followed by a line with the value of epsilon, followed by a line which either says "TRAINING SUCCEEDED" or "TRAINING FAILED" depending on whether the average was less than epsilon. Below is an example of how this might look:
Average Error:0.19
Epsilon:0.2
TRAINING SUCCEEDED

In order to test the working of the Single Perceptron, one need to issue the following command

python perceptron.py activation training_alg ground_file distribution num_train num_test epsilon

In this command, values that are mapped is as follows:
1. activation could have the following values : threshold, tanh, relu
    1.a. threshold : this uses the step activation function.
    1.b. tanh : This uses the activation function tanh provided by library math in python
    1.c. relu : This uses the activation function relu.

2. training_alg:
    2.a. perceptron or
    2.b. winnow.
3. ground_file: This provides the information about the location of ground_file which could have either NBF or TF.
4. distribution: this command helps in determining the values that training and test draws from.
    4.a. spere : this uses the uniform unit spherical distribution.
    4.b bool : this uses uniform boolean distribution. If ground_file has NBF, then distribution is always bool irrespective of what the command line has provided.
5. num_train: its an integer value defining the number of training examples that should be generated and tested for the NBF or TF.
6. num_test: its an integer value defining the number of test examples that should be generated and tested for NBF or TF.
7. epsilon: epsilon is the max average error that is allowed, if the average error of test cases is beyond the defined epsilon value, the training fails otherwise training succeeds.


Below is a concrete example of filling in the parameters in this line:

python perceptron.py relu perceptron my_nested_bool_fn.txt bool 500 250 0.2