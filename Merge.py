import os
from tqdm import tqdm
import re
import main

dir_list1, dir_list2, dir_list3 = main.dir_list_return()

BASE_PATH = "D:/Semester 8/IR/Assignments/A3/"


def str2list(string):
    li = list(string.split("\n"))
    return li


def str2list1(string):
    li = list(string.split(" "))
    return li


def read(dic_id):
    term_path = BASE_PATH + "index_%s_terms.txt" % str(dic_id)
    posting_path = BASE_PATH + "index_%s_postings.txt" % str(dic_id)
    term_file = open(term_path, "r")
    posting_file = os.open(posting_path, os.O_RDONLY)
    text = term_file.read()
    text = str2list(text)
    index_list = []
    count = 1
    for n in range((len(text) - 2)):
        term_line = str2list1(text[n])
        term_line_next = str2list1(text[n+1])
        term = term_line[0]
        num_byte = int(term_line_next[1]) - int(term_line[1])
        num_byte = num_byte + count
        read_bytes = os.read(posting_file, num_byte)
        posting_line = read_bytes.decode("utf-8")
        posting_list = str2list(posting_line)
        posting = str2list1(posting_list[0])
        index = {
            term: posting
        }
        index_list.append(index)

    term_line = str2list1(text[(len(text) - 2)])
    term = term_line[0]
    read_bytes = os.read(posting_file, 300)
    posting_line = read_bytes.decode("utf-8")
    posting_list = str2list(posting_line)
    posting = str2list1(posting_list[0])
    index = {
        term: posting
    }
    index_list.append(index)
    return index_list


def compare2dic(dic1, dic2):
    for key1, key2 in zip(dic1.keys(), dic2.keys()):
        if key1 == key2:
            return 1
    return -1


def tokenization(text):
    tokens = re.findall("[\w]+", text)
    return tokens


def min_dic3(index1, index2, index3):
    key1 = ""
    key2 = ""
    key3 = ""
    for key in index1.keys():
        key1 = key
    for key in index2.keys():
        key2 = key
    for key in index3.keys():
        key3 = key
    minimum = min(key1, key2, key3)
    if minimum == key1:
        return index1
    elif minimum == key2:
        return index2
    elif minimum == key3:
        return index3


def min_dic2(index1, index2):
    key1 = ""
    key2 = ""
    for key in index1.keys():
        key1 = key
    for key in index2.keys():
        key2 = key
    minimum = min(key1, key2)
    if minimum == key1:
        return index1
    elif minimum == key2:
        return index2


def minimum_index3(index1, index2, index3):
    minimum = min_dic3(index1, index2, index3)
    if compare2dic(minimum, index1) == 1:
        return 1
    elif compare2dic(minimum, index2) == 1:
        return 2
    elif compare2dic(minimum, index3) == 1:
        return 3
    return -1


def minimum_index2(index1, index2):
    minimum = min_dic2(index1, index2)
    if compare2dic(minimum, index1) == 1:
        return 1
    elif compare2dic(minimum, index2) == 1:
        return 2
    return -1


