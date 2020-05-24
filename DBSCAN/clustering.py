import sys
import math as m
import numpy as np
import matplotlib.pyplot as plt

minpts = 0
epsilon = 0
number_of_cluster = 0
visited = []


def getInfo(file):
    file = open(file, 'r', encoding='utf-8')

    idx, x_coor, y_coor = [], [], []
    for line in file:
        elems = line.split()
        idx.append(int(elems[0]))
        x_coor.append(float(elems[1]))
        y_coor.append(float(elems[2]))

    # Increase the maximum number of recursive try in python. (default = 1e3)
    sys.setrecursionlimit(len(idx))

    if len(idx) == len(x_coor) == len(y_coor):
        return idx, x_coor, y_coor
    else:
        print("Something wrong with a input file.\n")
        exit()


def getDistance(x1, y1, x2, y2):
    return float(m.sqrt(m.pow((x2 - x1), 2) + m.pow((y2 - y1), 2)))


def getNeighbor(x_list, y_list, elem):
    neighbor_idx = []
    for i in range(len(x_list)):    # range(len(x_list)) == idx

        if x_list[i] == x_list[elem] and y_list[i] == y_list[elem]:
            neighbor_idx.append(i)
            continue

        if getDistance(x_list[elem], y_list[elem], x_list[i], y_list[i]) <= epsilon:
            neighbor_idx.append(i)

    return neighbor_idx


def isCore(number_of_neighbors):
    if number_of_neighbors >= minpts:
        return True
    else:
        return False


def isBorder(number_of_neighbors):
    if minpts > number_of_neighbors > 1:
        return True
    else:
        return False


def isOutlier(number_of_neighbors):
    if number_of_neighbors == 1:
        return True
    else:
        return False


def clustering(x_list, y_list, elem, cluster_num):
    neighbors_of_elem = getNeighbor(x_list, y_list, elem)

    # elem'th index should be Core.
    if isCore(len(neighbors_of_elem)):
        visited[elem] = cluster_num
        for neighbor in neighbors_of_elem:
            if visited[neighbor] == 0:
                visited[neighbor] = cluster_num
                # Find recursively
                clustering(x_list, y_list, neighbor, cluster_num)

    elif isBorder(len(neighbors_of_elem)):
        visited[elem] = cluster_num
        return


def getClusters(idx, x_list, y_list):
    unique_clusters = []
    cluster_num = 1
    temp = 0
    for elem in idx:
        if visited[elem] == 0 and isCore(len(getNeighbor(x_list, y_list, elem))):
            unique_clusters.append(cluster_num)
            clustering(x_list, y_list, elem, cluster_num)
            temp += len(visited[visited == cluster_num])
            print("clustering :", str(cluster_num) + ', process(%) :', '%.1f' % (temp * 100 / len(idx)) + '%')
            cluster_num += 1

    print("Finish clustering")
    clusters_set = []
    for cluster in unique_clusters:
        temp = []
        for n, c_num in enumerate(visited):
            if c_num == cluster:
                temp.append(n)
        clusters_set.append([len(temp), cluster, temp])

    clusters = sorted(clusters_set, key=lambda x: x[0], reverse=True)

    print("Delete", len(clusters_set)-number_of_cluster, "clusters")
    return clusters[:number_of_cluster]


def plot(x, y, clusters):
    for category in clusters:
        xelem, yelem = [], []
        for elem in category[2]:
            xelem.append(x[elem])
            yelem.append(y[elem])
        plt.scatter(xelem, yelem, s=1.5, label=category[1])
    plt.legend()
    plt.show()


def save(file, clusters):
    for num, cluster in enumerate(clusters):
        filename = file + '_cluster_' + str(num) + '.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            for line in cluster[2]:
                f.write(str(line))
                f.write('\n')


def main():
    global epsilon, minpts, visited, number_of_cluster

    input_file = sys.argv[1]
    number_of_cluster = int(sys.argv[2])
    epsilon = float(sys.argv[3])
    minpts = int(sys.argv[4])

    index, x, y = getInfo(input_file)
    visited = np.zeros_like(index)
    clusters = getClusters(index, x, y)

    save(input_file, clusters)
    print("Done")
    plot(x, y, clusters)


if __name__ == "__main__":
    main()
