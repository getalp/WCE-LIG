# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:45:57 2015
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

#**************************************************************************#
import os
import sys
import re
#import linecache
#import stat
import datetime
import itertools
import nltk
import math

#for call shell script
#import shlex, subprocess

#**************************************************************************#
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from config.configuration import *
#from config.config_end_user import *
from common_module.cm_config import load_configuration, load_config_end_user
#**************************************************************************#
def u(s, encoding = 'utf-8', errors='strict'):
    #ensure s is properly unicode.. wrapper for python 2.6/2.7,
    if version < '3':
        #ensure the object is unicode
        if isinstance(s, unicode):
            return s
        else:
            return unicode(s, encoding,errors=errors)
    else:
        #will work on byte arrays
        if isinstance(s, str):
            return s
        else:
            return str(s,encoding,errors=errors)
        #end if
    #end if
#**************************************************************************#
def xrange(x):
    return iter(range(x))
#**************************************************************************#
def is_in_list(word, my_list):
    """
    Checking word that exists in list from the file or not

    :type word: string
    :param word: input word

    :type my_list: list
    :param my_list: list from the file

    :rtype: True if existed in List; otherwise False
    """
    if word in my_list:
        return True
    else:
        return False
    #end if
#**************************************************************************#
def is_in_string(word, my_string):
    """
    Checking word that exists in string given or not

    :type word: string
    :param word: input word

    :type my_string: string
    :param my_string: string given

    :rtype: True if existed in List; otherwise False
    """
    if word in my_string:
        return True
    else:
        return False
    #end if
#**************************************************************************#
#ref: http://www.regextester.com/
# >	,
def is_match(regex, text):
    """
    Checking the text is match in regex

    :type regex: string
    :param regex: Regular Expression.

    :type text: string
    :param text: Text.

    :rtype: True if matched; False otherwise
    """
    if re.match(regex, text) == None:
        return False
    else:
        return True
#**************************************************************************#
def is_numeric(text):
    """
    Checking the text is a numeric or not

    :type text: string
    :param text: Text.

    :rtype: True if text is a numeric; False otherwise
    """

    #regex = "^\d*[.,]?\d*$" #sai vi nhan dau . hay , la so ??!!
    regex = "[-+]?[0-9]*[.,]?[0-9]+$"

    return is_match(regex, text)
#**************************************************************************#
def check_value_boolean(str_boolean):
    """
    Convert string str_boolean to boolean

    :type str_boolean: int
    :param str_boolean: string of boolean

    :rtype: True/False
    """
    str_lowercase = str(str_boolean).lower()

    if str_lowercase == "true":
        return True
    elif str_lowercase == "false":
        return False
    else:
        return None
#**************************************************************************#
def split_string_to_list_delimeter_tab(text):
    """
    Splitting the text into a list of elements.

    :type text: string
    :param text: Text

    :rtype: list of element
    """
    #my_list = [] # make empty list
    #words = text.split() #for space
    #for current_word in words:
    #    my_list.append(current_word.lower())
    #return my_list

    return re.split(r'\t+', text)
#**************************************************************************#
def join_items_in_list_using_delimeter_tab(list_of_items):
    return "\t".join(list_of_items)
#**************************************************************************#
def split_string_to_list_delimeter_comma(text):
    """
    Splitting the text into a list of elements.

    :type text: string
    :param text: Text

    :rtype: list of element
    """
    #my_list = [] # make empty list
    #words = text.split() #for space
    #for current_word in words:
    #    my_list.append(current_word.lower())
    #return my_list

    return text.split(',')
#**************************************************************************#
#nodes=5
def get_str_value_given_key(str_key_value):
    """
    Getting the value given string key=value

    :type str_key_value: string
    :param str_key_value: string key=value

    :rtype: string of value
    """
    list_items = str_key_value.split("=")

    if len(list_items) != 2:
        return ""

    return list_items[1]
#**************************************************************************#
#str.startswith(str, begin_index=0,end_index=len(string));
def is_start_with(string_parent, substring):
    """
    Checking string_parent whether it starts with substring. True/False

    :type string_parent: string
    :param string_parent: string parent

    :type substring: string
    :param substring: sub-string

    :rtype: True/False
    """
    string_parent = string_parent.strip()  # trim
    substring = substring.strip()

    return string_parent.startswith(substring)
