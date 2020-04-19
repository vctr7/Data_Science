import sys
import math
import numpy as np


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


def getColNum(file):
    with open(file, 'r', encoding='utf-8') as t:
        for line in file:
            length = len(line.split())
            break
    return length


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
    unique_elem = set(column)
    a = 0
    b = 0
    for elem in column:
        if elem == list(unique_elem)[0]:
            a += 1
        else:
            b += 1

    return ((a + b) / k) * entropy(a, b)


def getAttrInfo(col, target_list):
    info_sum = 0
    col_len = len(target_list)
    unique_col = list(set(col))

    for elem in unique_col:
        temp = []
        for num, item in enumerate(col):
            if elem == item:
                temp.append(target_list[num])
        info_sum += calculateAttrInfo(temp, col_len)

    return info_sum


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

    # Delete the column of highest gain.
    del(category_result[max_idx])

    return category_result, n_target_list


def leaf(target_list):
    max_num = 0
    ans = 0
    for elem in set(target_list):
        count = target_list.count(elem)
        if max_num < count:
            max_num = count
            ans = elem

    return ans


def DTProcess(attr_list, target_list, height):

    # Set max height as 3 to avoid over-fitting problem
    if height > 3:
        return leaf(target_list)

    height += 1

    # If attribute list is empty, return
    if len(attr_list) < 1:
        return leaf(target_list)

    # If target list is already classified, return
    elif len(set(target_list[1:])) == 1:
        return leaf(target_list)

    # 우선 들어온 데이터에 대해 info 계산해서 best 정해야함.
    info_d = calculateInfoD(target_list[1:])

    # Calculate the Gain on each attribute
    gain_list = []
    for column in attr_list:
        column_info = getAttrInfo(column[1:], target_list[1:])
        gain_list.append(gain(info_d, column_info))

    # split_list = []
    # for column in attr_list:
    #     column_info = get_info(column[1:], target_list[1:])
    #     s_info = split_info(column[1:], target_list[1:])
    #     split_list.append(gain(info_d, column_info)/s_info)

    # Find the highest gain among the attributes.
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

    # Make tree recursively based on the Dictionary structure
    best = attr_list[max_idx][0]
    tree = {best: {}}

    # Find the subtrees of current node.
    for num, elem in enumerate(set(attr_list[max_idx][1:])):
        new_attr_list, new_target = makeSubtree(attr_list, target_list, elem, max_idx)
        subtree = DTProcess(new_attr_list, new_target, height)
        tree[best][elem] = subtree

    return tree


def predict(trx, attr, tree):

    if not isinstance(tree, dict):
        return tree

    for key, subtree in tree.items():
        for n, item in enumerate(attr):
            if key == item:
                return predict(trx, attr, subtree)

            elif key == trx[n]:
                return predict(trx, attr, subtree)

    return tree


def classifier(file, tree):
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    category_result = []

    for i in range(getColNum(file)):
        category = []
        for x in lines:
            category.append(x.split()[i])
        category_result.append(category)

    category_result = np.array(category_result).T

    t_attr = category_result[0]
    t_attr_list = category_result[1:]
    result = []
    for trx in t_attr_list:
        result.append(predict(trx, t_attr, tree))

    return result


def save(train, test, result, output):

    first_line = open(train, 'r', encoding='utf-8').readline()
    output_file = open(output, 'w', encoding='utf-8')
    output_file.writelines(first_line)

    with open(test, 'r', encoding='utf-8') as f:
        for n, line in enumerate(f):
            if n == 0:
                continue

            new_line = line.strip() + '\t' + result[n-1] + '\n'
            output_file.write(new_line)

        f.close()


def main():
    input_train = sys.argv[1]
    input_test = sys.argv[2]
    output_file = sys.argv[3]

    attr_list, target_list = preprocess(input_train, getColNum(input_train))
    result = classifier(input_test, DTProcess(attr_list, target_list, height=0))
    save(input_train, input_test, result, output_file)


if __name__ == "__main__":
    main()
