import numpy as np
import argparse
import time
import math
from numpy.linalg import svd


def getInfo(filename):

    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split()
            data.append([int(line[0]), int(line[1]), int(line[2]), int(line[3])])

    return data


def getSimilarity(user1, user2):
    v = [(rating1, user2.get(item_id, 0)) for item_id, rating1 in user1.items()]

    if len(v) == 0:
        return 0
    elif sum([w1 * w2 for w1, w2 in v]) == 0:
        return 0
    else:
        return (sum([w1 * w2 for w1, w2 in v]) / math.sqrt(sum([w1 ** 2 for w1, w2 in v]))
                / math.sqrt(sum([w2 ** 2 for w1, w2 in v])))


def getNeighbors(user, users):
    # This part takes the most time of the procedure.
    min_val = 0.35

    neighbor_list = []
    for neighbor in users:
        if user == neighbor:
            continue

        # Set min_val in heuristic way
        if getSimilarity(user, neighbor) >= min_val:
            neighbor_list.append(neighbor)

    return neighbor_list


def predicate(test_data, neighbor):
    outcome = []
    for user_id, item_id, real_rating, _ in test_data:
        # Predicate rating by calculating average of neighbors
        v = [u[item_id] for u in neighbor[user_id] if item_id in u]

        # Set minimum rating as 2 to increase the accuracy.
        if len(v) == 0:
            rating = 2
        else:
            rating = round(sum(v) / len(v))

        outcome.append([user_id, item_id, rating])

    return outcome


def compare(train_data, test_data):

    # Make user - item matrix
    # print("Make user-item table")
    data = {}
    for user_id, item_id, rating, timestamp in train_data:
        if user_id not in data:
            data[user_id] = {}
        data[user_id][item_id] = rating
    # print("Make user-item table Finish")

    # print("Make user and neighbors table")
    neighbors = {}
    for user_id, user in data.items():
        neighbors[user_id] = getNeighbors(user=user, users=data.values())
    # print("Make user and neighbors table finish")

    # print("Predict the test file's rates")
    output = predicate(test_data, neighbors)
    # print("Predicting finish")

    return output


def save(filename, result):
    title = filename + '_prediction.txt'
    with open(title, 'w', encoding='utf-8') as f:
        for line in result:
            f.write(str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) + '\n')


def main():

    parser = argparse.ArgumentParser(description='Main parameters for recommendation system')
    parser.add_argument('train_file', help="input train file name")
    parser.add_argument('test_file', help="input test file name")
    args = parser.parse_args()

    print("NOTICE : It takes a while to generate the result due to numerous computation")
    output = compare(getInfo(args.train_file), getInfo(args.test_file))
    save(args.train_file, output)
    print("Done.")


if __name__ == "__main__":
    main()