def merge():
    index_1 = read(1)
    index_2 = read(2)
    index_3 = read(3)
    term_path = BASE_PATH + "inverted_index_terms.txt"
    posting_path = BASE_PATH + "inverted_index_postings.txt"
    term_file = open(term_path, "w", errors="ignore")
    posting_file = open(posting_path, "w")
    posting_file.close()
    posting_file = os.open(posting_path, os.O_RDWR)
    count_1 = 0
    count_2 = 0
    count_3 = 0
    final_index = []
    while count_1 < len(index_1) and count_2 < len(index_2) and count_3 < len(index_3):
        if compare2dic(index_1[count_1], index_2[count_2]) == -1 and compare2dic( index_1[count_1], index_3[count_3]) == -1 and compare2dic( index_2[count_2], index_3[count_3]) == -1:
            minimum = min_dic3(index_1[count_1], index_2[count_2], index_3[count_3])
            posting = {}
            for key, value in minimum.items():
                posting = {
                    key: value
                }
                if key in index_1[count_1].keys():
                    count_1 += 1
                elif key in index_2[count_2].keys():
                    count_2 += 1
                elif key in index_3[count_3].keys():
                    count_3 += 1
            final_index.append(posting)

        elif compare2dic(index_1[count_1], index_2[count_2]) == 1 and compare2dic(index_2[count_2], index_3[count_3]) == 1:
            posting = {}
            for key, value in index_1[count_1].items():
                posting = {
                    key: value
                }
            for key, value in index_2[count_2].items():
                posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                value.remove(value[0])
                posting[key].append(value)
            for key, value in index_3[count_3].items():
                posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                value.remove(value[0])
                posting[key].append(value)
            final_index.append(posting)
            count_1 = count_1 + 1
            count_2 = count_2 + 1
            count_3 = count_3 + 1

        elif compare2dic(index_1[count_1], index_2[count_2]) == 1 and compare2dic(index_2[count_2], index_3[count_3]) == -1:
            minimum = minimum_index3(index_1[count_1], index_2[count_2], index_3[count_3])
            if minimum == 1:
                posting = {}
                for key, value in index_1[count_1].items():
                    posting = {
                        key: value
                    }
                for key, value in index_2[count_2].items():
                    posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                    value.remove(value[0])
                    posting[key].append(value)
                final_index.append(posting)
                count_1 += 1
                count_2 += 2
            elif minimum == 3:
                posting = {}
                for key, value in index_1[count_1].items():
                    posting = {
                        key: value
                    }
                final_index.append(posting)
                count_3 += 1

        elif compare2dic(index_1[count_1], index_2[count_2]) == -1 and compare2dic(index_2[count_2], index_3[count_3]) == 1:
            posting = {}
            minimum = minimum_index3(index_1[count_1], index_2[count_2], index_3[count_3])
            if minimum == 1:
                for key, value in index_1[count_1].items():
                    posting = {
                        key: value
                    }
                final_index.append(posting)
                count_1 += 1
            elif minimum == 2:
                for key, value in index_2[count_2].items():
                    posting = {
                        key: value
                    }
                for key, value in index_3[count_3].items():
                    posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                    value.remove(value[0])
                    posting[key].append(value)
                final_index.append(posting)
                count_2 += 1
                count_3 += 1

        elif compare2dic(index_1[count_1], index_2[count_2]) == -1 and compare2dic(index_1[count_1], index_3[count_3]) == 1:
            posting = {}
            minimum = minimum_index3(index_1[count_1], index_2[count_2], index_3[count_3])
            if minimum == 1:
                for key, value in index_1[count_1].items():
                    posting = {
                        key: value
                    }
                for key, value in index_3[count_3].items():
                    posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                    value.remove(value[0])
                    posting[key].append(value)
                final_index.append(posting)
                count_1 += 1
                count_3 += 1
            elif minimum == 2:
                for key, value in index_2[count_2].items():
                    posting = {
                        key: value
                    }
                final_index.append(posting)
                count_2 += 1

    if len(index_1) < len(index_2) and len(index_1) < len(index_3):
        while count_2 < len(index_2) and count_3 < len(index_3):
            if compare2dic(index_2[count_2], index_3[count_3]) == 1:
                posting = {}
                for key, value in index_2[count_2].items():
                    posting = {
                        key: value
                    }
                for key, value in index_3[count_3].items():
                    posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                    value.remove(value[0])
                    posting[key].append(value)
                final_index.append(posting)
                count_2 += 1
                count_3 += 1
            elif compare2dic(index_2[count_2], index_3[count_3]) == -1:
                minimum = minimum_index2(index_2[count_2], index_3[count_3])
                if minimum == 1:
                    final_index.append(index_2[count_2])
                    count_2 += 1
                elif minimum == 2:
                    final_index.append(index_3[count_3])
                    count_3 += 1
        if len(index_2) < len(index_3):
            while count_3 < len(index_3):
                final_index.append(index_3[count_3])
                count_3 += 1
        elif len(index_3) < len(index_2):
            while count_2 < len(index_2):
                final_index.append(index_2[count_2])
                count_2 += 1

    elif len(index_2) < len(index_1) and len(index_2) < len(index_3):
        while count_1 < len(index_1) and count_3 < len(index_3):
            if compare2dic(index_1[count_1], index_3[count_3]) == 1:
                posting = {}
                for key, value in index_1[count_1].items():
                    posting = {
                        key: value
                    }
                for key, value in index_3[count_3].items():
                    posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                    value.remove(value[0])
                    posting[key].append(value)
                final_index.append(posting)
                count_1 += 1
                count_3 += 1
            elif compare2dic(index_1[count_1], index_1[count_1]) == -1:
                minimum = minimum_index2(index_1[count_1], index_3[count_3])
                if minimum == 1:
                    final_index.append(index_1[count_1])
                    count_1 += 1
                elif minimum == 2:
                    final_index.append(index_3[count_3])
                    count_3 += 1
        if len(index_1) < len(index_3):
            while count_3 < len(index_3):
                final_index.append(index_3[count_3])
                count_3 += 1
        elif len(index_3) < len(index_1):
            while count_1 < len(index_1):
                final_index.append(index_1[count_1])
                count_1 += 1

    elif len(index_3) < len(index_2) and len(index_1) > len(index_3):
        while count_1 < len(index_1) and count_2 < len(index_2):
            if compare2dic(index_1[count_1], index_2[count_2]) == 1:
                posting = {}
                for key, value in index_1[count_1].items():
                    posting = {
                        key: value
                    }
                for key, value in index_2[count_2].items():
                    posting[key][0] = str(int(posting[key][0]) + int(value[0]))
                    value.remove(value[0])
                    posting[key].append(value)
                final_index.append(posting)
                count_1 += 1
                count_2 += 1
            elif compare2dic(index_1[count_1], index_2[count_2]) == -1:
                minimum = minimum_index2(index_1[count_1], index_2[count_2])
                if minimum == 1:
                    final_index.append(index_1[count_1])
                    count_1 += 1
                elif minimum == 2:
                    final_index.append(index_2[count_2])
                    count_1 += 1
        if len(index_1) < len(index_2):
            while count_2 < len(index_2):
                final_index.append(index_2[count_2])
                count_2 += 1
        elif len(index_2) < len(index_1):
            while count_1 < len(index_1):
                final_index.append(index_1[count_1])
                count_1 += 1
    start_bytes = 0
    for dic in tqdm(range(0, len(final_index))):
        for key, value in final_index[dic].items():
            string_for_term_file = key + " " + str(start_bytes) + "\n"
            term_file.write(string_for_term_file)
            check_list = [1]
            check_str = "a"
            list1 = value.pop()
            if type(list1) == type(check_str):
                value.append(list1)
            elif type(list1) == type(check_list):
                list2 = value.pop()
                if type(list2) == type(check_str):
                    value.append(list2)
                    for string in list1:
                        value.append(string)
                elif type(list2) == type(check_list):
                    for string in list2:
                        value.append(string)
                    for string in list1:
                        value.append(string)

            list2str = ' '.join(map(str, value))
            list2str = list2str + "\n"

            line = str.encode(list2str)
            num_bytes = os.write(posting_file, line)
            start_bytes = start_bytes + num_bytes
    final_index_dic = {}
    for dic in final_index:
        for key, value in dic.items():
            final_index_dic[key] = value
    return final_index_dic


