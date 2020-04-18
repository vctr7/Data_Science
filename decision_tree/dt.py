import sys
import math
import numpy as np

test = {}

def split_info(column, target_list):
    summation = 0
    column_len = len(target_list)
    reduced_column = list(set(column))

    for elem in reduced_column:
        temp = []
        for num, item in enumerate(column):
            if elem == item:
                temp.append(target_list[num])
        summation += calculateAttrInfo(temp, column_len)

    return summation


def getColNum(input_n):
    with open(input_n, 'r', encoding='utf-8') as t:
        for line in t:
            k = len(line.split())
            break
    return k


def preprocess(file, k):
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    category_result = []

    for i in range(k):
        category = []
        for num, x in enumerate(lines):

            category.append(x.split()[i])
        category_result.append(category)

    return category_result[:-1], category_result[-1]


def calculateInfoD(column):
    set_ = set(column)
    a = 0
    b = 0
    for elem in column:
        if elem == list(set_)[0]:
            a += 1
        else:
            b += 1

    x = max(a, 1e-10)
    y = max(b, 1e-10)
    s = x + y
    return -((x / s) * math.log2(x / s)) - ((y / s) * math.log2(y / s))


def entropy(a, b):
    x = max(a, 1e-10)
    y = max(b, 1e-10)
    s = x + y
    return -((x / s) * math.log2(x / s)) - ((y / s) * math.log2(y / s))


def calculateAttrInfo(column, k):
    set_ = set(column)
    a = 0
    b = 0
    for elem in column:
        if elem == list(set_)[0]:
            a += 1
        else:
            b += 1

    return ((a + b) / k) * entropy(a, b)


def getAttrInfo(column, target_list):
    summation = 0
    column_len = len(target_list)
    reduced_column = list(set(column))

    for elem in reduced_column:
        temp = []
        for num, item in enumerate(column):
            if elem == item:
                temp.append(target_list[num])
        summation += calculateAttrInfo(temp, column_len)

    return summation


def gain(info_x, info_y):
    return info_x - info_y


def makeSubtree(attr_list, target_list, elem, max_idx):
    n_target_list, n_attr_list, category_result = [], [], []
    n_target_list.append(target_list[0])

    for n, item in enumerate(attr_list[max_idx]):
        temp = []
        if elem == item:
            for column in attr_list:
                temp.append(column[n])

            n_target_list.append(target_list[n])

        if temp:
            n_attr_list.append(temp)

    for item in range(len(n_attr_list[0])):
        category = []
        for num, x in enumerate(n_attr_list):
            category.append(x[item])

        category_result.append(category)

    for n, item in enumerate(category_result):
        item.insert(0, attr_list[n][0])

    del(category_result[max_idx])

    return category_result, n_target_list


def DTProcess(attr_list, target_list, ntree, height):

    # max height. avoid over-fitting
    if height > 3:
        return set(target_list)

    # print the height of node and its content
    if height >= 0:
        # print(height, target_list[1:])
        height += 1

    # attr_list 비어있을 경우 return
    if len(attr_list) < 1:
        max_num = 0
        ans = 0
        for i in set(target_list):
            count = target_list.count(i)
            if max_num < count:
                max_num = count
                ans = i

        return ans

    # 완벽히 분류되었을 시 return
    elif len(set(target_list[1:])) == 1:
        max_num = 0
        ans = 0
        for i in set(target_list):
            count = target_list.count(i)
            if max_num < count:
                max_num = count
                ans = i

        return ans

    # 우선 들어온 데이터에 대해 info 계산해서 best 정해야함.
    info_d = calculateInfoD(target_list[1:])

    # attr 별로 gain 계산해야 함..
    gain_list = []
    for column in attr_list:
        column_info = getAttrInfo(column[1:], target_list[1:])
        gain_list.append(gain(info_d, column_info))

    # split_list = []
    # for column in attr_list:
    #     column_info = get_info(column[1:], target_list[1:])
    #     s_info = split_info(column[1:], target_list[1:])
    #     split_list.append(gain(info_d, column_info)/s_info)

    # attr_list 중, max gain 을 가진 attr 구한다
    max_gain = 0
    max_idx = 0
    for num, i in enumerate(gain_list):
        if max_gain < i:
            max_gain = i
            max_idx = num

    # attr_list 중, max split info 을 가진 attr 구한다
    # for num, i in enumerate(split_list):
    #     if max_gain < i:
    #         max_gain = i
    #         max_idx = num

    # parent node 기준에 맞는 자식 nodes 생성
    best = attr_list[max_idx][0]
    tree = {best: {}}

    for num, elem in enumerate(set(attr_list[max_idx][1:])):
        new_attr_list, new_target = makeSubtree(attr_list, target_list, elem, max_idx)
        ntree.append(attr_list[max_idx][0])
        subtree = DTProcess(new_attr_list, new_target, ntree, height)
        tree[best][elem] = subtree

    return tree




def classifier(file, tree):
    col = getColNum(file)
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    category_result = []

    for i in range(col):
        category = []
        for num, x in enumerate(lines):
            category.append(x.split()[i])
        category_result.append(category)

    category_result = np.array(category_result).T
    print(tree)
    t_attr = category_result[0]
    t_attr_list = category_result[1:]

    for n, line in enumerate(t_attr_list):
        trx = []
        for num, item in enumerate(line):
            trx.append([t_attr[num], item])
        print(n+1, trx)


def main():
    input_train = sys.argv[1]
    input_test = sys.argv[2]
    output_file = sys.argv[3]
    tree_info = []
    col = getColNum(input_train)
    attr_list, target_list = preprocess(input_train, col)
    tree = DTProcess(attr_list, target_list, tree_info, height=0)
    classifier(input_test, tree)


if __name__ == "__main__":
    main()
