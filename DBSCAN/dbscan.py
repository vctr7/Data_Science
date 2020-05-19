import sys
import math as m
import numpy as np

minpts = 0
epsilon = 0
visited = []


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
    return float(m.sqrt(m.pow((x2 - x1), 2) + m.pow((y2 - y1), 2)))


def getNeighbor(x_list, y_list, elem):
    neighbor_idx = []
    for i in range(len(x_list)):    # range(len(x_list)) == idx
        if x_list[i] == x_list[elem] and y_list[i] == y_list[elem]:
            continue

        if getDistance(x_list[elem], y_list[elem], x_list[i], y_list[i]) <= epsilon:
            neighbor_idx.append(i)

    return neighbor_idx


def isCore(neighbors):
    if neighbors >= minpts:
        return True
    else:
        return False


def getCluster(x_list, y_list, elem, cluster_num):
    n_idx = getNeighbor(x_list, y_list, elem)

    if isCore(len(n_idx)):
        visited[elem] = cluster_num
        for i in n_idx:
            if visited[i] == 0:
                visited[i] = cluster_num
                getCluster(x_list, y_list, i, cluster_num)
    else:
        return


def clustering(idx, x_list, y_list):
    unique_clusters = []
    cluster_num = 1
    for elem in idx:
        if visited[elem] == 0 and isCore(len(getNeighbor(x_list, y_list, elem))):
            unique_clusters.append(cluster_num)
            getCluster(x_list, y_list, elem, cluster_num)
            cluster_num += 1

    clusters = []
    for unique_c in unique_clusters:
        temp = []
        for idx, c_num in enumerate(visited):
            if c_num == unique_c:
                temp.append(idx)
        clusters.append(temp)

    return clusters


def main():
    global epsilon
    global minpts
    global visited

    input_file = sys.argv[1]
    number_of_cluster = int(sys.argv[2])
    epsilon = float(sys.argv[3])
    minpts = int(sys.argv[4])

    index, x, y = getInfo(input_file)
    visited = np.zeros_like(index)
    clustering(index, x, y)


if __name__ == "__main__":
    main()