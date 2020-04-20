# Decision Tree
[Project Instruction](https://github.com/vctr7/Data_Science/blob/master/decision_tree/Decision_Tree.pdf)

## 1.	Summary of the algorithm

  This code denotes the algorithm of decision tree. It is written in Python and composed with several functions. 

The decision tree has some methods to decrease its error such as information gain, split information, and gini index. I select information gain in this project.

  I used very basic libraries; sys for I/O, math for calculating entropy, numpy for easy transpose matrix.

   

## 2.	Detailed description of codes (for each function) 

This code has several functions including main(). I'll introduce important functions.


    def preprocess(file): Convert the train file into list form.
    
    def caculateAttrInfo(): Calculate the attribute's partial information(entropy).

    def makeSubtree(): Make subtrees of highest gain attribute.
    
    def leaf(): Return the most unique value of leaf node.
    
    def DTProcess(): Recursively complete the structure of the decision tree.
    
    def predict(): Give proper value of given test-transaction by recursively searching the tree.
    
    def classifer(): Classify the test file according to the decision tree.
    
    def save(): save the output file in order.



 
## 3.	Instructions for compiling source codes 

Since I use Python, it has subtle differnece with [instruction](https://github.com/vctr7/Data_Science/blob/master/apriori_algorithm/apriori.pdf).

    python3 dt.py (train_file.txt) (test_file.txt) (output_file.txt)



(Python3 version : 3.7.3)
 



## 4.	Any other specification of implementation and testing

Numpy should be installed in the executed environment.