def find_result_of_query(index, query):
    tokens = tokenization(query)
    final_result = []
    for token in tokens:
        if token not in index.keys():
            return -1
        else:
            posting_list = index[token]
            result_list_n = []
            jump = 1
            value_to_add = 0
            flag1 = 0
            flag2 = 0
            for n in range(int(posting_list[0])):
                doc_id = int(posting_list[jump]) + value_to_add
                value_to_add = doc_id
                if doc_id > 1160 and doc_id < 2266 and flag1 == 0:
                    value_to_add = int(posting_list[jump])
                    doc_id = int(posting_list[jump])
                    flag1 = 1
                elif doc_id > 2265 and flag2 == 0:
                    value_to_add = int(posting_list[jump])
                    doc_id = int(posting_list[jump])
                    flag2 = 1
                temp_list = [doc_id]
                jump += 1
                counter = int(posting_list[jump])
                temp_list.append(counter)
                result_list_n.append(temp_list)
                jump += counter
                jump += 1

            final_result.append(result_list_n)
    return final_result


def Sort(sub_li):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    return (sorted(sub_li, key=lambda x: x[1], reverse=True))


def column(matrix, i):
    return [row[i] for row in matrix]


def print_result(result_list):
    if len(result_list) > 1:
        res = []
        for i in range(len(result_list) - 1):
            temp_list = result_list[i]
            for j in range(len(temp_list)):
                temp_list2 = column(result_list[i+1], 0)
                value = result_list[i][j][0]
                if value in temp_list2:
                    res.append(result_list[i][j])
        if len(res) == 0:
            print("No Results Found")
            return 0
        res = Sort(res)
        for i in range(len(res)):
            if int(res[i][0]) < len(dir_list1):
                print("Sub_directory is 1 and filename is " + dir_list1[int(res[i][0]) - len(dir_list1)])
            elif int(res[i][0]) > len(dir_list1) - 1 and int(res[i][0]) < len(dir_list1) + len(dir_list2):
                print("Sub_directory is 2 and filename is " + dir_list2[int(res[i][0]) - len(dir_list1)])
            elif int(res[i][0]) > len(dir_list1) + len(dir_list2) - 1:
                print("Sub_directory is 3 and filename is " + dir_list3[int(res[i][0]) - len(dir_list1)])
        print(res)
    else:
        result_list[0] = Sort(result_list[0])
        for i in range(len(result_list[0])):
            if int(result_list[0][i][0]) < len(dir_list1):
                print("Sub_directory is 1 and filename is " + dir_list1[int(result_list[0][i][0]) - len(dir_list1)])
            elif int(result_list[0][i][0]) > len(dir_list1) - 1 and int(result_list[0][i][0]) < len(dir_list1) + len(dir_list2):
                print("Sub_directory is 2 and filename is " + dir_list2[int(result_list[0][i][0]) - len(dir_list1)])
            elif int(result_list[0][i][0]) > len(dir_list1) + len(dir_list2) - 1:
                print("Sub_directory is 3 and filename is " + dir_list3[int(result_list[0][i][0]) - len(dir_list1)])
        print(result_list[0])


index = merge()
query = input("Enter the query:     ")
result = find_result_of_query(index, query)
num = 1
if type(result) == type(num):
    print("No result found")
else:
    print_result(result)

