# DBSCAN(Density-based spatial clustering of applications with noise)

[Project Instruction](https://github.com/vctr7/Data_Science/blob/master/DBSCAN/2020_DM_Programming_Assignment_3.pdf)

## 1.	Summary of the algorithm

This code denotes the algorithm of DBSCAN. It is written in Python and composed with several functions. 

DBSCAN groups the points using the several parameters such as epsilon and minpts. Based on these values, this algorithm defines several ideas such as core point, neighbor, etc; and implements the procedure using these criteria.

I used very basic libraries; sys for change the maximum time of recursion, argparse for I/O, math for calculating the distance between two points, numpy for making zero array, matplotlib for visualizing the result.

I meaning to perfectly reproduce the results of the instruction but eventually couldn’t. Maybe there is subtle differences between my code and TA’s.


## 2.	Detailed description of codes (for each function) 

This code has several functions including main(). I'll introduce important functions.

    def getInfo(file): Get information of file and return the index, x coordinate, y coordinate of input file respectively.
    
    def getDistance(): Get distance between the two points.
    
    def getNeighbor(): Get neighbor point’s index.
    
    def isCore(): Check the criterion point is a core point or not.

    def isBorder(): Check the criterion point is a border point or not.
    
    def clustering(): Recursively find and include the points into specific cluster.
    
    def def getClusters(): Group the points into several clusters according to the given number of clusters.
    
    def save(): Save the result into files.




 
## 3.	Instructions for compiling source codes 

Since I use Python, it has subtle differnece with [instruction](https://github.com/vctr7/Data_Science/blob/master/DBSCAN/2020_DM_Programming_Assignment_3.pdf).

    python3 clustering.py <input.txt> <number of clusters> <epsilon> <minpts>

(Python3 version : 3.7.3)
 



## 4.	Any other specification of implementation and testing

Numpy, matplotlib should be installed in the executed environment.