#**************************************************************************#
def get_right_content(line, start_by_string):
    """
    Getting right content for Sentence in output from tool Terpa

    Ex: Sentence ID: [TienLe_TanLe][Tien_Tan_system][TienNgocLe_TanNgocLe][5]

    :type start_by_string: string
    :param start_by_string: sub-string

    :rtype: string
    """
    line = line.strip()
    start_by_string = start_by_string.strip()

    if is_start_with(line, start_by_string):
        n = len(start_by_string)
        result = line[n:]
        result = result.strip()
    else:
        result = ""

    return result
#**************************************************************************#
def is_disjoint(list_reference, list_test):
    """
    Checking whether each element of list_test is existed in list_reference or not. True if there is not any item in both list_reference and list_test.

    :type list_reference: list
    :param list_reference: list of reference

    :type list_test: list
    :param list_test: list of testing

    :rtype: True if there is not any item in both list_reference and list_test; False: otherwise
    """
    for item in list_test:
        if item in list_reference:
            return False
        #end if
    #end for

    return True
#**************************************************************************#
def get_list_intersection(list_reference, list_test):
    """
    Getting list intersection between list_reference and list_test.

    :type list_reference: list
    :param list_reference: list of reference

    :type list_test: list
    :param list_test: list of testing

    :rtype: List intersection
    """
    result = []
    for item in list_test:
        if item in list_reference:
            result.append(item)
        #end if
    #end for

    return result
#**************************************************************************#
def get_subset_from_superset(list_superset, number_of_items_in_subset):
    """
    Getting all subsets that have the number of item in subset.

    :type list_superset: list
    :param list_superset: contains the data of superset

    :type number_of_item_in_subset: int
    :param number_of_item_in_subset: the number of items in subset

    :raise ValueError: if number_of_items_in_subset >= len(list_superset)
    """
    if number_of_items_in_subset >= len(list_superset):
        raise Exception("The number of items in subset should smaller then the number of items in superset.")

    return itertools.combinations(list_superset, number_of_items_in_subset)
#**************************************************************************#
def print_introduction(file_output_path):
    #for writing append: file_output_path
    file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

    str_intro = "Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole Toolkit (eval_agent Toolkit) \n"
    str_intro += "Homepage: http://getalp.imag.fr \n"
    str_intro += "Author: Tien Ngoc LE (ngoc-tien.le@imag.fr) \n"
    str_intro += "Advisors: Laurent Besacier & Benjamin Lecouteux \n"
    str_intro += "URL: tienhuong.weebly.com \n"

    file_writer.write(str_intro)
    print(str_intro)
    file_writer.write("\n")

    file_writer.close()
#*****************************************************************************#
def print_result(feature_name, file_output_path):
    #for writing append: file_output_path
    file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

    str_output = "END - Processing - " + feature_name + " - Done at " + str(datetime.datetime.now()) + "\n"

    print(str_output)
    file_writer.write(str_output)
    file_writer.write("\n")

    file_writer.close()
#*****************************************************************************#
def print_time(feature_name, file_output_path):
    #for writing append: file_output_path
    file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

    ruler = ""
    for i in range(len(feature_name) + 40):
        ruler += "="

    print(ruler)
    file_writer.write(ruler)
    file_writer.write("\n")

    str_feature_name = "= " + feature_name + " start at " + str(datetime.datetime.now()) + " ="
    print(str_feature_name)
    file_writer.write(str_feature_name)
    file_writer.write("\n")

    print(ruler)
    file_writer.write(ruler)
    file_writer.write("\n")

    file_writer.close()
