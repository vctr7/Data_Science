import sys
import math as m
import numpy as np


def getInfo(file):
    idx, x_coor, y_coor = [], [], []
    for line in file:
        elems = line.split()
        idx.append(elems[0])
        x_coor.append(elems[1])
        y_coor.append(elems[2])

    if len(idx) == len(x_coor) == len(y_coor):
        return idx, x_coor, y_coor
    else:
        print("Error input!\n")
        exit()


def getDistance(x1, y1, x2, y2):
    return m.sqrt(m.pow((x2 - x1), 2) + m.pow((y2 - y1), 2))


def main():
    input_file = sys.argv[1]
    number_of_cluster = int(sys.argv[2])
    epsilon = int(sys.argv[3])
    min_points = int(sys.argv[4])

    index, x, y = getInfo(input_file)


if __name__ == "__main__":
    main()