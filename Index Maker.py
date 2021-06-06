# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from bs4 import BeautifulSoup
import re
import StopWords
from nltk.stem import PorterStemmer
from tqdm import tqdm

PARENT_DIR = "D:/Semester 8/IR/Assignments/A3/corpus/corpus1/"
FILE_PATH = "D:/Semester 8/IR/Assignments/A3/"
STOP_WORDS = StopWords.STOP_WORDS


def list_all_files(path):
    dir_list = os.listdir(path)
    return dir_list


def html_page_parser(page_name, dir_id):
    path = str(dir_id) + "/" + page_name
    file_path = os.path.join(PARENT_DIR,path )
    file_object = open(file_path, errors="ignore")
    file_content = file_object.read()
    soup = BeautifulSoup(file_content, "html.parser")
    if soup.find("html") is not None:
        text = soup.find("html").text
        text = text.lower().replace("\n", " ").replace("\t", " ").strip()
        file_object.close()
        return text
    return None


def tokenization(text):
    tokens = re.findall("[\w]+", text)
    return tokens


def difference_of_two_list(li1, li2):
    li_dif = [i for i in li1 if i not in li2]
    return li_dif


def stemming(words_lst, doc_id):
    porter = PorterStemmer()
    temp_list = []
    for word in words_lst:
        temp_list.append(porter.stem(word))
    # temp_list = sorted(temp_list)
    return_list = []
    for word in temp_list:
        dic = {
            word: doc_id
        }
        return_list.append(dic)
    return return_list


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# function to return key for any value
def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key

    return "key doesn't exist"


def create_index(index, token_list):
    for n, id_ in tqdm(enumerate(token_list), total=len(token_list)):
        key = get_key(token_list[n], list(token_list[n].values())[0])
        posting = index.get(key, None)

        doc = token_list[n][key]
        if posting is None:

            posting = {
                doc: 1,
                "position" + str(doc): [n],
            }
            posting["position" + str(doc)].append(n)
        else:
            if token_list[n][key] not in posting:
                posting[doc] = 1
                posting["position" + str(doc)] = [n]
                posting["position" + str(doc)].append(n)
            else:
                posting[doc] = posting[doc] + 1
                # all_index = [all_index for all_index, value in enumerate(token_list) if value == token]
                num = posting["position" + str(doc)].pop()
                posting["position" + str(doc)].append(n - num)
                posting["position" + str(doc)].append(n)

        index[key] = posting


def write2file(index, dir_id):
    index2write = dict(sorted(index.items()))
    term_path = FILE_PATH + "index_%s_terms.txt" % str(dir_id)
    posting_path = FILE_PATH + "index_%s_postings.txt" % str(dir_id)
    term_file = open(term_path, "w", errors="ignore")
    posting_file = open(posting_path, "w")
    posting_file.close()
    posting_file = os.open(posting_path, os.O_RDWR)
    start_bytes = 0
    for key in index2write.keys():
        term_list = []
        dt = len(index2write[key]) / 2
        term_list.append(int(dt))
        count = 0
        for key2 in index2write[key]:
            if isinstance(key2, int):
                term_list.append((key2 - count))
                term_list.append(index2write[key][key2])
                count = key2
            else:
                index2write[key][key2].pop()
                for pos in index2write[key][key2]:
                    term_list.append(pos)

        string_for_term_file = key + " " + str(start_bytes) + "\n"
        term_file.write(string_for_term_file)
        list2str = ' '.join(map(str, term_list))
        list2str = list2str + "\n"
        line = str.encode(list2str)
        num_bytes = os.write(posting_file, line)
        start_bytes = start_bytes + num_bytes

    os.close(posting_file)
    term_file.close()


def str2list(string):
    li = list(string.split("\n"))
    return li


def rename(dir_list, path, starting_index):

    for count, file_name in enumerate(dir_list):
        dst = str(count + starting_index)
        src = path + "/" + file_name
        dst = path + "/" + dst
        os.rename(src, dst)
    dir_list = os.listdir(path)
    return dir_list


def dir_list_return():
    dic_path1 = PARENT_DIR + str(1)
    dr_list1 = list_all_files(dic_path1)
    dic_path2 = PARENT_DIR + str(2)
    dr_list2 = list_all_files(dic_path2)
    dic_path3 = PARENT_DIR + str(3)
    dr_list3 = list_all_files(dic_path3)
    return  dr_list1, dr_list2, dr_list3

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    dic_id = input("Enter the directory for which you want to make indexes: ")
    dic_path1 = PARENT_DIR + str(1)
    dr_list1 = list_all_files(dic_path1)
    dic_path2 = PARENT_DIR + str(2)
    dr_list2 = list_all_files(dic_path2)
    dic_path3 = PARENT_DIR + str(3)
    dr_list3 = list_all_files(dic_path3)
    starting_index = 0
    if int(dic_id) == 1:
        starting_index = 0
    elif int(dic_id) == 2:
        starting_index = len(dr_list1)
    elif int(dic_id) == 3:
        starting_index = len(dr_list1) + len(dr_list2)
    dic_path = PARENT_DIR + str(dic_id)
    dr_list = list_all_files(dic_path)
    # dr_list = rename(dr_list, dic_path, starting_index)
    doc_info_path = FILE_PATH + "docInfo.txt"
    doc_info_file = open(doc_info_path, "a")
    index = {}
    for i in tqdm(range(0, 10)):

        text = html_page_parser(dr_list[i], dic_id)
        if text is not None:
            token_list = tokenization(text)
            token_list = difference_of_two_list(token_list, STOP_WORDS)
            token_list = stemming(token_list, (i+starting_index))
            if starting_index == 0:
                line = str(i + starting_index) + " " + "1/" + dr_list[i] + " " + str(len(token_list)) + " " + str(len(token_list)) + "\n"
                doc_info_file.write(line)
            elif starting_index == len(dr_list1):
                line = str(i + starting_index) + " " + "2/" + dr_list[i] + " " + str(len(token_list)) + " " + str(
                    len(token_list)) + "\n"
                doc_info_file.write(line)
            elif starting_index == len(dr_list1) + len(dr_list2):
                line = str(i + starting_index) + " " + "3/" + dr_list[i] + " " + str(len(token_list)) + " " + str(
                    len(token_list)) + "\n"
                doc_info_file.write(line)
            create_index(index, token_list)
    doc_info_file.close()
    write2file(index, dic_id)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