#**************************************************************************#
def get_list_of_oracle_label_and_list_of_wapiti_label_from_result_wapiti_labeling(file_input_path):
    """
    Getting the list of oracle label and list of wapiti label from the result of tool wapiti

    :type file_input_path: string
    :param file_input_path: The path of result of tool wapiti (included oracle label)

    :rtype: list_of_oracle_label, list_of_wapiti_label

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('(included oracle label) File does not exist: '+file_input_path)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    list_of_oracle_label = []
    list_of_wapiti_label = []

    ## 0 0.997856
    #0	0	0	0	0	1	1	1	1	NNS	8	3	1	F	2	2	2	2	surgeons	NNS	surgeon	in	IN	in	_X-1	_X-1	_X-1	chirurgiens	NOM	chirurgien	de	PRP	de	les	DET	le	0.7177257489511406	surgeons	0.19413	2	0.19413	0.80587	G	G	G/0.999993
    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            continue
        #end if

        list_of_items = line.split()
        length_of_list = len(list_of_items)
        if length_of_list < 6: ## 0 0.997856
            continue
        #end if

        #0	0	0	0	0	1	1	1	1	NNS	8	3	1	F	2	2	2	2	surgeons	NNS	surgeon	in	IN	in	_X-1	_X-1	_X-1	chirurgiens	NOM	chirurgien	de	PRP	de	les	DET	le	0.7177257489511406	surgeons	0.19413	2	0.19413	0.80587	G	G	G/0.999993
        label_oracle = list_of_items[length_of_list - 3]
        label_wapiti = list_of_items[length_of_list - 2]

        list_of_oracle_label.append(label_oracle)
        list_of_wapiti_label.append(label_wapiti)
    #end for

    #close file
    file_reader.close()

    return list_of_oracle_label, list_of_wapiti_label
#**************************************************************************#
#Find Z ? How many number of labels --> ?Good ; ?Bad
#Let Z be the total number of words which true label is G/B (oracle label)
#Let Y be the total number of words classified as G/B (Tong so tu duoc gan nhan la G/B)
def get_number_of_words_with_label_good_and_bad_in_list_label(list_of_label):
    """
    Getting list of words' labels that has the same length and ALL labels are Good/Bad

    :type list_of_label: string
    :param list_of_label: contains list of word label that is list of oracle label or list of classifier label.

    :type label_all_word: string
    :param label_all_word: "G"/"B"

    :rtype: list that has two item: Number of label "Good" AND Number of label "Bad"

    :raise ValueError: if len(list_of_oracle_label) = 0
    """
    if len(list_of_label) == 0:
        raise Exception("You should check list of oracle label that must be existed.")

    num_of_label_good = 0
    num_of_label_bad = 0
    #label_good = "G"
    #label_bad = "B"
    current_config = load_configuration()
    label_good = current_config.LABEL_GOOD
    label_bad = current_config.LABEL_BAD

    for item in list_of_label:
        if item == label_good:
            num_of_label_good += 1
        elif item == label_bad:
            num_of_label_bad += 1
    #end for

    #result.append(num_of_label_good)
    #result.append(num_of_label_bad)

    #return result
    return num_of_label_good, num_of_label_bad
#**************************************************************************#
def get_number_of_words_with_label_good_and_bad_in_list_label_threads(list_of_label,current_config):
    """
    Getting list of words' labels that has the same length and ALL labels are Good/Bad

    :type list_of_label: string
    :param list_of_label: contains list of word label that is list of oracle label or list of classifier label.

    :type label_all_word: string
    :param label_all_word: "G"/"B"

    :rtype: list that has two item: Number of label "Good" AND Number of label "Bad"

    :raise ValueError: if len(list_of_oracle_label) = 0
    """
    if len(list_of_label) == 0:
        raise Exception("You should check list of oracle label that must be existed.")

    num_of_label_good = 0
    num_of_label_bad = 0
    #label_good = "G"
    #label_bad = "B"
    #current_config = load_configuration()
    label_good = current_config.LABEL_GOOD
    label_bad = current_config.LABEL_BAD

    for item in list_of_label:
        if item == label_good:
            num_of_label_good += 1
        elif item == label_bad:
            num_of_label_bad += 1
    #end for

    #result.append(num_of_label_good)
    #result.append(num_of_label_bad)

    #return result
    return num_of_label_good, num_of_label_bad
#**************************************************************************#
#Let X be the number of words whose true label is G/B and have been tagged with this label by the classifier (So tu duoc classifier gan nhan dung la G/B, vi co khi nhan oracle label cua no la B/G nhung classifier gan la G/B)
def get_number_of_words_with_same_label_between_classifier_label_and_oracle_label(list_of_oracle_label, list_of_classifier_label, word_label):
    """
    Getting the number of words whose true label is G/B and have been tagged with this label by the classifier.

    :type list_of_oracle_label: string
    :param list_of_oracle_label: contains list of word label (oracle label)

    :type list_of_classifier_label: string
    :param list_of_classifier_label: contains list of classifier label

    :type word_label: string
    :param word_label: given "G"/"B"

    :rtype: the number of words whose true label is G/B and have been tagged with this label by the classifier.

    :raise ValueError: if list_of_oracle_label and list_of_classifier_label does not have the same length.
    """
    length_list_of_oracle_label = len(list_of_oracle_label)
    length_list_of_classifier_label = len(list_of_classifier_label)

    if length_list_of_oracle_label != length_list_of_classifier_label:
        raise Exception("You should check the length of list of oracle label and the length of list of classifier label.")

    #Dem so luong tu co nhan la word_label o ca 2 list, phu thuoc vao list of classifier label
    result = 0
    range_length = range(length_list_of_oracle_label)

    for i in range_length:
        if list_of_oracle_label[i] == word_label and list_of_classifier_label[i] == word_label:
            result += 1
        #end if
    #end for

    return result
#**************************************************************************#
#ref NLTK.metrics.scores
def accuracy(reference, test):
    """
    Getting list of words' labels that has the same length and ALL labels are Good/Bad

    :type list_of_oracle_label: string
    :param list_of_oracle_label: contains list of word label (oracle label)

    :type label_all_word: string
    :param label_all_word: "G"/"B"

    :raise ValueError: if any path is not existed
    """
    nltk.metrics.scores.accuracy(reference, test)
#**************************************************************************#
#B1: tao 1 mang ngau nhien B/G voi chieu dai bang chieu dai cua danh sach oracle label
#B2: Ap dung cong thuc tinh X, Y, Z --> Pr, Rc, F

#PP tong quat: dua vao 1 mang chua du lieu B/G roi dua ra ket qua gom:
#X,Y,Z,Pr,Rc,F
#dua vao ham nay thay doi thuat toan trong Baseline
#VD: Khoi tao danh sach toan bo la B/G roi goi ham tinh
def get_precision_recall_fscore_within_list(reference, test):
    """
    Getting the scores both X, Y, Z and Precision; Recall; F-score.
    + Pr of a specific label characterizes the ability of system to predict correctly (for it) over all classified words.
    + Rc reflects how efficient the system is in retrieving the accurate labels from DB.
    + F is the harmonic mean of Precision and Recall
    Pr = X/Y
    Rc = X/Z
     F = (2*Pr*Rc)/(Pr+Rc)

    :type reference: list
    :param reference: list of label G/B

    :type test: list
    :param test: list of label G/B

    :rtype: the values of X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good
    """

    """
    Let X be the number of words whose true label is B and have been tagged with this label by the classifier (So tu duoc classifier gan nhan dung la B, vi co khi nhan oracle label cua no la G nhung classifier gan la B)
    Let Y be the total number of words classified as B (Tong so tu duoc gan nhan la B)
    Let Z be the total number of words which true label is B (oracle label)
    """
    ############
    #B-label
    word_label_bad = "B"
    word_label_good = "G"
    #X?
    X_bad = get_number_of_words_with_same_label_between_classifier_label_and_oracle_label(reference, test, word_label_bad)
    X_good = get_number_of_words_with_same_label_between_classifier_label_and_oracle_label(reference, test, word_label_good)

    #Y?
    Y_good, Y_bad = get_number_of_words_with_label_good_and_bad_in_list_label(test)

    #Z?
    Z_good, Z_bad = get_number_of_words_with_label_good_and_bad_in_list_label(reference)


    #Sau khi co X, Y, Z thi goi ham sau
    #get_precision_recall_fscore(X, Y, Z)
    Pr_bad, Rc_bad, F_bad = get_precision_recall_fscore( X_bad, Y_bad, Z_bad)
    Pr_good, Rc_good, F_good = get_precision_recall_fscore( X_good, Y_good, Z_good)

    return X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good
#**************************************************************************#
#Viet ham danh cho phan tinh Pr; Rc; F-score
#Pr = X/Y
#Rc = X/Z
# F = (2*Pr*Rc)/(Pr+Rc)

def get_precision_recall_fscore_within_list_threads(reference, test, current_config):
    """
    Getting the scores both X, Y, Z and Precision; Recall; F-score.
    + Pr of a specific label characterizes the ability of system to predict correctly (for it) over all classified words.
    + Rc reflects how efficient the system is in retrieving the accurate labels from DB.
    + F is the harmonic mean of Precision and Recall
    Pr = X/Y
    Rc = X/Z
     F = (2*Pr*Rc)/(Pr+Rc)

    :type reference: list
    :param reference: list of label G/B

    :type test: list
    :param test: list of label G/B

    :rtype: the values of X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good
    """

    """
    Let X be the number of words whose true label is B and have been tagged with this label by the classifier (So tu duoc classifier gan nhan dung la B, vi co khi nhan oracle label cua no la G nhung classifier gan la B)
    Let Y be the total number of words classified as B (Tong so tu duoc gan nhan la B)
    Let Z be the total number of words which true label is B (oracle label)
    """
    ############
    #B-label
    word_label_bad = "B"
    word_label_good = "G"
    #X?
    X_bad = get_number_of_words_with_same_label_between_classifier_label_and_oracle_label(reference, test, word_label_bad)
    X_good = get_number_of_words_with_same_label_between_classifier_label_and_oracle_label(reference, test, word_label_good)

    #Y?
    Y_good, Y_bad = get_number_of_words_with_label_good_and_bad_in_list_label_threads(test, current_config)

    #Z?
    Z_good, Z_bad = get_number_of_words_with_label_good_and_bad_in_list_label_threads(reference, current_config)


    #Sau khi co X, Y, Z thi goi ham sau
    #get_precision_recall_fscore(X, Y, Z)
    Pr_bad, Rc_bad, F_bad = get_precision_recall_fscore( X_bad, Y_bad, Z_bad)
    Pr_good, Rc_good, F_good = get_precision_recall_fscore( X_good, Y_good, Z_good)

    return X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good
#**************************************************************************#
#Viet ham danh cho phan tinh Pr; Rc; F-score
#Pr = X/Y
#Rc = X/Z
# F = (2*Pr*Rc)/(Pr+Rc)

def get_precision_recall_fscore(X, Y, Z):
    """
    Getting the scores Precision; Recall and F-score with X, Y, Z given.
    + Pr of a specific label characterizes the ability of system to predict correctly (for it) over all classified words.
    + Rc reflects how efficient the system is in retrieving the accurate labels from DB.
    + F is the harmonic mean of Precision and Recall
    Pr = X/Y
    Rc = X/Z
     F = (2*Pr*Rc)/(Pr+Rc)

    :type X: int
    :param X: Let X be the number of words whose true label is B and have been tagged with this label by the classifier

    :type Y: int
    :param Y: Let Y be the total number of words classified as B

    :type Z: int
    :param Z: Let Z be the total number of words which true label is B (oracle label)

    :rtype: the values of Pr, Rc and F
    """

    """
    Let X be the number of words whose true label is B and have been tagged with this label by the classifier (So tu duoc classifier gan nhan dung la B, vi co khi nhan oracle label cua no la G nhung classifier gan la B)
