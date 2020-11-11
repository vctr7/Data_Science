import sys

cnt = 0
cnt2 = 0


# Generate subsets of given set.
def generate_subset(given_set):
    p = [[]]
    for elem in given_set:
        for sub_set in p:
            p = p + [list(sub_set) + [elem]]

    # Excludes empty set
    return p[1:]


# Pre-processes input file.
def pre_process(input_file):
    c, d = [], []
    with open(input_file, 'r', encoding='utf-8') as f1:
        for line in f1:
            elements = line.split()
            integer = []
            for i in elements:
                integer.append(int(i))
            d.append(integer)
            for item in elements:
                if not [item] in c:
                    c.append(int(item))

    c = list(set(c))
    c.sort()

    return c, d


# Calculates support rate of item sets and ditch the items lesser than minimum support rate.
def scan(trx_data, item_id, min_support):
    item_len = len(item_id)
    trx_len = len(trx_data)
    global cnt

    # 요소 n 은 몇개의 그룹에 포함되어 있는지 계산
    count = [0]*item_len

    # Count the number of a item_set containing single item_id
    if not cnt:
        for num, item in enumerate(item_id):
            for row in trx_data:
                if {item}.issubset(set(row)):
                    count[num] += 1
                    cnt += 1

    # Count the number of a item set containing multiple item_ids
    else:
        for num, item in enumerate(item_id):
            for row in trx_data:
                if set(item).issubset(set(row)):
                    count[num] += 1

    # Calculate support rate
    new_count = [count[n] / trx_len for n in range(item_len)]

    # Zip item and support rate
    support_of_c = list(zip(item_id, new_count))

    update_list, update_support = [], []
    for i in support_of_c:
        if i[1] >= min_support:
            update_list.append(i[0])
            update_support.append((i[1] * 100))

    return update_list, update_support


# Generate apriori candidates.
def generate_apriori(lk, k):
    global cnt2
    retList = []
    lk_len = len(lk)

    if not cnt2:
        for i in range(lk_len):
            for j in range(i + 1, lk_len):
                new_set = set(lk[i: i + 1]) | set(lk[j: j + 1])

                if len(new_set) != k:
                    continue
                if list(new_set) in retList:  # 이미 있을 경우
                    continue
                retList.append(list(new_set))
        cnt2 += 1
    else:
        for i in range(lk_len):
            for j in range(i + 1, lk_len):
                new_set = set(lk[i]) | set(lk[j])

                if len(new_set) != k:
                    continue
                if list(new_set) in retList:  # 이미 있을 경우
                    continue
                retList.append(list(new_set))

    return retList


# Apriori algorithm.
def apriori(item_id, trx_data, min_support):
    sup = []
    L1, support_data = scan(trx_data, item_id, min_support)
    sup.append(support_data)
    l = [L1]
    k = 2
    while (len(l[k - 2]) > 0):
        ck = generate_apriori(l[k - 2], k)
        lk, supK = scan(trx_data, ck, min_support)
        sup.append(supK)
        l.append(lk)
        k += 1
    return l, sup


# Returns support rate of given item id.
def search_support(given_id, final):
    for item, support_rate in final:
        if given_id == set(item):
            return support_rate


# Zip item set and support rate.
def zip_item_and_support(item_set, support_data):
    item, support = [], []

    for i, j in enumerate(item_set):
        if i == 0:
            for k in j:
                item.append([k])
        else:
            for element in j:
                item.append(element)

    for i in support_data:
        for element in i:
            support.append(element)

    return list(zip(item, support))


# Saves file.
def save_file(output_file, final):
    f = open(output_file, 'w', encoding='utf-8')

    for num, content in enumerate(final):
        pair = content[0]
        supp = content[1]
        p_set = generate_subset(pair)

        if len(p_set[-1:][0]) == 1:
            line = "{}" + "\t" + "{" + str(pair[0]) + "}" + "\t" + str(round(supp, 2)) + "\t" + str(
                round(supp, 2)) + "\n"
            f.write(line)

        else:
            for subset in p_set:
                if len(subset) == len(p_set[-1:][0]):
                    continue
                rest = list(set(p_set[-1:][0]) - set(subset))
                conf = supp * 100 / (search_support(set(subset), final))
                line = str(set(subset)) + "\t" + str(set(rest)) + "\t" + str(round(supp, 2)) + "\t" + str(
                    round(conf, 2)) + "\n"
                f.write(line)


def main():
    min_support_rate = int(sys.argv[1]) / 100
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    # item_id : 무슨 item이 있는지 들어있는 리스트
    # trx_data : 트랜잭션의 데이터가 들어있는 리스트
    item_id, trx_data = pre_process(input_file_name)

    # item_set : minimum support rate 보다 support rate가 큰 item_id의 부분집합
    # support_data : 각각의 item set에 대한 support rate
    item_set, support_data = apriori(item_id, trx_data, min_support_rate)
    final = zip_item_and_support(item_set, support_data)

    save_file(output_file_name, final)


if __name__ == "__main__":
    main()
