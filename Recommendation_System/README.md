# Recommendation System

[Instruction](https://github.com/vctr7/Data_Science/blob/master/Recommendation_System/2020_DM_Programming_Assignment_4.pdf)


## 1.	Summary of the algorithm

This is the code of recommender system which is operated based on the similarity method. There are numerous techniques in recommendation process such as Similarity, Matrix decomposition, and Neural network etc. I meaning to use a sophisticated method, but they require many expertise in math and AI area, that I didn’t learn. So, I mainly use a basic technic of cosine similarity.

Since the technic I used is not elaborated, it shows a lower accuracy than expected. So I have to apply heuristic idea such as minimum cosine similarity value and minimum rating.

I have multiple exams in recent days, so I cannot put much effort in this assignment than before. So maybe at this summer vacation, I would enhance the performance of this recommender system with up-to-date ways.



## 2.	Detailed description of codes (for each function) 

This code has several functions including main(). I'll introduce important functions.

    def getInfo(file): Transform a raw input file into 4 tuples
    
    def getSimilarity(user1, user2): Get similarity of two users based on the Cosine Similarity. 
       (We could use Pearson Correlation method instead)
    
    def getNeighbors(): Get the neighbors of given user whom are above the minimum cosine similarity. 
        The minimum similarity value is given as heuristic.(It could be change depending on a situation)
    
    def predicate(test_data, neighbor): Predict the rating of given test file’s information. 
        The prediction is processed based on the neighbors’ rating data. It trims the round value 
        and set minimum rating as 2 to increase the accuracy.

    def compare(train_data, test_data): The main frame of this code. 
    
    def save(filename, result): Save the outcomes of prediction.
    

 
## 3.	Instructions for compiling source codes 

    $ python3 recommender.py <train_file> <test file>

(Python3 version : 3.7.3)
 



## 4.	Any other specification of implementation and testing

None.