Let Y be the total number of words classified as B (Tong so tu duoc gan nhan la B)
Let Z be the total number of words which true label is B (oracle label)
    """
    Pr = 0
    Rc = 0
    F = 0
    if Y == 0 and Z == 0:
        Pr = -1
        Rc = -1
        F = -1
    elif Y == 0:
        Pr = -1 #Not a number
        Rc = X/Z
        F = -1 #Not a number
    elif Z == 0:
        Pr = X/Y
        Rc = -1
        F = -1
    else:
        Pr = X/Y
        Rc = X/Z

        if Pr+Rc == 0:
            F = -1 # Not a Number
        else:
            F = (2*Pr*Rc)/(Pr+Rc)
        #end if
    #end if

    return Pr, Rc, F
#**************************************************************************#
def convert_text_to_decimal(str_input):
    array_bytes = str_input.encode('utf-8') #tuong tu lenh: array_bytes = bytes(str_input, 'utf-8')

    #ref: https://docs.python.org/dev/library/stdtypes.html#int.from_bytes
    #If byteorder is "big", the most significant byte is at the beginning of the byte array.
    #If byteorder is "little", the most significant byte is at the end of the byte array.

    result = int.from_bytes(array_bytes, byteorder='big')
    #result = int.from_bytes(array_bytes, byteorder='little')
    """
    for x in array_bytes:
        result += x
    #end for
    """
    return result
#**************************************************************************#
#list_of_exceptions = ["<unknown>", "unk", "<UNKNOWN>", "UNK", "_X-2", "_X-1", "_X+1", "_X+2"]
def convert_text_to_decimal_within_list_of_exceptions(str_input, list_of_exceptions):
    if str_input in list_of_exceptions:
        return 0
    #end if

    result = convert_text_to_decimal(str_input)

    return result
#**************************************************************************#
def replace_substring_in_string(str_input, str_find, str_replace):
    #return string after replacing
    return str_input.replace(str_find, str_replace)
#**************************************************************************#
def get_distance_euclide(x, y):
    """Getting distance Euclide between 2 vectors
    """
    if len(x) != len(y):
        raise Exception("Cannot calculate distance Euclide :) ")
    return math.sqrt(sum((x[i] - y[i])**2 for i in range(len(x))))
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    print("OK")