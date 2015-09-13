# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:39:11 2015
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
#import re
import linecache
import shutil
#import stat
#import datetime
import random
import threading
import time

#for call shell script
#import shlex, subprocess

#**************************************************************************#
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from config.configuration import *
#from config.config_end_user import *

from common_module.cm_config import load_configuration, load_config_end_user, get_absolute_path_current_module
from common_module.cm_util import  is_in_string, split_string_to_list_delimeter_tab, get_list_of_oracle_label_and_list_of_wapiti_label_from_result_wapiti_labeling, get_precision_recall_fscore_within_list, replace_substring_in_string
from common_module.cm_script import create_script_temp, call_script, run_chmod
#**************************************************************************#
def get_list_from_file(file_list_path):
    """
    Getting List from the file

    :type file_list_path: string
    :param file_list_path: contains the punctuations with format "each line is a punctuation"

    :raise ValueError: if path is not existed
    """

    #initialization with empty list
    my_list = []

    #check existed path
    """
    if not os.path.exists(file_list_path):
        raise TypeError('Not Existed file List Of Punctuations')
    """
    str_message_if_not_existed = "Not Existed file input that contains list"
    is_existed_file(file_list_path, str_message_if_not_existed)

    #open file
    file_reader = open(file_list_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #read data in openned file
    for line in file_reader:
        #checking empty line
        line = line.strip() #trim line

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            continue #No append to list
        else:
            my_list.append(line.strip()) #adding a new element to the end of a list

    #close file
    file_reader.close()

    return my_list
#**************************************************************************#
def get_list_from_file_for_verify(file_list_path):
    """
    Getting List from the file that is used for verify_result_old_and_new.py

    :type file_list_path: string
    :param file_list_path: contains the punctuations with format "each line is a punctuation"

    :raise ValueError: if path is not existed
    """

    #initialization with empty list
    my_list = []

    #check existed path
    """
    if not os.path.exists(file_list_path):
        raise TypeError('Not Existed file List Of Punctuations')
    """
    str_message_if_not_existed = "Not Existed file input that contains list"
    is_existed_file(file_list_path, str_message_if_not_existed)

    #open file
    file_reader = open(file_list_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #read data in openned file
    for line in file_reader:
        #checking empty line
        line = line.strip() #trim line

        my_list.append(line) #adding a new element to the end of a list

    #close file
    file_reader.close()

    return my_list
#**************************************************************************#
def convert_format_column_to_format_row_from_output_treetagger_old(file_input_path, file_output_path):
    """
    Converting format column to format row

    :type file_input_path: string
    :param file_input_path: each line contains output of tool TreeTagger. If POS == SENT thi ket thuc cau do

    :type file_output_path: string
    :param file_output_path: Text

    :raise ValueError: if path is not existed
    """

    #initialization with empty list
    my_list = []

    #check existed path
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file file_input_path')
    """

    str_message_if_not_existed = "Not Existed file input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open file
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    #cap nhat them 1 flag de biet duoc co ghi hay khong
    my_flag_not_saved = False
    str_unknown = "<unknown>"
    str_end_of_sentence = "SENT"
    delimiter_char = "|||"

    #read data in openned file
    for line in file_reader:
        #checking empty line
        line = line.strip() #trim line

        line_split = split_string_to_list_delimeter_tab(line)

        if len(line_split) == 0:
            raise Exception("du lieu dua vao ham split_string_to_list_delimeter_tab khong dung. Kiem tra lai nha :)")
        else:
            line_word = line_split[0]
            line_pos = line_split[1]
            line_stemming = line_split[2]

            if line_stemming == str_unknown: #muc dich: De khi thong ke thi phan tu nay chiem rat nho trong csdl. Neu de unknown thi khi dua vao so luong unknown de tinh toan --> du lieu khong duoc tot
                #line_stemming = line_word
                #cap nhat lai line nay
                #line = line_word + "/t" + line_pos + "/t" + line_stemming

                line_split[2] = line_word
                #cap nhat lai line nay
                line = "\t".join(line_split)

            #end if
            if line_pos == str_end_of_sentence:
                if my_flag_not_saved == False:
                    #combine all items in list by space character to string
                    line_out = delimiter_char.join(my_list)

                    #write to output file
                    file_writer.write(line_out)

                    file_writer.write("\n") #new line
                    my_flag_not_saved == True #saved

                    #reinitialization with empty list
                    my_list = []
            else:
                my_list.append(line) #adding a new element to the end of a list
                my_flag_not_saved = False
            #end if
        #end if
    #end for

    #neu trong file format column khong co dong trong cuoi dung thi dung ham nay de kiem tra va luu sentence cuoi
    if my_flag_not_saved == False:
        #combine all items in list by space character to string
        line_out = delimiter_char.join(my_list)

        #write to output file
        file_writer.write(line_out)

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def get_file_contains_number_of_words_each_line(file_input_path, file_output_path):
    """
    Getting the number of words of each sentence in each line.

    :type file_input_path: string
    :param file_input_path: string

    :type file_output_path: string
    :param file_output_path: number of words in each line

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file input')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    number_of_words = 0

    # read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        number_of_words = len(line.split()) # cac tu cach nhau bang khoang trang

        file_writer.write(str(number_of_words))
        file_writer.write("\n")
    #end for

    #close files
    file_reader.close()
    file_writer.close()
#**************************************************************************#

#cach nay cung khong kha thi
#vi treetagger hieu qu' thanh qu ' ; a-t-il thanh avoir va il
def convert_format_column_to_format_row_from_output_treetagger(file_input_path, file_number_of_words_path, file_output_path):
    """
    Converting format column to format row

    :type file_input_path: string
    :param file_input_path: each line contains output of tool TreeTagger. If POS == SENT thi ket thuc cau do

    :type file_number_of_words_path: string
    :param file_number_of_words_path: each line the number of words of sentence respectively

    :type file_output_path: string
    :param file_output_path: Text

    :raise ValueError: if path is not existed
    """

    #initialization with empty list
    my_list = []

    #check existed path
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file file_input_path')

    if not os.path.exists(file_number_of_words_path):
        raise TypeError('Not Existed file file_number_of_words_path')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file file_number_of_words_path ("+file_number_of_words_path+")"
    is_existed_file(file_number_of_words_path, str_message_if_not_existed)

    #open file
    file_reader = open(file_number_of_words_path, mode = 'r', encoding = 'utf-8')#, 'r')
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #cap nhat them 1 flag de biet duoc co ghi hay khong
    my_flag_not_saved = False
    str_unknown = "<unknown>"
    #str_end_of_sentence = "SENT"
    delimiter_char = "|||"

    number_of_line_readed = 0

    #y tuong: doc tung dong de lay so tu trong dong do. sau do co bao nhieu tu thi lay bay nhieu dong trong file TreeTagger
    for iline in file_reader:
        """
        print("*Da doc den cau*")
        print(number_of_line_readed)
        print(iline)
        print("*Da doc den cau*")
        """
        number_of_words = int(iline)

        #sau do co bao nhieu tu thi lay bay nhieu dong trong file TreeTagger
        #get_line_given_number_of_sentence(file_input_path, number_of_sentence)
        #gia tri tra ve da ton tai \n
        until_index = number_of_line_readed + number_of_words
        my_list = [] #gia su cau chua co gi
        current_range = range(number_of_line_readed, until_index)
        #range(5, 10) --> 5 through 9
        for item in current_range:
            line_given_number_of_sentence = get_line_given_number_of_sentence(file_input_path, item + 1) #vi item la index nen can phai them 1 don vi de thanh cau thu N

            #checking empty line
            line = line_given_number_of_sentence.strip() #trim line

            print("item")
            print(item)
            print("item")

            print("line")
            print(line)
            print("line")


            line_split = split_string_to_list_delimeter_tab(line)

            if len(line_split) == 0:
                raise Exception("du lieu dua vao ham split_string_to_list_delimeter_tab khong dung. Kiem tra lai nha :)")
            else:
                print("*line_split*")
                print(line_split)
                print("*line_split*")
                line_word = line_split[0]
                line_pos = line_split[1]
                line_stemming = line_split[2]

                if line_stemming == str_unknown: #muc dich: De khi thong ke thi phan tu nay chiem rat nho trong csdl. Neu de unknown thi khi dua vao so luong unknown de tinh toan --> du lieu khong duoc tot
                    #line_stemming = line_word
                    #cap nhat lai line nay
                    #line = line_word + "/t" + line_pos + "/t" + line_stemming

                    line_split[2] = line_word
                    #cap nhat lai line nay
                    line = "\t".join(line_split)
                #end if
            #end if
            my_list.append(line) #adding a new element to the end of a list
            my_flag_not_saved = False
        #end for

        if my_flag_not_saved == False:
            #combine all items in list by space character to string
            line_out = delimiter_char.join(my_list)

            #write to output file
            file_writer.write(line_out)

            file_writer.write("\n") #new line
            my_flag_not_saved == True #saved
            my_list = []

        #end if

        #cap nhat lai number_of_line_readed
        number_of_line_readed += number_of_words#vi se doc tu index 0

        #close file
        file_reader.close()
        file_writer.close()
        raise Exception("Kiem tra ket qua cua dong dau tien :)")

    #end for

    #neu trong file format column khong co dong trong cuoi dung thi dung ham nay de kiem tra va luu sentence cuoi
    if my_flag_not_saved == False:
        #combine all items in list by space character to string
        line_out = delimiter_char.join(my_list)

        #write to output file
        file_writer.write(line_out)

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def get_line_given_number_of_sentence(file_input_path, number_of_sentence):
    """
    Getting line given index in file_input_path

    :type file_input_path: string
    :param file_input_path: Text

    :type number_of_sentence: int
    :param number_of_sentence: number_of_sentence of the line in file, duoc dem tu 1,...,n

    :rtype: return the content of the line that has index which given

    :raise ValueError: if path is not existed
    """
    #check existed path
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file file_input_path')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #linecache — Random access to text lines
    #ref: https://docs.python.org/3.4/library/linecache.html
    result = linecache.getline(file_input_path, number_of_sentence) #co chua \n

    #print(result)
    #.strip() #de khong chua ky tu xuong dong
    return result

#**************************************************************************#
def get_target_sentence_from_output_moses(string_output_alignment_target_to_source_from_moses_path):
    """
    Creating list of alignment word to word from Source To Target
    =============================================================
    0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15

    :type string_output_alignment_target_to_source_from_moses_path: string
    :param string_output_alignment_target_to_source_from_moses_path: the string of ouput included alignment word to word from Source To Target from MOSES

    :rtype: the string of target sentence
    """
    result = "" # empty string
    list_of_group = [] #gan danh sach cac nhom la RONG
    delimiter = "|||"

    #trim line_input
    string_output_alignment_target_to_source_from_moses_path = string_output_alignment_target_to_source_from_moses_path.strip()

    # split cac nhom khac nhau --> chon nhom cuoi
    list_of_group = string_output_alignment_target_to_source_from_moses_path.split(delimiter)

    #target sentence
    result = list_of_group[1].strip()
    """
    print("************************************")
    print("Target sentence sau khi xu ly la: ")
    print(result)
    print("************************************")
    """
    return result
#---------------------------------------------------------------------------#
def get_file_hypothethis_from_output_moses(file_output_from_moses_path, file_output_path):
    """
    Getting the hypothesis from output of MOSES
    =============================================================
    0 ||| yet a crucial step for the Balkans .  ||| d: 0 -1.39532 0 0 -1.10053 0 0 lm: -135.242 tm: -3.65122 -9.83896 -3.59304 -6.25423 3.99959 w: -8 ||| -164.237 ||| 0=0 1-4=1-4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7

    :type string_output_alignment_target_to_source_from_moses_path: string
    :param string_output_alignment_target_to_source_from_moses_path: contains the string of ouput included alignment word to word from target to source from MOSES

    :type file_output_path: string
    :param file_output_path: contains corpus with format row.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_output_from_moses_path):
        raise TypeError('Not Existed file corpus that is output from MOSES')
    """
    str_message_if_not_existed = "Not Existed file corpus input that is result of tool MOSES ("+file_output_from_moses_path+")"
    is_existed_file(file_output_from_moses_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_output_from_moses_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    list_of_group = [] #gan danh sach cac nhom la RONG
    delimiter = "|||"

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
        else:
            # split cac nhom khac nhau --> chon nhom co index = 1
            list_of_group = line.split(delimiter)

            hypothesis_content = list_of_group[1].strip() #index = 1

            file_writer.write(hypothesis_content)
            file_writer.write('\n')


    #close 2 files
    file_reader.close()
    file_writer.close()
#---------------------------------------------------------------------------#
#doi voi version moses 2009 thi item cuoi cung trong string la alignment from TARGET to SOURCE
#do do, can cap nhat lai ham nay cho chuan
#version cua ham nay dung cho du lieu o nhom cuoi cua MOSES duoc hieu la: alignment from TARGET to SOURCE
#get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET
"""
Vi du:
0 ||| yet a crucial step for the Balkans .  ||| d: 0 -1.39532 0 0 -1.10053 0 0 lm: -135.242 tm: -3.65122 -9.83896 -3.59304 -6.25423 3.99959 w: -8 ||| -164.237 ||| 0=0 1-4=1-4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7
"""
#Chu y: Khi update ham nay thi cung can update ham dung cho fast_align
#get_list_alignment_target_to_source_from_line_output_fast_align_TARGET_To_SOURCE
def get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(string_output_alignment_target_to_source_from_moses_path):
    """
    Creating list of alignment word to word from TARGET to SOURCE
    =============================================================
    0 ||| yet a crucial step for the Balkans .  ||| d: 0 -1.39532 0 0 -1.10053 0 0 lm: -135.242 tm: -3.65122 -9.83896 -3.59304 -6.25423 3.99959 w: -8 ||| -164.237 ||| 0=0 1-4=1-4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7

    :type string_output_alignment_target_to_source_from_moses_path: string
    :param string_output_alignment_target_to_source_from_moses_path: the string of ouput included alignment word to word from target to source from MOSES

    :rtype: list of alignment word to word from target to source, Note: if value = '' then value=-1 that means there is no word in Source language associated.
    """
    result = [] # empty list
    list_after_split = [] # contains items after splitting
    char_equal = "=" # Source to Target (in lastest MOSES), Target To Source (in MOSES 2009)
    char_minus = "-" # Target To Source (in lastest MOSES)
    current_char = "" # contains which char in the string-input

    list_of_group = [] #gan danh sach cac nhom la RONG
    delimiter = "|||"
    #num_of_sentence = 0

    #trim line_input
    string_output_alignment_target_to_source_from_moses_path = string_output_alignment_target_to_source_from_moses_path.strip()

    # split cac nhom khac nhau --> chon nhom cuoi
    list_of_group = string_output_alignment_target_to_source_from_moses_path.split(delimiter)

    #alignment Target to Source
    #lay nhom cuoi
    string_output_alignment_target_to_source_path = list_of_group[len(list_of_group)-1]

    #trim string alignment
    string_output_alignment_target_to_source_path = string_output_alignment_target_to_source_path.strip()
    """
    print("***************************")
    print("Alignment TARGET to SOURCE")
    print(string_output_alignment_target_to_source_path)
    print("***************************")
    """
    #Lay so tu trong chuoi dich, index_group = 1 (nhom thu 2)
    string_target_language = list_of_group[1].strip()
    number_of_words_in_target_language = len(string_target_language.split())
    """
    print("*number_of_words_in_target_language*")
    print(number_of_words_in_target_language)
    print("*number_of_words_in_target_language*")
    """
    if is_in_string(char_equal,string_output_alignment_target_to_source_path):  # if string-input contains delimiter by "="
        current_char= char_equal
    else: # if string-input contains delimiter by "-"
        current_char= char_minus
    #end if

    # split string --> {'0=0', '1=1',..., '23=25,26'}
    list_after_split = string_output_alignment_target_to_source_path.split()
    """
    print("*list_after_split*")
    print(list_after_split)
    print("*list_after_split*")
    """
    # find max-index of Target Side (left side) in string-input
    # co the tim so tu trong Target side o nhom 2 nen khong can lam buoc nay
    """
    max_index_target_side = 0
    for item in list_after_split:
        split_temp = item.split(current_char) # list contain left and right side of each item in list_after_split
        if len(split_temp) == 0:
            print("Kiem tra lai phan tu trong alignment from Target To Source")
            continue

        value_index_0 = split_temp[0] # left side
        value_index_1 = split_temp[1] # right side

        int_value_index_0 = int(value_index_0)

        if max_index_target_side < int_value_index_0: # cap nhat max_index_target_side
            max_index_target_side = int_value_index_0

    #just for testing :)
    print("************************************")
    print("Max index target side in current line: %d" %max_index_target_side)
    print("************************************")
    """

    # tao mang result voi so phan tu bang max_index_target_side + 1
    # range_result = range(max_index_target_side + 1) #version 1
    range_result = range(number_of_words_in_target_language)
    for item in range_result:
        result.append('') # '' gia su tu dich nay khong lien ket voi tu nao o nguon
    """
    print("*number_of_words_in_target_language*************")
    print(number_of_words_in_target_language)
    print("*number_of_words_in_target_language*************")
    """
    #duyet lai list_after_split de dua vao list result
    #tai sao lai lam 2 lan nhu vay? --> vi trong list_after_split cac index o left side khong theo tuan tu.
    #vi du: 0-0 1-1 2-2 3-3 4-4 5-5 7-6 6-8 8-9 9-9 11-11 10-12 12-14 15-15 16-16 13-17 14-18 17-19 18-20 19-21 20-22 22-23 21-24 23-25 24-26 25-27
    #left side: index 13 va 14 dung sau 15, 16 --> De bi lap trinh sai neu chi dung index
    #cach 2: chung ta co the gia su danh sach result co 100 phan tu ban dau. Nhung neu lam cach nay thi kho khan trong viec Debug de biet chinh xac so tu trong cau hien tai :) --> chap nhan lam cach 1 :)
    for item in list_after_split:
        split_temp = item.split(current_char) # list contain left and right side of each item in list_after_split
        #print("*split_temp**********************")
        #print(split_temp)
        #print("*split_temp**********************")
        if len(split_temp) == 0:
            print("Kiem tra lai phan tu trong alignment from Target To Source")
            continue

        value_index_0 = split_temp[0] # left side
        value_index_1 = split_temp[1] # right side, co khi la chuoi

        int_value_index_0 = int(value_index_0)
        """
        print("*int_value_index_0**********************")
        print(int_value_index_0)
        print("*int_value_index_0**********************")
        """
        #gan gia tri voi index trong result
        #result[int_value_index_0] = value_index_1
        if result[int_value_index_0] == "":
            result[int_value_index_0] = value_index_1
        else:
            result[int_value_index_0] = result[int_value_index_0] + "," + value_index_1
        #end if
    #end for

    """
    print("************************************")
    print("Danh sach result sau khi xu ly la - from_line_output_moses: ")
    print(string_output_alignment_target_to_source_from_moses_path)
    print("\n")
    print(result)
    print("************************************")
    """
    return result

#---------------------------------------------------------------------------#
def get_list_alignment_target_to_source_from_line_output_fast_align_TARGET_To_SOURCE(string_output_alignment_target_to_source_from_fast_align_path, string_target_language):
    """
    Creating list of alignment word to word from TARGET to SOURCE
    =============================================================
    0-0 1-1 2-3 3-2 4-4 5-5 6-6 7-7

    :type string_output_alignment_target_to_source_from_moses_path: string
    :param string_output_alignment_target_to_source_from_moses_path: the string of ouput included alignment word to word from target to source from MOSES

    :rtype: list of alignment word to word from target to source, Note: if value = '' then value=-1 that means there is no word in Source language associated.
    """
    result = [] # empty list
    list_after_split = [] # contains items after splitting
    char_equal = "=" # Source to Target (in lastest MOSES), Target To Source (in MOSES 2009)
    char_minus = "-" # Target To Source (in lastest MOSES)
    current_char = "" # contains which char in the string-input

    #list_of_group = [] #gan danh sach cac nhom la RONG
    #delimiter = "|||"
    #num_of_sentence = 0

    #trim line_input
    #string_output_alignment_target_to_source_from_moses_path = string_output_alignment_target_to_source_from_moses_path.strip()

    # split cac nhom khac nhau --> chon nhom cuoi
    #list_of_group = string_output_alignment_target_to_source_from_moses_path.split(delimiter)

    #alignment Target to Source
    #lay nhom cuoi
    #string_output_alignment_target_to_source_path = list_of_group[len(list_of_group)-1]

    #trim string alignment
    #string_output_alignment_target_to_source_path = string_output_alignment_target_to_source_path.strip()
    string_output_alignment_target_to_source_path = string_output_alignment_target_to_source_from_fast_align_path.strip()
    """
    print("***************************")
    print("Alignment TARGET to SOURCE")
    print(string_output_alignment_target_to_source_path)
    print("***************************")
    """
    #Lay so tu trong chuoi dich, index_group = 1 (nhom thu 2)
    #string_target_language = list_of_group[1].strip()
    number_of_words_in_target_language = len(string_target_language.split())
    """
    print("*number_of_words_in_target_language*")
    print(number_of_words_in_target_language)
    print("*number_of_words_in_target_language*")
    """
    if is_in_string(char_equal,string_output_alignment_target_to_source_path):  # if string-input contains delimiter by "="
        current_char= char_equal
    else: # if string-input contains delimiter by "-"
        current_char= char_minus

    # split string --> {'0=0', '1=1',..., '23=25,26'}
    list_after_split = string_output_alignment_target_to_source_path.split()
    """
    print("*list_after_split*")
    print(list_after_split)
    print("*list_after_split*")
    """
    # find max-index of Target Side (left side) in string-input
    # co the tim so tu trong Target side o nhom 2 nen khong can lam buoc nay
    """
    max_index_target_side = 0
    for item in list_after_split:
        split_temp = item.split(current_char) # list contain left and right side of each item in list_after_split
        if len(split_temp) == 0:
            print("Kiem tra lai phan tu trong alignment from Target To Source")
            continue

        value_index_0 = split_temp[0] # left side
        value_index_1 = split_temp[1] # right side

        int_value_index_0 = int(value_index_0)

        if max_index_target_side < int_value_index_0: # cap nhat max_index_target_side
            max_index_target_side = int_value_index_0

    #just for testing :)
    print("************************************")
    print("Max index target side in current line: %d" %max_index_target_side)
    print("************************************")
    """

    # tao mang result voi so phan tu bang max_index_target_side + 1
    # range_result = range(max_index_target_side + 1) #version 1
    range_result = range(number_of_words_in_target_language)
    for item in range_result:
        result.append('') # '' gia su tu dich nay khong lien ket voi tu nao o nguon
    """
    print("*number_of_words_in_target_language*************")
    print(number_of_words_in_target_language)
    print("*number_of_words_in_target_language*************")
    """
    #duyet lai list_after_split de dua vao list result
    #tai sao lai lam 2 lan nhu vay? --> vi trong list_after_split cac index o left side khong theo tuan tu.
    #vi du: 0-0 1-1 2-2 3-3 4-4 5-5 7-6 6-8 8-9 9-9 11-11 10-12 12-14 15-15 16-16 13-17 14-18 17-19 18-20 19-21 20-22 22-23 21-24 23-25 24-26 25-27
    #left side: index 13 va 14 dung sau 15, 16 --> De bi lap trinh sai neu chi dung index
    #cach 2: chung ta co the gia su danh sach result co 100 phan tu ban dau. Nhung neu lam cach nay thi kho khan trong viec Debug de biet chinh xac so tu trong cau hien tai :) --> chap nhan lam cach 1 :)
    for item in list_after_split:
        split_temp = item.split(current_char) # list contain left and right side of each item in list_after_split
        print("*split_temp**********************")
        print(split_temp)
        print("*split_temp**********************")
        if len(split_temp) == 0:
            print("Kiem tra lai phan tu trong alignment from Target To Source")
            continue

        value_index_0 = split_temp[0] # left side
        value_index_1 = split_temp[1] # right side, co khi la chuoi

        int_value_index_0 = int(value_index_0)

        print("*int_value_index_0**********************")
        print(int_value_index_0)
        print("*int_value_index_0**********************")

        #gan gia tri voi index trong result
        if result[int_value_index_0] == "":
            result[int_value_index_0] = value_index_1
        else:
            result[int_value_index_0] = result[int_value_index_0] + "," + value_index_1
        #end if
    """
    print("************************************")
    print("Danh sach result sau khi xu ly la - from_line_output_moses: ")
    print(string_output_alignment_target_to_source_from_moses_path)
    print("\n")
    print(result)
    print("************************************")
    """
    return result

#---------------------------------------------------------------------------#
#version cua ham nay dung cho du lieu o nhom cuoi cua MOSES >= 2013 duoc hieu la:
#alignment from SOURCE to TARGET ?????
#ham nay co rat nhieu truong hop ngoai le nhung chua check het -> da kiem soat hau het cac truong hop :)
"""Vi du: 11-13=11-12 --> Khong biet nhom cuoi co hay khong???
0 ||| the chirurgiens of los Angeles ont said qu' ils étaient outrés , said M. Camus .  ||| LexicalReordering0= -1.91753 0 0 -2.12096 0 0 Distortion0= 0 LM0= -145.241 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -3.22583 -4.66521 ||| -914.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
"""
def get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(string_output_alignment_target_to_source_from_moses_path):
    """
    Creating list of alignment word to word from Source To Target
    =============================================================
    0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15

    :type string_output_alignment_target_to_source_from_moses_path: string
    :param string_output_alignment_target_to_source_from_moses_path: the string of ouput included alignment word to word from Source To Target from MOSES

    :rtype: list of alignment word to word from Source To Target, Note: if value = '' then value=-1 that means there is no word in Source language associated.
    """
    result = [] # empty list
    list_after_split = [] # contains items after splitting
    char_equal = "=" # Source to Target (in lastest MOSES), Source To Target (in MOSES 2009)
    char_minus = "-" # Source To Target (in lastest MOSES)
    current_char = "" # contains which char in the string-input

    list_of_group = [] #gan danh sach cac nhom la RONG
    delimiter = "|||"
    #num_of_sentence = 0

    #print("string_output_alignment_target_to_source_from_moses_path-BEGIN")
    #print(string_output_alignment_target_to_source_from_moses_path)
    #print("string_output_alignment_target_to_source_from_moses_path-END")

    #trim line_input
    string_output_alignment_target_to_source_from_moses_path = string_output_alignment_target_to_source_from_moses_path.strip()

    # split cac nhom khac nhau --> chon nhom cuoi
    list_of_group = string_output_alignment_target_to_source_from_moses_path.split(delimiter)

    #alignment Source to Target
    #lay nhom cuoi
    string_output_alignment_target_to_source_path = list_of_group[len(list_of_group)-1]

    #trim string alignment
    string_output_alignment_target_to_source_path = string_output_alignment_target_to_source_path.strip()
    """
    print("***************************")
    print("Alignment Source To Target")
    print(string_output_alignment_target_to_source_path)
    print("***************************")
    """
    #Lay so tu trong chuoi dich, index_group = 1 (nhom thu 2)
    string_target_language = list_of_group[1].strip()
    number_of_words_in_target_language = len(string_target_language.split())
    """
    print("*number_of_words_in_target_language*")
    print(number_of_words_in_target_language)
    print("*number_of_words_in_target_language*")
    """
    if is_in_string(char_equal,string_output_alignment_target_to_source_path):  # if string-input contains delimiter by "="
        current_char= char_equal
    else: # if string-input contains delimiter by "-"
        current_char= char_minus
    #end if

    # split string --> {'0-0', '1-1',..., '23-25,26'}
    list_after_split = string_output_alignment_target_to_source_path.split()
    """
    print("*list_after_split*")
    print(list_after_split)
    print("*list_after_split*")
    """
    # find max-index of Target Side (left side) in string-input
    # co the tim so tu trong Target side o nhom 2 nen khong can lam buoc nay
    """
    max_index_target_side = 0
    for item in list_after_split:
        split_temp = item.split(current_char) # list contain left and right side of each item in list_after_split
        if len(split_temp) == 0:
            print("Kiem tra lai phan tu trong alignment from Source To Target")
            continue

        value_index_0 = split_temp[0] # left side
        value_index_1 = split_temp[1] # right side

        int_value_index_0 = int(value_index_0)

        if max_index_target_side < int_value_index_0: # cap nhat max_index_target_side
            max_index_target_side = int_value_index_0

    #just for testing :)
    print("************************************")
    print("Max index target side in current line: %d" %max_index_target_side)
    print("************************************")
    """

    # tao mang result voi so phan tu bang max_index_target_side + 1
    # range_result = range(max_index_target_side + 1) #version 1
    range_result = range(number_of_words_in_target_language)
    for item in range_result:
        result.append("") # "" gia su tu dich nay khong lien ket voi tu nao o nguon
    """
    print("*number_of_words_in_target_language*************")
    print(number_of_words_in_target_language)
    print("*number_of_words_in_target_language*************")
    """
    #duyet lai list_after_split de dua vao list result
    #tai sao lai lam 2 lan nhu vay? --> vi trong list_after_split cac index o left side khong theo tuan tu.
    #vi du: 0-0 1-1 2-2 3-3 4-4 5-5 7-6 6-8 8-9 9-9 11-11 10-12 12-14 15-15 16-16 13-17 14-18 17-19 18-20 19-21 20-22 22-23 21-24 23-25 24-26 25-27
    #left side: index 13 va 14 dung sau 15, 16 --> De bi lap trinh sai neu chi dung index
    #cach 2: chung ta co the gia su danh sach result co 100 phan tu ban dau. Nhung neu lam cach nay thi kho khan trong viec Debug de biet chinh xac so tu trong cau hien tai :) --> chap nhan lam cach 1 :)
    for item in list_after_split:
        split_temp = item.split(current_char) # list contain left and right side of each item in list_after_split
        #print("*split_temp**********************")
        #print(split_temp)
        #print("*split_temp**********************")
        if len(split_temp) == 0:
            print("Kiem tra lai phan tu trong alignment from Source To Target")
            continue

        value_index_0 = split_temp[0] # left side, index cua source
        value_index_1 = split_temp[1] # right side, co khi la chuoi, index cua target

        # int_value_index_0 = int(value_index_0) #version 1 - Target _to_ Source
        """
        print("*value_index_0 Source**********************")
        print(value_index_0)
        print("*value_index_0 Source**********************")

        print("*value_index_1 Target**********************")
        print(value_index_1)
        print("*value_index_1 Target**********************")
        """
        #gan gia tri voi index trong result
        #result[int_value_index_0] = value_index_1 #version 1 - Target _to_ Source

        #version 2 - BEGIN
        comma = ","
        temp_version2 = []

        if is_in_string(char_minus,value_index_0) or is_in_string(comma,value_index_0):
            raise Exception("Kiem tra LEFT SIDE * %s * trong alignment tu Source den Target co ky tu dac biet" %value_index_0)

        int_value_index_0 = int(value_index_0) #gia su phia trai, phia tu Source chi co 1 phan tu


        if is_in_string(char_minus,value_index_1) or is_in_string(comma,value_index_1): #xet phia Target, phia phai co tu 2 phan tu tro len
        #    raise Exception("Kiem tra RIGHT SIDE * %s * trong alignment tu Source den Target co ky tu dac biet" %value_index_1)
            #khi do tu Souce alignment den nhieu tu Target
            if is_in_string(char_minus,value_index_1):
                temp_version2 = value_index_1.split(char_minus)
            else:
                temp_version2 = value_index_1.split(comma)
        else: # phia target _ phia ben phai _ chi co 1 phan tu
            #kiem tra neu ben phai chua du lieu giong nhu: 17=-1, co nghia la: Tu nguon co index 17 khong co lien ket voi tu nao o cau dich
            int_value_index_1 = int(value_index_1)
            if int_value_index_1 == -1:
                continue #bo qua truong hop nay

            temp_version2.append(value_index_1)

        if len(temp_version2) == 0:
            raise Exception("Kiem tra RIGHT SIDE * %s * trong alignment tu Source den Target co ky tu dac biet" %value_index_1)
        else:
            """
            print("temp_version2-BEGIN")
            print(temp_version2)
            print("temp_version2-END")
            """
            for item in temp_version2:
                int_item = int(item) #index target, nhieu dich

                try:
                    #kiem tra tu nguon da co lien ket voi tu dich nao chua
                    #neu chua co thi gan moi
                    if result[int_item] == "":
                        result[int_item] = value_index_0
                    else:#neu da gan voi 1 tu nguon nao do roi thi them vao chuoi va them vao dau ,
                        str_temp = result[int_item] + comma + value_index_0

                        result[int_item] = str_temp  #gan vao list voi format list[target_index] = source1, source2
                    #end if
                except:
                    pass
            #end for

        #version 2 - END
    """
    print("************************************")
    print("version Source to Target _ Danh sach result sau khi xu ly la - from_line_output_moses: ")
    print(string_output_alignment_target_to_source_from_moses_path)
    print(result)
    print("************************************")
    """
    return result
#**************************************************************************#
def delete_all_files_temporary():
    """
    Deleting all files Phrase* in directory "lib/shell_script"
    """
    current_config = load_configuration()

    #using tool MOSES in order to generate n-best-list
    #path_script = current_config.TOOL_N_BEST_TO_LATTICE #Path to the TOOL_N_BEST_TO_LATTICE Tool

    #change mode execute script
    #run_chmod(path_script)

    command_line = "rm -rf Phrase*"

    #print(command_line)

    #generate shell script, roi goi lenh chay script
    #generate shell script
    list_of_commands = []

    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #goi lenh chay
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
def delete_all_files_temporary_threads(current_config):
    """
    Deleting all files Phrase* in directory "lib/shell_script"
    """
    #current_config = load_configuration()

    #using tool MOSES in order to generate n-best-list
    #path_script = current_config.TOOL_N_BEST_TO_LATTICE #Path to the TOOL_N_BEST_TO_LATTICE Tool

    #change mode execute script
    #run_chmod(path_script)

    command_line = "rm -rf Phrase*"

    #print(command_line)

    #generate shell script, roi goi lenh chay script
    #generate shell script
    list_of_commands = []

    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #goi lenh chay
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
def delete_all_files_temporary_within_path_pattern(file_output_path_pattern):
    """
    Deleting all files Phrase* in directory "lib/shell_script"
    """
    current_config = load_configuration()

    #using tool MOSES in order to generate n-best-list
    #path_script = current_config.TOOL_N_BEST_TO_LATTICE #Path to the TOOL_N_BEST_TO_LATTICE Tool

    #change mode execute script
    #run_chmod(path_script)

    command_line = "rm -rf " + file_output_path_pattern + "*"

    #print(command_line)

    #generate shell script, roi goi lenh chay script
    #generate shell script
    list_of_commands = []

    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #goi lenh chay
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
def delete_all_files_temporary_terpa():
    """
    Deleting all files from output of Tool TERp-A in directory "lib/shell_script"
    """
    current_config = load_configuration()

    #change mode execute script
    #run_chmod(path_script)
    """
    rm -rf terp.*
    rm -rf TienNLe_TanNLe_system.*.*
    """

    command_line1 = "rm -rf terp.*"
    command_line2 = "rm -rf Tien_Tan_system.*.*"

    #print(command_line)

    #generate shell script, roi goi lenh chay script
    #generate shell script
    list_of_commands = []

    list_of_commands.append(command_line1)
    list_of_commands.append(command_line2)
    create_script_temp(list_of_commands)

    #goi lenh chay
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
def delete_file_within_given_path(file_input_path):
    """
    Deleting all files Phrase* in directory "lib/shell_script"
    """
    ## if file exists, delete it ##
    if os.path.isfile(file_input_path):
        os.remove(file_input_path)
    else:    ## Show an error ##
        print("Error: %s file not found" % file_input_path)
    #end if
#**************************************************************************#
def delete_file_within_given_path_and_message_error(file_input_path, str_message_error):
    """
    Deleting file within given file path and message error
    """
    ## if file exists, delete it ##
    if os.path.isfile(file_input_path):
        os.remove(file_input_path)
    else:    ## Show an error ##
        print(str_message_error)
    #end if
#**************************************************************************#
def count_number_of_words_in_sentences(file_input_path, file_output_path):
    """
    Counting the number of words in each line with format Column

    :type file_input_path: string
    :param file_input_path: contains the data in file

    :type file_output_path: string
    :param file_output_path: contains the number of words in each sentence

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed input file')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode='w', encoding='utf-8')

    number_of_words_in_sentence = 0
    number_of_sentences = 0

    for line in file_reader:
        line = line.strip() #trim() content of line

        if len(line) ==0: #\n or empty line
            file_writer.write(str(number_of_words_in_sentence))
            file_writer.write("\n")

            number_of_words_in_sentence = 0
            number_of_sentences +=  1
        else:
            number_of_words_in_sentence += 1
        #end if
    #end for

    print("So cau trong file %s la: %d." %(file_input_path, number_of_sentences))

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def count_number_of_words_in_file_format_row(file_input_path):
    """
    Counting the number of words in each line with format ROW

    :type file_input_path: string
    :param file_input_path: contains the data in file

    :rtype: number of words in file

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed input file')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    number_of_words_in_file = 0
    number_of_sentences = 0

    for line in file_reader:
        line = line.strip() #trim() content of line

        number_of_sentences +=  1

        if len(line) == 0:
            print("You should check data, because there is an empty line :)")

        for word in line.split():
            number_of_words_in_file += 1
    #end for

    print("So cau trong file %s la: %d." %(file_input_path, number_of_sentences))
    print("So tu trong file la: %d" %number_of_words_in_file)

    #close file
    file_reader.close()
    return number_of_words_in_file
#**************************************************************************#
def count_number_of_words_in_sentences_format_row(file_input_path, file_output_path):
    """
    Counting the number of words in each line with format ROW

    :type file_input_path: string
    :param file_input_path: contains the data in file

    :rtype: number of words in file

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed input file')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode='w', encoding='utf-8')

    number_of_sentences = 0
    for line in file_reader:
        number_of_words_in_sentence = 0
        line = line.strip() #trim() content of line

        number_of_sentences +=  1

        if len(line) == 0:
            print("You should check data, because there is an empty line :)")

        for word in line.split():
            number_of_words_in_sentence += 1
        #end for

        file_writer.write(str(number_of_words_in_sentence) + "\n")

    #end for

    print("So cau trong file %s la: %d." %(file_input_path, number_of_sentences))

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def count_number_of_words_in_sentences_format_row_to_result_list(file_input_path):
    """
    Counting the number of words in each line with format ROW

    :type file_input_path: string
    :param file_input_path: contains the data in file

    :rtype: number of words in file

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed input file')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    result = []

    number_of_sentences = 0
    for line in file_reader:
        number_of_words_in_sentence = 0
        line = line.strip() #trim() content of line

        number_of_sentences +=  1

        if len(line) == 0:
            print("You should check data, because there is an empty line :)")

        for word in line.split():
            number_of_words_in_sentence += 1
        #end for

        #file_writer.write(str(number_of_words_in_sentence) + "\n")
        result.append(number_of_words_in_sentence)

    #end for

    print("So cau trong file %s la: %d." %(file_input_path, number_of_sentences))

    #close file
    file_reader.close()

    return result
#**************************************************************************#
def count_number_of_sentences_in_file_within_format_column(file_input_path):
    """
    Counting the number of sentences in file within format Column that is separated by an empty line.

    :type file_input_path: string
    :param file_input_path: contains the data in file with format column

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed input file')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open file:
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    number_of_sentences = 0

    for line in file_reader:
        line = line.strip() #trim() content of line

        if len(line) == 0: #\n or empty line
            number_of_sentences +=  1
        #end if
    #end for

    #print("So cau trong file la: %d." %(number_of_sentences))

    #close file
    file_reader.close()

    return number_of_sentences
#**************************************************************************#
def get_filename(file_path):
    """
    Getting file name within filetype from file's path

    :type file_path: string
    :param file_path: the path of file

    :rtype: file's name within filetype
    """
    return os.path.basename(file_path)
#**************************************************************************#
def convert_format_row_to_format_column(file_input_path, file_output_path):
    """
    Converting the format row to format column

    :type file_input_path: string
    :param file_input_path: contains corpus with format row

    :type file_output_path: string
    :param file_output_path: contains corpus with format column; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    number_of_sentence = 0
    #sum_number_of_words = 0

    #str_unk = "<unk>"
    #str_unk_output = "<unk>\t<unk>\t<unk>"

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        line_split = line.split() #delimiter = space character

        """
        char_lastest = line_split[len(line_split)-1]

        if not is_in_list(char_lastest, list_char_end_of_sentence):
            line = line + " " + default_end_of_sentence
            sum_number_of_sentence = sum_number_of_sentence + 1
            print("Dong khong co dau ket thuc cau: %d" %number_of_sentence)
        """
        for item in line_split:
            item = item.strip() # trim string
            if is_in_string("|||", item): #danh cho make-factor-pos
                """
                if is_in_string(str_unk, item.lower()):
                    item = str_unk_output
                    print(item)
                else:
                    #thay the bang ky tu tab
                    item = item.replace("|||","\t")
                    #sum_number_of_words = sum_number_of_words + 1
                    #print("Tu co thay the: %d" %sum_number_of_words)
                #end if
                """
                #thay the bang ky tu tab
                item = item.replace("|||","\t")
                #sum_number_of_words = sum_number_of_words + 1
                #print("Tu co thay the: %d" %sum_number_of_words)
            #end if

            file_writer.write(item)
            file_writer.write("\n")

        #Cac cau cach nhau bang 1 dong trong
        file_writer.write("\n")
        number_of_sentence = number_of_sentence + 1

    #print("Tong so Dong da duyet la: %d" %number_of_sentence)
    #end for

    #close 2 files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def convert_format_column_to_format_row(file_input_path, file_output_path):
    """
    Converting format column to format row

    :type file_input_path: string
    :param file_input_path: Text

    :type file_output_path: string
    :param file_output_path: Text

    :raise ValueError: if path is not existed
    """

    #initialization with empty list
    my_list = []
    number_of_lines = 0

    #check existed path
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file file_input_path')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open file
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #cap nhat them 1 flag de biet duoc co ghi hay khong
    my_flag_not_saved = False

    #read data in openned file
    for line in file_reader:
        #checking empty line
        line = line.strip() #trim line

        if len(line) == 0: #empty line
            if my_flag_not_saved == False:
                #combine all items in list by space character to string
                line_out = " ".join(my_list)

                #write to output file
                file_writer.write(line_out)
                number_of_lines += 1

                file_writer.write("\n") #new line
                number_of_lines += 1
                my_flag_not_saved == True #saved

                #reinitialization with empty list
                my_list = []
        else:
            my_list.append(line) #adding a new element to the end of a list
            my_flag_not_saved = False
        #end if
    #end for

    #neu trong file format column khong co dong trong cuoi dung thi dung ham nay de kiem tra va luu sentence cuoi
    if my_flag_not_saved == False:
        #combine all items in list by space character to string
        line_out = " ".join(my_list)

        #write to output file
        file_writer.write(line_out)
        number_of_lines += 1

        file_writer.write("\n") #new line
        number_of_lines += 1

    #close file
    file_reader.close()
    file_writer.close()

    #print("So dong co the co trong file result: %d" %number_of_lines)
#**************************************************************************#
#giong ham: concat_all_features(list_of_file_paths, file_output_path)
#trong common_function_metrics
def concatenating_files(list_of_file_paths, file_output_path):
    num_of_sent = 0
    with open(file_output_path, mode = 'w', encoding = 'utf-8') as outfile:
        for f_path in list_of_file_paths:
            with open(f_path, mode = 'r', encoding = 'utf-8') as infile:
                for line in infile:
                    outfile.write(line)
                    num_of_sent += 1
                #end for
            #end with
        #end for
    #end with
    print("Number of sentences in file %s is: %d" %(file_output_path, num_of_sent))
#**************************************************************************#
def copy_file_from_path1_to_path2(path1, path2):
    """
    Copy file from path1 to path2

    :type path1: string
    :param path1: path 1

    :type path2: string
    :param path2: path 2

    :raise ValueError: if any path is not existed
    """
    #check existed path
    """
    if not os.path.exists(path1):
        raise TypeError('Not Existed file input in path1')
    """
    str_message_if_not_existed = "Not Existed file corpus input in ("+path1+")"
    is_existed_file(path1, str_message_if_not_existed)

    shutil.copy2(path1, path2)
#**************************************************************************#
#ref: function "creating_sequential_corpus_train_dev_test_file_from_merged_file"
def splitting_corpus_after_merging_all_features(file_input_path, num_of_sentences, file_output_path1, file_output_path2):
    """
    Splitting corpus from 1 file to 2 file output that the first output file has given number of sentences and the second output file contains the remain sentences.

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :type num_of_sentences: int
    :param num_of_sentences: number of sentences

    :type file_output_path1: string
    :param file_output_path1: the first output file's path

    :type file_output_path2: string
    :param file_output_path2: the second output file's path

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed merged file that contains all features')
    """
    str_message_if_not_existed = "Not Existed file corpus input that contains all merged features ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    number_of_current_sentence = 1

    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing:
    file_writer_1 = open(file_output_path1, mode = 'w', encoding = 'utf-8')
    file_writer_2 = open(file_output_path2, mode = 'w', encoding = 'utf-8')

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line) == 0: #cau moi xuat hien
            number_of_current_sentence += 1
        else:
            if number_of_current_sentence <= num_of_sentences:
                file_writer_1.write(line)
            else:
                file_writer_2.write(line)
            #end if
        #end if

        if number_of_current_sentence <= num_of_sentences:
            file_writer_1.write('\n')
        else:
            file_writer_2.write('\n')
        #end if

    #end for

    #close file
    file_reader.close()
    file_writer_1.close()
    file_writer_2.close()
#**************************************************************************#
def splitting_corpus_for_bl(file_input_path, num_of_sentences_skip, file_output_path):
    """
    Splitting corpus from 1 file to 2 file output that the first output file has given number of sentences and the second output file contains the remain sentences.

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :type num_of_sentences_skip: int
    :param num_of_sentences_skip: number of sentences

    :type file_output_path: string
    :param file_output_path: the first output file's path

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed merged file that contains all features')
    """
    str_message_if_not_existed = "Not Existed file corpus input that contains merged features ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    number_of_current_sentence = 1

    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing:
    file_writer_1 = open(file_output_path, mode = 'w', encoding = 'utf-8')

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line) == 0: #cau moi xuat hien
            number_of_current_sentence += 1
        else:
            if number_of_current_sentence <= num_of_sentences_skip:
                #file_writer_1.write(line)
                continue
            else:
                file_writer_1.write(line)
            #end if
        #end if

        if number_of_current_sentence <= num_of_sentences_skip:
            #file_writer_1.write('\n')
            continue
        else:
            file_writer_1.write('\n')
        #end if

    #end for

    #close file
    file_reader.close()
    file_writer_1.close()
    #file_writer_2.close()
#**************************************************************************#
#B2: Tao cac file dung cho qua trinh train; dev; test
#Tao du lieu tuan tu (Sequential Corpus for train, dev, test)
#remaining sentences in corpus is number_of_sentences_in_file_for_testing
def creating_sequential_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing):
    """
    Generating the sequential corpus for training, developing and testing from merge file. Note: The number of sentences for training corpus is the remaining sentences.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type file_input_path: string
    :param file_input_path: path to merged file that contains all features

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed merged file that contains all features')
    """
    str_message_if_not_existed = "Not Existed file corpus input that contains all features ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #chu y: chuong trinh se sinh ra theo tuan tu 9000 cau dau cho train + 1000 dev + 881 test
    #number_of_sentences_in_file_for_training = 9000
    #number_of_sentences_in_file_for_developing = 1000
    #number_of_sentences_in_file_for_testing = 881 # co nghia la con lai bao nhieu thi dua qua file testing

    number_of_sentences_in_file_for_developing_to = number_of_sentences_in_file_for_training + number_of_sentences_in_file_for_developing

    #number_of_sentences_in_file_for_testing_to = number_of_sentences_in_file_for_developing_to + number_of_sentences_in_file_for_testing

    number_of_current_sentence = 1

    current_config = load_configuration()

    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    training_corpus_path = current_config.TRAIN_FILE_PATH + "_" + demo_name + ".txt"
    developing_corpus_path = current_config.DEV_FILE_PATH + "_" + demo_name + ".txt"
    testing_corpus_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    #for writing:
    file_writer_train = open(training_corpus_path, mode = 'w', encoding = 'utf-8')
    file_writer_dev = open(developing_corpus_path, mode = 'w', encoding = 'utf-8')
    file_writer_test = open(testing_corpus_path, mode = 'w', encoding = 'utf-8')

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line) == 0: #cau moi xuat hien
            number_of_current_sentence += 1
        else:
            if number_of_current_sentence <= number_of_sentences_in_file_for_training:
                file_writer_train.write(line)
            elif number_of_current_sentence <= number_of_sentences_in_file_for_developing_to:
                file_writer_dev.write(line)
            else:
                file_writer_test.write(line)
            #end if
            #continue
        #end if

        if number_of_current_sentence <= number_of_sentences_in_file_for_training:
            file_writer_train.write('\n')
        elif number_of_current_sentence <= number_of_sentences_in_file_for_developing_to:
            file_writer_dev.write('\n')
        else:
            file_writer_test.write('\n')
        #end if

    #end for

    #close file
    file_reader.close()
    file_writer_train.close()
    file_writer_dev.close()
    file_writer_test.close()
#**************************************************************************#
#Random Corpus
#Phuong phap:
#Cho truoc so luong cac cau trong corpus cho tung giai doan training, developing va testing
#Giai doan 1: Lay du lieu ngau nhien tu corpus voi format column
#1.1. Cho so luong cau cua cac corpus --ham--> danh sach chua index cua cac cau trong tung corpus random
###--> ??? random chon phan tu trong danh sach roi bo phan tu do ra hay co cach khac hay hon ???
#1.2. viet ham get_list_index_of_empty_line(merged_file) --> l[N] (voi Muc dich: biet cho nao ngat cau)
#
#Giai doan 2: Viet ham get_sentence_with_format_column(index)
#Lay dong co index = k
#if k == 0: lay tu dong 0-->l[0]-1 #day la chan duoi
#else: lay tu dong l[k-1]+1 --> l[k]-1
######################
#Giai doan 1: Lay du lieu ngau nhien tu corpus voi format column
#1.1. Cho so luong cau cua cac corpus --ham--> danh sach chua index cua cac cau trong tung corpus random
###--> ??? random chon phan tu trong danh sach roi bo phan tu do ra hay co cach khac hay hon ???
def get_random_index_of_sentences_for_train_dev_test(number_of_sentences_merged_file, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing):
    """
    Getting there data sets that contain random index of sentences of there corpus for training, developing and testing phase within given number of sentences in merged file.

    :type number_of_sentences_merged_file: int
    :param number_of_sentences_merged_file: number of sentences in merged file

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :rtype: there lists that contain random index of sentences of there corpus for training, developing and testing phase
    """
    if number_of_sentences_in_file_for_training + number_of_sentences_in_file_for_developing > number_of_sentences_merged_file:
        raise Exception("You should check the number for corpus!")

    #the number of sentences in merged file
    my_set = set(range(number_of_sentences_merged_file))
    num_for_training = number_of_sentences_in_file_for_training
    num_for_developing = number_of_sentences_in_file_for_developing
    num_for_testing = number_of_sentences_merged_file - number_of_sentences_in_file_for_training - number_of_sentences_in_file_for_developing

    list_index_training = []
    list_index_developing = []
    list_index_testing = []

    #print(my_set)

    while len(my_set) > 0:
        random_choice = random.choice(list(my_set))
        #print("random choice : %d" %random_choice)

        if num_for_training > 0:#training
            list_index_training.append(random_choice)
            num_for_training = num_for_training - 1
        elif num_for_developing > 0: #developing
            list_index_developing.append(random_choice)
            num_for_developing = num_for_developing - 1
        elif num_for_testing > 0:#testing
            list_index_testing.append(random_choice)
            num_for_testing = num_for_testing - 1
        #end if

        my_set.remove(random_choice)
    #end while

    print("So luong cac phan tu trong corpus de training, developing va testing la: %d, %d va %d" %(len(list_index_training), len(list_index_developing), len(list_index_testing)))

    return list_index_training, list_index_developing, list_index_testing
#**************************************************************************#
#1.2. viet ham get_list_index_of_empty_line(merged_file) --> l[N] (voi Muc dich: biet cho nao ngat cau)
def get_list_index_of_empty_line(file_input_path):
    """
    Getting list of index of empty line from given file within format column. Note: in file within format column, there is an empty line for separating sentences.

    :type file_input_path: string
    :param file_input_path: path to merged file that contains the features within format column

    :rtype: List of index of empty line from given file within format column.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open file for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    result = []
    current_index_sentence = 0

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            result.append(current_index_sentence)
        #end if

        current_index_sentence += 1
    #end for

    #close 2 files
    file_reader.close()

    return result
#**************************************************************************#
#Giai doan 2: Viet ham get_sentence_with_format_column(index)
#Lay dong co index = k
#if k == 0: lay tu dong 0-->l[0]-1 #day la chan duoi
#else: lay tu dong l[k-1]+1 --> l[k]-1
def get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, index_of_sentence, file_output_path):
    """
    Getting all the words of sentences in format-column file within given index of sentence.

    :type file_input_path: string
    :param file_input_path: path to merged file that contains the features within format column

    :type index_of_sentence: string
    :param index_of_sentence: given index of sentence

    :type file_output_path: string
    :param file_output_path: path of file that we could append data within given index of sentence

    :rtype: List of index of empty line from given file within format column.

    :raise ValueError: if any path is not existed
    """
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #vi du lieu moi lan chay se append nen can phai viet ham xoa file cu
    #delete_file_within_given_path(file_output_path)

    current_config = load_configuration()

    #get_list_index_of_empty_line(file_input_path)
    list_index_empty_line = get_list_index_of_empty_line(current_config.OUTPUT_MERGED_FEATURES)
    #print(list_index_empty_line)
    #print("The number of sentences in merged file is: %d" %len(list_index_empty_line))

    #for reading: file_input_path
    #file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#reading

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')#appending

    i_range = range(6) #init
    #get_line_given_number_of_sentence(file_input_path, number_of_sentence)
    #note: number_of_sentence = 1..n
    if index_of_sentence == 0:#lay tu dong 0-->l[0]-1 #day la chan duoi
        i_range = range(list_index_empty_line[0])
    else:#lay tu dong l[k-1]+1 --> l[k]-1
        i_range = range(list_index_empty_line[index_of_sentence-1]+1, list_index_empty_line[index_of_sentence])
    #end if

    for i in i_range:
        word_line = get_line_given_number_of_sentence(file_input_path, i + 1)
        file_writer.write(word_line.strip())
        file_writer.write("\n")
    #end for
    file_writer.write("\n") #ket thuc cau

    #close file
    #file_reader.close()
    file_writer.close()
#**************************************************************************#
#B2: Tao cac file dung cho qua trinh train; dev; test
#Tao du lieu random (Random Corpus for train, dev, test)
#remaining sentences in corpus is number_of_sentences_in_file_for_testing
def creating_random_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path,  number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing):
    """
    Generating the random corpus for training, developing and testing from merge file. Note: The number of sentences for training corpus is the remaining sentences.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type file_input_path: string
    :param file_input_path: path to merged file that contains all features

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed merged file that contains all features')
    """
    str_message_if_not_existed = "Not Existed file corpus input that contains all features ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    current_config = load_configuration()

    training_corpus_path = current_config.TRAIN_FILE_PATH + "_" + demo_name + ".txt"
    developing_corpus_path = current_config.DEV_FILE_PATH + "_" + demo_name + ".txt"
    testing_corpus_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    #vi du lieu moi lan chay se append nen can phai viet ham xoa file cu
    #delete_file_within_given_path(file_output_path)
    delete_file_within_given_path(training_corpus_path)
    delete_file_within_given_path(developing_corpus_path)
    delete_file_within_given_path(testing_corpus_path)

    #Giai doan 1: Lay du lieu ngau nhien tu corpus voi format column
    #1.1. Cho so luong cau cua cac corpus --ham--> danh sach chua index cua cac cau trong tung corpus random
    ###--> ??? random chon phan tu trong danh sach roi bo phan tu do ra hay co cach khac hay hon ???
    #1.2. viet ham get_list_index_of_empty_line(merged_file) --> l[N] (voi Muc dich: biet cho nao ngat cau)
    #
    #Giai doan 2: Viet ham get_sentence_with_format_column(index)
    #Lay dong co index = k
    #if k == 0: lay tu dong 0-->l[0]-1 #day la chan duoi
    #else: lay tu dong l[k-1]+1 --> l[k]-1

    number_of_sentences_merged_file = count_number_of_sentences_in_file_within_format_column(file_input_path)
    print("Number of sentences in merged file is: %d" %number_of_sentences_merged_file)

    #get random index list for training, developing and testing
    list_index_training, list_index_developing, list_index_testing = get_random_index_of_sentences_for_train_dev_test(number_of_sentences_merged_file, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)

    #get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, index_of_sentence, file_output_path)
    #training corpus
    for item in list_index_training:
        get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, item, training_corpus_path)

    #developing corpus
    for item in list_index_developing:
        get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, item, developing_corpus_path)

    #testing corpus
    for item in list_index_testing:
        get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, item, testing_corpus_path)
#**************************************************************************#
def generating_merged_features():
    """
    Generating merged features from files that are extracted in process "Extracting Features"
    """
    #Creating list of file paths
    list_of_file_paths = get_list_of_file_paths_not_included_nbestlist_and_asr() #within given labels
    #list_of_file_paths = get_list_of_file_paths_included_asr()
    #list_of_file_paths = get_list_of_file_paths_not_included_nbestlist_and_asr_within_our_labels #within our labels

    #Using command "paste" in order to merge lines in files
    current_config = load_configuration()
    merging_all_features(list_of_file_paths, current_config.OUTPUT_MERGED_FEATURES)
#**************************************************************************#
def generating_merged_features_within_given_list_of_file_paths(list_of_file_paths, file_output_path):
    """
    Generating merged features from files that are extracted in process "Extracting Features"
    """
    merging_all_features(list_of_file_paths, file_output_path)
#**************************************************************************#
#B1: Ket hop cac feature theo thu tu bang lenh "paste".
#Sau do chi du lieu thanh cac phan khac nhau: train, dev, test
#def merging_all_features(list_of_file_paths):
#moved to module "common_function_metrics"
#**************************************************************************#
def get_list_of_file_paths_not_included_nbestlist_and_asr_within_our_labels():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    if current_config.punctuation:
      list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    if current_config.stop_words:
      list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    if current_config.numeric:
      list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    if current_config.proper_name:
      list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    if current_config.unknown_lemma:
      list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    if current_config.occurence_words:
      list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    if current_config.occurence_stems:
      list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    if current_config.google_translator:
      list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    if current_config.bing_translator:
      list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    if current_config.label:
      list_of_file_paths.append( current_config.CONSTITUENT_LABEL)

    # Distance to Root
    if current_config.distance_to_root:
      list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    if current_config.polysemy_count_target:
      list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    if current_config.longest_ngram_length_tgt:
      list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    if current_config.backoff:
      list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)

    # Longest Source gram length
    if current_config.longest_ngram_length_src:
      list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    if current_config.alignments:
      list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    #list_of_file_paths.append( current_config.LABEL_OUTPUT)
    list_of_file_paths.append( current_config.LABEL_OUTPUT_TERCOM_WCE)



    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_for_ape_2015_version1():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    #list_of_file_paths.append( current_config.LABEL_OUTPUT)
    list_of_file_paths.append( current_config.LABEL_OUTPUT_TERCOM_APE)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_for_ape_within_extension_included_tag(extension):
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION + extension)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD + extension)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC + extension)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME + extension)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA + extension)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD + extension)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM + extension)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE + extension)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE + extension)

    # Constituent Label
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL + extension)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT + extension)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST + extension)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH + extension)

    # Backoff Behaviour
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR + extension)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET + extension)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES + extension)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    list_of_file_paths.append( current_config.LABEL_OUTPUT + extension)
    #list_of_file_paths.append( current_config.LABEL_OUTPUT_TERCOM_WCE)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_for_ape_2015():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    #list_of_file_paths.append( current_config.LABEL_OUTPUT)
    #list_of_file_paths.append( current_config.LABEL_OUTPUT_TERCOM_WCE)
    list_of_file_paths.append( current_config.LABEL_OUTPUT_TERCOM_APE)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_for_ape_within_given_dir_path(directory_path):
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( directory_path + get_filename(current_config.PUNCTUATION))

    # Stop Word
    list_of_file_paths.append( directory_path + get_filename(current_config.STOP_WORD))

    # Numeric
    list_of_file_paths.append( directory_path + get_filename(current_config.NUMERIC))

    # Proper Name
    list_of_file_paths.append(directory_path + get_filename(current_config.PROPER_NAME))

    # unknown lemma
    list_of_file_paths.append(directory_path + get_filename( current_config.UNKNOWN_LEMMA))

    # Number Of Occurrences word
    list_of_file_paths.append(directory_path + get_filename( current_config.NUMBER_OF_OCCURRENCES_WORD))

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append(directory_path + get_filename( current_config.NUMBER_OF_OCCURRENCES_STEM))

    # Occur in Google Translator
    list_of_file_paths.append(directory_path + get_filename( current_config.OCCUR_IN_GOOGLE_TRANSLATE ))

    # Occur in Bing Translator
    list_of_file_paths.append(directory_path + get_filename( current_config.OCCUR_IN_BING_TRANSLATE))

    # Constituent Label
    list_of_file_paths.append(directory_path + get_filename( current_config.CONSTITUENT_LABEL))

    # Distance to Root
    list_of_file_paths.append(directory_path + get_filename( current_config.DISTANCE_TO_ROOT ))

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append(directory_path + get_filename( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST ))

    # Longest Target gram length
    list_of_file_paths.append(directory_path + get_filename( current_config.LONGEST_TARGET_GRAM_LENGTH ))

    # Backoff Behaviour
    list_of_file_paths.append(directory_path + get_filename( current_config.BACKOFF_BEHAVIOUR))

    # Longest Source gram length
    list_of_file_paths.append(directory_path + get_filename( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET ))

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append(directory_path + get_filename( current_config.ALIGNMENT_FEATURES ))

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    #No having Label for test corpus
    # label of word Good/Bad
    #list_of_file_paths.append( current_config.LABEL_OUTPUT + extension)
    #list_of_file_paths.append( current_config.LABEL_OUTPUT_TERCOM_WCE)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_for_ape_within_extension(extension):
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION + extension)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD + extension)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC + extension)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME + extension)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA + extension)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD + extension)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM + extension)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE + extension)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE + extension)

    # Constituent Label
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL + extension)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT + extension)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST + extension)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH + extension)

    # Backoff Behaviour
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR + extension)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET + extension)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES + extension)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    """list_of_file_paths.append( current_config.LABEL_OUTPUT + extension)"""
    #list_of_file_paths.append( current_config.LABEL_OUTPUT_TERCOM_WCE)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_not_included_nbestlist_and_asr():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    list_of_file_paths.append( current_config.LABEL_OUTPUT)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_not_included_nbestlist_and_asr_all_numerics():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    #list_of_file_paths.append( current_config.CONSTITUENT_LABEL)
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL_AFTER_CONVERTING_TO_INT)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    #list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR_AFTER_CONVERTING_TO_INT)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    #list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES_AFTER_CONVERTING_TO_INT)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    #for using PCA nen khong dung Label
    # label of word Good/Bad
    #list_of_file_paths.append( current_config.LABEL_OUTPUT)

    return list_of_file_paths
#**************************************************************************#
def split_file_after_PCA_to_format_column(file_input_path, file_ref_path, file_output_path):
    #for reading: file_input_path
    file_reader = open(file_ref_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    number_of_sentence = 1

    for line in file_reader:
        line = line.strip()

        line_content = get_line_given_number_of_sentence(file_input_path, number_of_sentence)
        line_content = line_content.strip()

        if len(line) == 0:
            file_writer.write("\n")
            continue
        #end if

        str_output = line_content
        file_writer.write(str_output + "\n")

        number_of_sentence += 1
    #end for

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def get_list_of_file_paths_not_included_nbestlist_and_asr_all_numerics_after_PCA():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    #list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    #list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    #list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    #list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    #list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    #list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    #list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    #list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    #list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    #list_of_file_paths.append( current_config.CONSTITUENT_LABEL)
    #list_of_file_paths.append( current_config.CONSTITUENT_LABEL_AFTER_CONVERTING_TO_INT)

    # Distance to Root
    #list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    #list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    #list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)
    #list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR_AFTER_CONVERTING_TO_INT)

    # Longest Source gram length
    #list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    #list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)
    #list_of_file_paths.append( current_config.ALIGNMENT_FEATURES_AFTER_CONVERTING_TO_INT)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    ##chuyen format pca thanh format column duoc phan chia boi 1 dong trong
    list_of_file_paths.append( current_config.OUTPUT_MERGED_FEATURES_WMT15_AFTER_PCA_LAST)
    #list_of_file_paths.append( current_config.OUTPUT_MERGED_FEATURES_WMT15_AFTER_CONVERTING_TO_INT) #de test voi int ban dau, truoc khi dung PCA

    #for using PCA nen khong dung Label
    # label of word Good/Bad
    list_of_file_paths.append( current_config.LABEL_OUTPUT)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_not_included_nbestlist_and_asr_all_numerics_for_wmt15():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    #list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    #list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    #list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    #list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    #list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    #list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    #list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    #list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    #list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    #list_of_file_paths.append( current_config.CONSTITUENT_LABEL)
    #list_of_file_paths.append( current_config.CONSTITUENT_LABEL_AFTER_CONVERTING_TO_INT)

    # Distance to Root
    #list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    #list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    #list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)
    #list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR_AFTER_CONVERTING_TO_INT)

    # Longest Source gram length
    #list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    #list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)
    #list_of_file_paths.append( current_config.ALIGNMENT_FEATURES_AFTER_CONVERTING_TO_INT)

    # WPP Exact
    #list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    #list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    ##chuyen format pca thanh format column duoc phan chia boi 1 dong trong
    #list_of_file_paths.append( current_config.OUTPUT_MERGED_FEATURES_WMT15_AFTER_PCA_LAST)
    list_of_file_paths.append( current_config.OUTPUT_MERGED_FEATURES_WMT15_AFTER_CONVERTING_TO_INT) #de test voi int ban dau, truoc khi dung PCA

    #for using PCA nen khong dung Label
    # label of word Good/Bad
    list_of_file_paths.append( current_config.LABEL_OUTPUT)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_included_asr():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)

    # WPP Exact
    list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    list_of_file_paths.append( current_config.LABEL_OUTPUT)

    return list_of_file_paths
#**************************************************************************#
def get_list_of_file_paths_included_nbestlist_not_asr():
    """
    Creating list of file paths that are extracted in process "Extracting Features"
    """
    current_config = load_configuration()
    list_of_file_paths = []

    #Order of the files ~ Order of the features FOR Merging features
    # Punctuation
    list_of_file_paths.append( current_config.PUNCTUATION)

    # Stop Word
    list_of_file_paths.append( current_config.STOP_WORD)

    # Numeric
    list_of_file_paths.append( current_config.NUMERIC)

    # Proper Name
    list_of_file_paths.append( current_config.PROPER_NAME)

    # unknown lemma
    list_of_file_paths.append( current_config.UNKNOWN_LEMMA)

    # Number Of Occurrences word
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_WORD)

    # Number of occurrences stem (frequency of stemmed word)
    list_of_file_paths.append( current_config.NUMBER_OF_OCCURRENCES_STEM)

    # Occur in Google Translator
    list_of_file_paths.append( current_config.OCCUR_IN_GOOGLE_TRANSLATE)

    # Occur in Bing Translator
    list_of_file_paths.append( current_config.OCCUR_IN_BING_TRANSLATE)

    # Constituent Label
    list_of_file_paths.append( current_config.CONSTITUENT_LABEL)

    # Distance to Root
    list_of_file_paths.append( current_config.DISTANCE_TO_ROOT)

    # Polysemy Count - Target POLYSEMY_COUNT_TARGET --> BABEL_NET_OUTPUT_CORPUS_EN_LAST
    #for spanish - target
    #list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    list_of_file_paths.append( current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    # Longest Target gram length
    list_of_file_paths.append( current_config.LONGEST_TARGET_GRAM_LENGTH)

    # Backoff Behaviour
    list_of_file_paths.append( current_config.BACKOFF_BEHAVIOUR)

    # Longest Source gram length
    list_of_file_paths.append( current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    # alignment_features : 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
    list_of_file_paths.append( current_config.ALIGNMENT_FEATURES)

    # WPP Exact
    list_of_file_paths.append( current_config.WPP_EXACT)

    # Chu y: trong file nay column dau tien la word cua Target Language
    # WPP any
    # Nodes
    # Min
    # Max
    list_of_file_paths.append( current_config.WPP_NODES_MIN_MAX)

    # Features' values ASR: les        0.509947        -4.38473        1        0        0        0.48        DET:ART
    # word
    # Post posterior
    # LM probability
    # order of n-gram
    # Use context
    # backoff score
    # length of frame (ton may giay cho tu nay)
    # POS
    #list_of_file_paths.append( current_config.FEATURES_ASR_ALIGNED_LAST)

    # label of word Good/Bad
    list_of_file_paths.append( current_config.LABEL_OUTPUT)

    return list_of_file_paths
#**************************************************************************#
class Feature_Name_And_Path(object):
    """
    This class contains the following information: feature name & feature-template path.
    """
    def __init__(self):
        self.feature_name = ""
        self.template_path = ""
        self.is_removed = False

    def __init__(self, feature_name, template_path):
        self.feature_name = feature_name
        self.template_path = template_path
        self.is_removed = False

    #set
    def set_feature_name(self, feature_name = ""):
        self.feature_name = feature_name

    def set_template_path(self, template_path=""):
        self.template_path = template_path

    def set_is_removed(self, is_removed = True):
        self.is_removed = is_removed

    #get
    def get_feature_name(self):
        return self.feature_name

    def get_template_path(self):
        return self.template_path

    def get_is_removed(self):
        return self.is_removed

    #operator overloadding ref: https://docs.python.org/3.4/library/operator.html
    def __eq__(self, other):
        if self.feature_name == other.get_template_path():
            return True
        else:
            return False

    #methods
    def is_same_feature_name(self, feature_name):
        """
        Checking whether feature_name is the same with given string input. True if existed; False otherwise.
        """
        if self.feature_name == feature_name:
            return True
        else:
            return False

    def remove_feature_name(self, feature_name):
        """
        Removing feature name that is the 'weak' feature.
        """
        if self.feature_name == feature_name:
            self.set_is_removed(True)
            return True #Deleted successfully
        else:
            return False #Deleted unsuccessfully

#**************************************************************************#
class Subset_Feature(object):
    """
    This class contains the following information: subset (subset is the list that contains all instances  Feature_Name_And_Path of words), threshold_good, F_avg, tham so lien quan (Pr_bad, Rc_bad, F_bad & Pr_good, Rc_good, F_good)
    """
    def __init__(self):
        self.subset = []
        self.threshold_good =  -1.0
        self.F_avg = -1.0
        self.Pr_bad = -1.0
        self.Rc_bad =  -1.0
        self.F_bad =  -1.0
        self.Pr_good =  -1.0
        self.Rc_good =  -1.0
        self.F_good =  -1.0

    def __init__(self, subset, threshold_good =  -1.0, F_avg =  -1.0, Pr_bad =  -1.0, Rc_bad =  -1.0, F_bad = -1.0, Pr_good =  -1.0, Rc_good = -1.0, F_good = -1.0):
        self.threshold_good = threshold_good
        self.F_avg = F_avg
        self.Pr_bad = Pr_bad
        self.Rc_bad = Rc_bad
        self.F_bad = F_bad
        self.Pr_good = Pr_good
        self.Rc_good = Rc_good
        self.F_good = F_good
        self.subset = []

        if len(subset) == 0:
            self.subset = []
        else:
            for item in subset:
                obj = Feature_Name_And_Path(item.get_feature_name(), item.get_template_path())
                self.subset.append(obj)
            #end for
    #end def

    #set
    def set_threshold_good(self, threshold_good = -1.0):
        self.threshold_good = threshold_good

    def set_F_avg(self, F_avg = -1.0):
        self.F_avg = F_avg

    def set_Pr_bad(self, Pr_bad = -1.0):
        self.Pr_bad = Pr_bad

    def set_Rc_bad(self, Rc_bad = -1.0):
        self.Rc_bad = Rc_bad

    def set_F_bad(self, F_bad = -1.0):
        self.F_bad = F_bad

    def set_Pr_good(self, Pr_good = -1.0):
        self.Pr_good = Pr_good

    def set_Rc_good(self, Rc_good = -1.0):
        self.Rc_good = Rc_good

    def set_F_good(self, F_good = -1.0):
        self.F_good = F_good

    def set_subset(self, subset):
        if len(subset) == 0:
            self.subset = []
        else:
            for item in subset:
                obj = Feature_Name_And_Path(item.get_feature_name(), item.get_template_path())
                self.subset.append(obj)
            #end for

    #get
    def get_threshold_good(self):
        return self.threshold_good

    def get_F_avg(self):
        return self.F_avg

    def get_Pr_bad(self):
        return self.Pr_bad

    def get_Rc_bad(self):
        return self.Rc_bad

    def get_F_bad(self):
        return self.F_bad

    def get_Pr_good(self):
        return self.Pr_good

    def get_Rc_good(self):
        return self.Rc_good

    def get_F_good(self):
        return self.F_good

    def get_subset(self):
        return self.subset

    #methods
    def get_list_paths(self):
        """
        Getting list of paths of all feature-template path in subset.
        """
        result = []
        for item in self.subset:
            path = item.get_template_path()
            result.append(path)
        #end for

        return result

    def get_list_feature_names(self):
        """
        Getting list of features' names of all feature-template path in subset.
        """
        result = []
        for item in self.subset:
            f_name = item.get_feature_name()
            result.append(f_name)
        #end for

        return result

    #operator overloadding : >; ref: https://docs.python.org/3.4/library/operator.html
    def __gt__(self, other):
        if self.F_avg > other.get_F_avg():
            return True
        else:
            return False
        #end if
    #end def
#**************************************************************************#
def init_all_feature_names_and_path_to_templates():
    """
    Getting list of all of features' names and paths to templates.

    :rtype: list of instances Feature_Name_And_Path
    """

    lst = []
    current_config = load_configuration()
    """
    feature_name = current_config.ALIGNMENT_FEATURES_NAME
    template_path = current_config.ALIGNMENT_FEATURES_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))
    """
    feature_name = current_config.ALIGNMENT_CONTEXT_POS_NAME
    template_path = current_config.ALIGNMENT_CONTEXT_POS_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.ALIGNMENT_CONTEXT_STEM_NAME
    template_path = current_config.ALIGNMENT_CONTEXT_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.ALIGNMENT_CONTEXT_WORD_NAME
    template_path = current_config.ALIGNMENT_CONTEXT_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.SOURCE_POS_NAME
    template_path = current_config.SOURCE_POS_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.SOURCE_STEM_NAME
    template_path = current_config.SOURCE_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.SOURCE_WORD_NAME
    template_path = current_config.SOURCE_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.TARGET_POS_NAME
    template_path = current_config.TARGET_POS_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.TARGET_STEM_NAME
    template_path = current_config.TARGET_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.TARGET_WORD_NAME
    template_path = current_config.TARGET_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.BACKOFF_BEHAVIOUR_NAME
    template_path = current_config.BACKOFF_BEHAVIOUR_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.CONSTITUENT_LABEL_NAME
    template_path = current_config.CONSTITUENT_LABEL_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.DISTANCE_TO_ROOT_NAME
    template_path = current_config.DISTANCE_TO_ROOT_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.LONGEST_SOURCE_GRAM_LENGTH_NAME
    template_path = current_config.LONGEST_SOURCE_GRAM_LENGTH_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.LONGEST_TARGET_GRAM_LENGTH_NAME
    template_path = current_config.LONGEST_TARGET_GRAM_LENGTH_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.MAX_EN_NAME
    template_path = current_config.MAX_EN_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.MIN_EN_NAME
    template_path = current_config.MIN_EN_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NODES_NAME
    template_path = current_config.NODES_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NUMBER_OF_OCCURRENCES_STEM_NAME
    template_path = current_config.NUMBER_OF_OCCURRENCES_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NUMBER_OF_OCCURRENCES_WORD_NAME
    template_path = current_config.NUMBER_OF_OCCURRENCES_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NUMERIC_NAME
    template_path = current_config.NUMERIC_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.OCCUR_IN_BING_TRANSLATOR_NAME
    template_path = current_config.OCCUR_IN_BING_TRANSLATOR_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.OCCUR_IN_GOOGLE_TRANSLATOR_NAME
    template_path = current_config.OCCUR_IN_GOOGLE_TRANSLATOR_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.POLYSEMYCOUNT_TARGET_NAME
    template_path = current_config.POLYSEMYCOUNT_TARGET_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.PROPER_NAME_NAME
    template_path = current_config.PROPER_NAME_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.PUNCTUATION_NAME
    template_path = current_config.PUNCTUATION_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.STOP_WORD_NAME
    template_path = current_config.STOP_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.UNKNOWN_LEMMA_NAME
    template_path = current_config.UNKNOWN_LEMMA_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.WPP_ANY_NAME
    template_path = current_config.WPP_ANY_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.WPP_EXACT_NAME
    template_path = current_config.WPP_EXACT_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    """
    #dao nguoc lai danh sach khoi tao --> de kiem chung hien tuong
    #Tat ca cac thuoc tinh dang sau bi sap xep hang duoi ???
    result = []
    n_length_lst = len(lst)

    while n_length_lst >= 1:
        result.append(lst[n_length_lst-1])

        n_length_lst = n_length_lst - 1
    #end while

    return result
    """

    return lst
#**************************************************************************#
#F2: top 20 features
"""
No        Feature name
1        alignment context pos
2        alignment context stem
3        alignment context word
4        source pos
5        source stem
6        source word
7        target pos
8        target stem
9        target word
10        backoff behaviour
11        constituent label
12        distance to root
13        longest source gram length
14        longest target gram length
15        max
16        min
17        nodes
18        number of occurrences stem
19        number of occurrences word
20        numeric
21        occur in bing translator
22        occur in google translator
23        polysemycount target
24        proper namee
25        punctuation
26        stop word
27        unknown lemma
28        wpp any
29        wpp exact
"""
def top_20_feature_names_and_path_to_templates():
    """
    Getting list of all of features' names and paths to templates.

    :rtype: list of instances Feature_Name_And_Path
    """

    lst = []
    current_config = load_configuration()
    """
    feature_name = current_config.ALIGNMENT_FEATURES_NAME
    template_path = current_config.ALIGNMENT_FEATURES_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))
    """
    feature_name = current_config.ALIGNMENT_CONTEXT_POS_NAME
    template_path = current_config.ALIGNMENT_CONTEXT_POS_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.ALIGNMENT_CONTEXT_STEM_NAME
    template_path = current_config.ALIGNMENT_CONTEXT_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.ALIGNMENT_CONTEXT_WORD_NAME
    template_path = current_config.ALIGNMENT_CONTEXT_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.SOURCE_POS_NAME
    template_path = current_config.SOURCE_POS_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.SOURCE_STEM_NAME
    template_path = current_config.SOURCE_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.SOURCE_WORD_NAME
    template_path = current_config.SOURCE_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.TARGET_POS_NAME
    template_path = current_config.TARGET_POS_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.TARGET_STEM_NAME
    template_path = current_config.TARGET_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.TARGET_WORD_NAME
    template_path = current_config.TARGET_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.BACKOFF_BEHAVIOUR_NAME
    template_path = current_config.BACKOFF_BEHAVIOUR_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.CONSTITUENT_LABEL_NAME
    template_path = current_config.CONSTITUENT_LABEL_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.DISTANCE_TO_ROOT_NAME
    template_path = current_config.DISTANCE_TO_ROOT_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.LONGEST_SOURCE_GRAM_LENGTH_NAME
    template_path = current_config.LONGEST_SOURCE_GRAM_LENGTH_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.LONGEST_TARGET_GRAM_LENGTH_NAME
    template_path = current_config.LONGEST_TARGET_GRAM_LENGTH_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.MAX_EN_NAME
    template_path = current_config.MAX_EN_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.MIN_EN_NAME
    template_path = current_config.MIN_EN_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NODES_NAME
    template_path = current_config.NODES_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NUMBER_OF_OCCURRENCES_STEM_NAME
    template_path = current_config.NUMBER_OF_OCCURRENCES_STEM_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NUMBER_OF_OCCURRENCES_WORD_NAME
    template_path = current_config.NUMBER_OF_OCCURRENCES_WORD_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    feature_name = current_config.NUMERIC_NAME
    template_path = current_config.NUMERIC_PATH
    lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.OCCUR_IN_BING_TRANSLATOR_NAME
    #template_path = current_config.OCCUR_IN_BING_TRANSLATOR_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.OCCUR_IN_GOOGLE_TRANSLATOR_NAME
    #template_path = current_config.OCCUR_IN_GOOGLE_TRANSLATOR_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.POLYSEMYCOUNT_TARGET_NAME
    #template_path = current_config.POLYSEMYCOUNT_TARGET_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.PROPER_NAME_NAME
    #template_path = current_config.PROPER_NAME_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.PUNCTUATION_NAME
    #template_path = current_config.PUNCTUATION_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.STOP_WORD_NAME
    #template_path = current_config.STOP_WORD_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.UNKNOWN_LEMMA_NAME
    #template_path = current_config.UNKNOWN_LEMMA_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.WPP_ANY_NAME
    #template_path = current_config.WPP_ANY_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    #feature_name = current_config.WPP_EXACT_NAME
    #template_path = current_config.WPP_EXACT_PATH
    #lst.append(Feature_Name_And_Path(feature_name, template_path))

    return lst
#**************************************************************************#
def creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, order_n_fold, number_of_sentences_in_n_fold_testing_set, number_of_sentences_in_file_for_developing):
    """
    Generating the random corpus for training, developing and testing from merge file. Note: The number of sentences for training corpus is the remaining sentences.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type file_input_path: string
    :param file_input_path: path to merged file that contains all features

    :type order_n_fold: int
    :param order_n_fold: order of fold

    :type number_of_sentences_in_n_fold_testing_set: string
    :param number_of_sentences_in_n_fold_testing_set: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed merged file that contains all features')

    current_config = load_configuration()

    training_corpus_path = current_config.TRAIN_FILE_PATH + "_" + demo_name + ".txt"
    developing_corpus_path = current_config.DEV_FILE_PATH + "_" + demo_name + ".txt"
    testing_corpus_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    #vi du lieu moi lan chay se append nen can phai viet ham xoa file cu
    #delete_file_within_given_path(file_output_path)
    delete_file_within_given_path(training_corpus_path)
    delete_file_within_given_path(developing_corpus_path)
    delete_file_within_given_path(testing_corpus_path)

    #Giai doan 1: Lay du lieu ngau nhien tu corpus voi format column
    #1.1. Cho so luong cau cua cac corpus --ham--> danh sach chua index cua cac cau trong tung corpus random
    ###--> ??? random chon phan tu trong danh sach roi bo phan tu do ra hay co cach khac hay hon ???
    #1.2. viet ham get_list_index_of_empty_line(merged_file) --> l[N] (voi Muc dich: biet cho nao ngat cau)
    #
    #Giai doan 2: Viet ham get_sentence_with_format_column(index)
    #Lay dong co index = k
    #if k == 0: lay tu dong 0-->l[0]-1 #day la chan duoi
    #else: lay tu dong l[k-1]+1 --> l[k]-1

    number_of_sentences_merged_file = count_number_of_sentences_in_file_within_format_column(file_input_path)
    print("Number of sentences in merged file is: %d" %number_of_sentences_merged_file)

    #get random index list for training, developing and testing
    #list_index_training, list_index_developing, list_index_testing = get_random_index_of_sentences_for_train_dev_test(number_of_sentences_merged_file, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    list_index_training, list_index_developing, list_index_testing = get_n_fold_cross_validation_index_of_sentences_for_train_dev_test(order_n_fold, number_of_sentences_merged_file, number_of_sentences_in_n_fold_testing_set, number_of_sentences_in_file_for_developing)

    #get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, index_of_sentence, file_output_path)
    #training corpus
    for item in list_index_training:
        get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, item, training_corpus_path)

    #developing corpus
    for item in list_index_developing:
        get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, item, developing_corpus_path)

    #testing corpus
    for item in list_index_testing:
        get_file_containing_sentence_given_index_sentence_from_merged_file(file_input_path, item, testing_corpus_path)

#**************************************************************************#
def get_n_fold_cross_validation_index_of_sentences_for_train_dev_test(order_n_fold, number_of_sentences_merged_file, number_of_sentences_in_n_fold_testing_set, number_of_sentences_in_file_for_developing):
    """
    Getting there data sets that contain random index of sentences of there corpus for training, developing and testing phase within given number of sentences in merged file.

    :type order_n_fold: int
    :param order_n_fold: the order of n-fold, this number >= 1

    :type number_of_sentences_merged_file: int
    :param number_of_sentences_merged_file: number of sentences in merged file

    :type number_of_sentences_in_n_fold_testing_set: string
    :param number_of_sentences_in_n_fold_testing_set: the number of sentences for testing corpus in n-fold (cross validation)

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :rtype: there lists that contain cross validation data within index of sentences of there corpus for training, developing and testing phase
    """
    if number_of_sentences_in_n_fold_testing_set + number_of_sentences_in_file_for_developing > number_of_sentences_merged_file:
        raise Exception("You should check the number for corpus!")

    #the number of sentences in merged file
    my_set = set(range(number_of_sentences_merged_file))
    num_for_testing = number_of_sentences_in_n_fold_testing_set
    num_for_developing = number_of_sentences_in_file_for_developing
    num_for_training = number_of_sentences_merged_file - number_of_sentences_in_n_fold_testing_set - number_of_sentences_in_file_for_developing

    list_index_training = []
    list_index_developing = []
    list_index_testing = []

    #print(my_set)
    #cong thuc tong quat
    #neu training set chua l dong, thi o fold thu k co dang tong quat sau:
    #l*(k-1) --> l*k-1

    if num_for_testing*order_n_fold - 1 >= number_of_sentences_merged_file:
        raise Exception("You should check number of sentences in n-fold OR order of n-fold.")
    #end if

    #B1: chon ra duoc list_index_testing
    #de lay het du lieu testing thi co khi so le nen can phai cho sai so delta = 10
    #vi khi chia 10881 cho 10 folds thi du 1 cau --> can phai lay cau nay dua vao test --> Dung delta de: Neu tong so cau - (num_for_testing*order_n_fold - 1) >= delta thi gan index_end = number_of_sentences_merged_file
    current_config = load_configuration()
    delta = current_config.DELTA
    if num_for_testing*order_n_fold >= number_of_sentences_merged_file:
        index_end = number_of_sentences_merged_file - 1
    elif number_of_sentences_merged_file - num_for_testing*order_n_fold - 1 <= delta:
        index_end = number_of_sentences_merged_file - 1
    else:
        index_end = num_for_testing*order_n_fold - 1

    index_start = num_for_testing*(order_n_fold - 1)

    if index_start >= index_end:
        print("index_start = %d" %index_start)
        print("index_end = %d" %index_end)
        raise Exception("You should check number of sentences in n-fold OR order of n-fold. ERROR: index start & index end.")
    #end if

    while index_start <= index_end:
        list_index_testing.append(index_start)
        my_set.remove(index_start)
        index_start = index_start + 1
    #end while

    #B2: list_index_developing (random choice) _ o version nay thi dev = 0
    #B3: con lai la training
    for item in my_set:
        list_index_training.append(item)
    #end for
    """
    while len(my_set) > 0:
        random_choice = random.choice(list(my_set))

        if num_for_developing > 0:
            list_index_developing.append(random_choice)
            num_for_developing = num_for_developing - 1
        elif num_for_training > 0:
            list_index_training.append(random_choice)
            num_for_training = num_for_training - 1
        #end if

        my_set.remove(random_choice)
    #end while
    """
    """random_choice
    while len(my_set) > 0:
        random_choice = random.choice(list(my_set))
        #print("random choice : %d" %random_choice)

        if num_for_training > 0:#training
            list_index_training.append(random_choice)
            num_for_training = num_for_training - 1
        elif num_for_developing > 0: #developing
            list_index_developing.append(random_choice)
            num_for_developing = num_for_developing - 1
        elif num_for_testing > 0:#testing
            list_index_testing.append(random_choice)
            num_for_testing = num_for_testing - 1
        #end if

        my_set.remove(random_choice)
    #end while
    """

    print("So luong cac phan tu trong corpus de training, developing va testing la: %d, %d va %d" %(len(list_index_training), len(list_index_developing), len(list_index_testing)))

    return list_index_training, list_index_developing, list_index_testing
#**************************************************************************#
def is_existed_file(file_input_path, str_message_if_not_existed):
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError(str_message_if_not_existed)
#**************************************************************************#
def is_already_existed_file(file_input_path, str_message_if_existed):
    #check existed paths
    if os.path.exists(file_input_path):
        raise TypeError(str_message_if_existed)
def warning_already_existed_file(file_input_path, str_message_if_existed):
    #check existed paths
    if os.path.exists(file_input_path):
        print (str_message_if_existed)
def delete_already_existed_file(file_input_path, str_message_if_existed):
    #check existed paths
    if os.path.exists(file_input_path):
        os.remove(file_input_path)
        print (str_message_if_existed)
    #end if
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#/home/lent/Develops/Solution/tool/moses/scripts/training/train-model.perl -corpus /home/lent/Develops/Solution/tool/moses_test/corpus/output_preprocessing -f src -e tgt -alignment grow-diag-final-and --first-step 1 --last-step 3 --external-bin-dir=/home/lent/Develops/Solution/tool/giza-pp/bin --model-dir=/home/lent/Develops/Solution/tool/moses_test/word_alignment
def get_file_alignments_target_to_source_word_alignment_using_moses(pattern_file_path, extension_source, extension_target, path_to_tool_giza, output_directory_path, file_output_path):
    """
    Creating file of alignment word to word from Target To Source. Output has the format like n-best-list of tool MOSES
    #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
    =============================================================

    :type pattern_file_path: string
    :param pattern_file_path: the path of pattern corpus for tool MOSES

    :type extension_source: string
    :param extension_source: Ex: src/en

    :type extension_target: string
    :param extension_target: Ex: tgt/es

    :type path_to_tool_giza: string
    :param path_to_tool_giza: the path of directory GIZA_bin

    :type output_directory_path: string
    :param output_directory_path: the path of directory output of word alignment

    :rtype: list of alignment word to word from Target to Source, Note: if value = '' then value=-1 that means there is no word in Source language associated.
    """
    #current_config = load_configuration()
    config_end_user = load_config_end_user()

    command_line = "perl " #Path to the shell script TreeeTagger
    script_path = config_end_user.TOOL_TRAIN_MODEL

    #command_line = command_line + script_path + " -corpus "+ current_config.PATTERN_REF_TEST_FORMAT_ROW + " -f "+ current_config.EXTENSION_SOURCE +" -e "+ current_config.EXTENSION_TARGET + " -alignment grow-diag-final-and --first-step 1 --last-step 3 --external-bin-dir="+ config_end_user.PATH_TO_TOOL_GIZA +" --model-dir=" + current_config.MODEL_DIR_PATH
    command_line = command_line + script_path + " -corpus "+ pattern_file_path + " -f "+ extension_source +" -e "+ extension_target + " -alignment grow-diag-final-and --first-step 1 --last-step 3 --external-bin-dir="+ path_to_tool_giza +" --model-dir=" + output_directory_path

    print(command_line)

    #rm -rf corpus/ giza.src-tgt/ giza.tgt-src/
    current_config = load_configuration()

    list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)

    command_line = "rm -rf corpus/ giza.src-tgt/ giza.tgt-src/"
    list_of_commands.append(command_line)

    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)

    #Run Script
    #call_script(command_line, script_path)

    file_alignment_source_target_path = output_directory_path + "/" + "aligned.grow-diag-final-and"

    file_target_path = pattern_file_path + "." + extension_target

    print("file_alignment_source_target_path-BEGIN")
    print(file_alignment_source_target_path)
    print("file_alignment_source_target_path-END")

    print("file_target_path-BEGIN")
    print(file_target_path)
    print("file_target_path-END")

    #check existed paths
    """
    if not os.path.exists(file_alignment_source_target_path):
        raise TypeError('You should check tool MOSES from step 1 to step 3')

    if not os.path.exists(file_target_path):
        raise TypeError('You should check file target source in path: %s' %file_target_path)
    """
    str_message_if_not_existed = "You should check tool MOSES from step 1 to step 3"
    is_existed_file(file_alignment_source_target_path, str_message_if_not_existed)

    str_message_if_not_existed = "You should check file target source in path: " + file_target_path
    is_existed_file(file_target_path, str_message_if_not_existed)

    #for reading: file_input_path
    file_reader = open(file_alignment_source_target_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    num_of_sent = 0
    str_delimiter = " ||| "

    #Tao file output giong nhu format cua output MOSES
    #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
    for alignment_source_target in file_reader:
        alignment_source_target = alignment_source_target.strip()

        if len(alignment_source_target) == 0:
            continue
        #end if

        line_target = get_line_given_number_of_sentence(file_target_path, num_of_sent + 1)

        str_output = str(num_of_sent) + str_delimiter + line_target.strip() + str_delimiter + alignment_source_target

        file_writer.write(str_output + "\n")

        num_of_sent += 1
    #end for

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
#path_to_moses -f path_to_moses_ini -include-segmentation-in-n-best -print-alignment-info-in-n-best -n-best-list output_nbestlist_included_alignment_path N < input_path > mt_output_path
def create_n_best_list_by_moses( file_input_path, path_to_moses_ini, N_in_nbestlist, output_nbestlist_included_alignment_path, mt_output_path ):
    """
    Converting the format row to format column

    :type file_input_path: string
    :param file_input_path: contains corpus with format row

    :type path_to_moses_ini: string
    :param path_to_moses_ini: path of file "moses.ini"

    :type N_in_nbestlist: int
    :param N_in_nbestlist: the number of hypothesis sentences in n-best-list (Default: 1)

    :type output_nbestlist_included_alignment_path: string
    :param output_nbestlist_included_alignment_path: the ouput from moses best_n_list included alignment SOURCE to TARGET

    :type file_output_path: string
    :param file_output_path: contains hypothesis sentences from Machine Translation

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    if not os.path.exists(path_to_moses_ini):
        raise TypeError('Not Existed file moses.ini')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file path_to_moses_ini ("+path_to_moses_ini+")"
    is_existed_file(path_to_moses_ini, str_message_if_not_existed)

    #path_to_moses -f path_to_moses_ini -include-segmentation-in-n-best -print-alignment-info-in-n-best -n-best-list output_nbestlist_included_alignment_path N < input_path > mt_output_path
    current_config = load_configuration()

    #using tool MOSES in order to generate n-best-list
    path_script = current_config.TOOL_MOSES #Path to the MOSES Tool

    #change mode execute script
    #run_chmod(path_script)

    command_line = path_script + " -f " + path_to_moses_ini + " -include-segmentation-in-n-best -print-alignment-info-in-n-best -n-best-list " + output_nbestlist_included_alignment_path + " " + str(N_in_nbestlist) + " < " + file_input_path + " > " + mt_output_path

    #print(command_line)

    #Khong chay duoc dung dung cu phap
    #call_script(command_line, path_to_script)
    #call_script(command_line, current_config.TOOL_MOSES)

    #chuyen sang cach khac

    #change quyen execute cho tool moses
    run_chmod(current_config.TOOL_MOSES)

    #generate shell script, roi goi lenh chay script
    #generate shell script
    list_of_commands = []

    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #goi lenh chay
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
#B1: creating "Input format" for tool "fast_align"
#Input to `fast_align` must be tokenized and aligned into parallel sentences. Each line is a source language sentence and its target language translation, separated by a triple pipe symbol with leading and trailing white space (` ||| `). An example 3-sentence German–English parallel corpus is:
#doch jetzt ist der Held gefallen . ||| but now the hero has fallen .

#B2: *source–target*
#./fast_align -i text.fr-en -d -o -v > forward.align

#*target–source* alignments is to just add the `-r` (“reverse”) option
#./fast_align -i text.fr-en -d -o -v -r > reverse.align

#Output: `fast_align` produces outputs in the widely-used `i-j` “Pharaoh format,” where a pair `i-j` indicates that the <i>i</i>th word (zero-indexed) of the left language (by convention, the *source* language) is aligned to the <i>j</i>th word of the right sentence (by convention, the *target* language). For example, a good alignment of the above German–English corpus would be:
def creating_input_format_for_tool_fast_align(file_input_source_language_path, file_input_target_language_path, file_output_path):
    """
    Creating "Input format" for tool "fast_align"

    Input to `fast_align` must be tokenized and aligned into parallel sentences. Each line is a source language sentence and its target language translation, separated by a triple pipe symbol with leading and trailing white space (` ||| `). An example 3-sentence German–English parallel corpus is:
        doch jetzt ist der Held gefallen . ||| but now the hero has fallen .

    :type file_input_source_language_path: string
    :param file_input_source_language_path: the path of corpus source language

    :type file_input_target_language_path: string
    :param file_input_target_language_path: the path of corpus target language

    :type file_output_path: string
    :param file_output_path: the path of output-file

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_source_language_path):
        raise TypeError('Not Existed file corpus source language')

    if not os.path.exists(file_input_target_language_path):
        raise TypeError('Not Existed file corpus target language')
    """
    str_message_if_not_existed = "Not Existed file corpus input - file_input_source_language_path ("+file_input_source_language_path+")"
    is_existed_file(file_input_source_language_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file corpus input - file_input_target_language_path ("+file_input_target_language_path+")"
    is_existed_file(file_input_target_language_path, str_message_if_not_existed)

    str_delimiter = " ||| "

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_source_language_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    current_number_of_sentence = 1

    for line in file_reader:
        line = line.strip()

        if len(line) == 0:
            continue
        #end if

        line_file_input_target_language = get_line_given_number_of_sentence(file_input_target_language_path, current_number_of_sentence)
        line_file_input_target_language = line_file_input_target_language.strip()

        str_output = line + str_delimiter + line_file_input_target_language

        file_writer.write(str_output + "\n")

        current_number_of_sentence += 1
    #end for

    #close files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def get_word_alignment_using_tool_fast_align(file_input_path, file_output_alignment_source_to_target_path, file_output_alignment_target_to_source_path):
    """
    Getting word alignment by using tool "fast_align"

    Input to `fast_align` must be tokenized and aligned into parallel sentences. Each line is a source language sentence and its target language translation, separated by a triple pipe symbol with leading and trailing white space (` ||| `). An example 3-sentence German–English parallel corpus is:
        doch jetzt ist der Held gefallen . ||| but now the hero has fallen .

    :type file_input_path: string
    :param file_input_path: the path of input corpus

    :type file_output_alignment_source_to_target_path: string
    :param file_output_alignment_source_to_target_path: the path of output-file that contains alignments Source to Target

    :type file_output_alignment_target_to_source_path: string
    :param file_output_alignment_target_to_source_path: the path of output-file that contains alignments Target to Source

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file input corpus for tool fast-align')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    """
fast_align generates asymmetric alignments (i.e., by treating either the left or right language in the parallel corpus as primary language being modeled, slightly different alignments will be generated). The usually recommended way to generate source–target (left language–right language) alignments is:

./fast_align -i text.fr-en -d -o -v > forward.align

The usually recommended way to generate target–source alignments is to just add the -r (“reverse”) option:

./fast_align -i text.fr-en -d -o -v -r > reverse.align

Using other tools, the generated forward and reverse alignments can be symmetrized into a (often higher quality) single alignment using intersection or union operations, as well as using a variety of more specialized heuristic criteria.
    """
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    command_line = "" #Path to the shell script TreeeTagger
    script_path = config_end_user.TOOL_FAST_ALIGN

    #chmod execute for script
    run_chmod(script_path)

    list_of_commands = []

    #get alignment source to target
    command_line = script_path + " -i " + file_input_path + " -d -o -v > " + file_output_alignment_source_to_target_path
    list_of_commands.append(command_line)

    #get alignment target to source
    command_line = script_path + " -i " + file_input_path + " -d -o -v -r > " + file_output_alignment_target_to_source_path
    list_of_commands.append(command_line)

    #print(command_line)

    ##Generate Shell Script

    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
def lowercase_raw_corpus_not_tokenizer(file_input_path, target_language, file_output_path, current_config):
    """
    Getting lowercasing but NOT tokenizer the raw corpus

    :type file_input_path: string
    :param file_input_path: contains raw corpus with format ROW.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains corpus after normalizing punctuation and tokenizing

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #current_config = load_configuration()

    command_line = "" #Path to the shell script Pre_processing
    script_path = current_config.TOOL_PRE_PROCESSING_LOWERCASING

    command_line = script_path + " " + target_language + " " + file_input_path + " " + file_output_path

    print(command_line)

    call_script(command_line, script_path)
#**************************************************************************#
#B1: Chay script pre_processing.sh -->tokenizer, khong lowercaser
def tokenizer_raw_corpus(file_input_path, target_language, file_output_path, current_config):
    """
    Getting tokenizer the raw corpus without lowercasing

    :type file_input_path: string
    :param file_input_path: contains raw corpus with format ROW.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains corpus after normalizing punctuation and tokenizing

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #current_config = load_configuration()

    command_line = "" #Path to the shell script Pre_processing
    script_path = current_config.TOOL_PRE_PROCESSING

    command_line = script_path + " " + target_language + " " + file_input_path + " " + file_output_path

    print(command_line)

    call_script(command_line, script_path)
#**************************************************************************#
#B2: perl /home/lent/Develops/Solution/eval_agent/eval_agent/lib/shell_script/make-factor-pos.tree-tagger-TienLe-TanLe.perl -tree-tagger /home/lent/Develops/DevTools/treetagger -l fr /home/lent/Develops/Solution/eval_agent/eval_agent/corpus/fr_en/preprocessing/881_output_preprocessing.fr /home/lent/Develops/Solution/eval_agent/eval_agent/corpus/fr_en/preprocessing/881_output_preprocessing.treetagger.fr -wordtaglemma
def get_output_treetagger_format_row(file_input_path, target_language, file_output_path):
    """
    Getting output from TreeTagger with format row

    :type file_input_path: string
    :param file_input_path: contains raw corpus with format ROW.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains corpus after normalizing punctuation and tokenizing

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    current_config = load_configuration()
    config_end_user = load_config_end_user()

    command_line = "perl" #Path to the shell script TreeeTagger
    script_path = current_config.TOOL_TREE_TAGGER
    #tree_tagger_path = current_config.TREE_TAGGER_PATH
    #script_path = config_end_user.TOOL_TREE_TAGGER
    tree_tagger_path = config_end_user.TREE_TAGGER_PATH

    #chmod +x for tree_tagger_path + "/bin/tree-tagger"
    path_to_tool_treetagger = tree_tagger_path + "/bin/tree-tagger"
    run_chmod(path_to_tool_treetagger)

    command_line = command_line + " " + script_path + " -tree-tagger " + tree_tagger_path + " -l " + target_language + " " + file_input_path + " " + file_output_path + " -wordtaglemma"

    print(command_line)

    call_script(command_line, script_path)

    customize_output_treetagger_format_row(file_output_path, file_output_path)
#**************************************************************************#
#B3: Chuyen format row thanh format cot dung cho Solution, bao gom: chuyen format cho du lieu va cho format output from TreeTagger dong
#for raw_corpus fr
#python3 $PYTHON3_PREPROCESSING/convert_format_row_to_format_column.py /home/lent/Develops/Solution/eval_agent/eval_agent/corpus/fr_en/preprocessing/881_output_preprocessing.fr /home/lent/Develops/Solution/eval_agent/eval_agent/corpus/fr_en/preprocessing/881_output_preprocessing.col.fr
#convert_format_row_to_format_column(file_input_path, file_output_path)
#replace "<UNK>||||||" --> "<unk>|||<unk>|||<unk>" trong format dong
#sed 's-<UNK>||||||-<unk>|||<unk>|||<unk>-g' < file_format_row > file_format_row_after_customizing

def get_output_treetagger_format_row_threads(file_input_path, target_language, file_output_path, current_config, config_end_user):
    """
    Getting output from TreeTagger with format row

    :type file_input_path: string
    :param file_input_path: contains raw corpus with format ROW.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains corpus after normalizing punctuation and tokenizing

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """

    #current_config = load_configuration()
    #config_end_user = load_config_end_user()

    command_line = "perl" #Path to the shell script TreeeTagger
    script_path = current_config.TOOL_TREE_TAGGER
    #tree_tagger_path = current_config.TREE_TAGGER_PATH
    #script_path = config_end_user.TOOL_TREE_TAGGER
    tree_tagger_path = config_end_user.TREE_TAGGER_PATH

    #chmod +x for tree_tagger_path + "/bin/tree-tagger"
    path_to_tool_treetagger = tree_tagger_path + "/bin/tree-tagger"
    run_chmod(path_to_tool_treetagger)
    #print(path_to_tool_treetagger)

    #command_line = command_line + " " + script_path + " -tree-tagger " + tree_tagger_path + " -l " + target_language + " " + file_input_path + " " + file_output_path + " -wordtaglemma"

    #print(command_line)
    l_threads = []
    for l_inc in range(1,current_config.THREADS+1):
        str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path +"."+str(l_inc)+")"
        is_existed_file(file_input_path +"."+str(l_inc), str_message_if_not_existed)
        #print (file_input_path +"."+str(l_inc))
        #print (file_output_path +"."+str(l_inc))
        command_line_thread = command_line + " " + script_path + " -tree-tagger " + tree_tagger_path + " -l " + target_language + " " + file_input_path +"."+str(l_inc) + " " + file_output_path +".tmp."+str(l_inc) + " -wordtaglemma"
        print(command_line_thread)
        ts = threading.Thread(target=call_script, args=(command_line_thread, script_path))
        l_threads.append(ts)
        ts.start()
    for myT in l_threads:
        myT.join()    
    time.sleep(1)
    customize_output_treetagger_format_row_threads(file_output_path +".tmp", file_output_path, current_config)
#**************************************************************************#

def customize_output_treetagger_format_row(file_input_path, file_output_path):
    """
    Getting output from TreeTagger with format row

    :type file_input_path: string
    :param file_input_path: contains raw corpus with format ROW.

    :type file_output_path: string
    :param file_output_path: contains corpus after normalizing punctuation and tokenizing

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    current_config = load_configuration()

    script_path = current_config.CUSTOMIZE_OUTPUT_TREETAGGER

    run_chmod(script_path)

    command_line = "sh " + script_path + " " + file_input_path + " " + file_output_path

    #print(command_line)
    call_script(command_line, script_path)
#**************************************************************************#
def customize_output_treetagger_format_row_threads(file_input_path, file_output_path, current_config):
    """
    Getting output from TreeTagger with format row

    :type file_input_path: string
    :param file_input_path: contains raw corpus with format ROW.

    :type file_output_path: string
    :param file_output_path: contains corpus after normalizing punctuation and tokenizing

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """

    #current_config = load_configuration()

    script_path = current_config.CUSTOMIZE_OUTPUT_TREETAGGER

    #run_chmod(script_path)

    #command_line = "sh " + script_path + " " + file_input_path + " " + file_output_path

    #print(command_line)
    for l_inc in range(1,current_config.THREADS+1):
        str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path +"."+str(l_inc)+")"
        is_existed_file(file_input_path +"."+str(l_inc), str_message_if_not_existed)
        #print (file_input_path +"."+str(l_inc))
        #print (file_output_path +"."+str(l_inc))
        command_line = "sh " + script_path + " " + file_input_path +"."+str(l_inc) + " " + file_output_path +"."+str(l_inc)
        print(command_line)
        call_script(command_line, script_path)
    #call_script(command_line, script_path)
#**************************************************************************#
def merging_1all_features_original(list_of_file_paths):
    """
    Using command paste to merge lines of files in list_of_file_paths

    :type list_of_file_paths: string
    :param list_of_file_paths: List contains ordered files that are results of extracting features

    :rtype: a file TEXT contains all features that is merged lines from ordered files
    """
    if len(list_of_file_paths) == 0:
        raise Exception("You should check the list of file paths")

    current_config = load_configuration()
    list_of_commands = []

    command_line = "paste "

    for item in list_of_file_paths:
        command_line += " " + item

    #append output
    command_line += " > " + current_config.OUTPUT_MERGED_FEATURES

    #Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
##########
def merging_all_features(list_of_file_paths, file_output_path):
    """
    Using command paste to merge lines of files in list_of_file_paths

    :type list_of_file_paths: string
    :param list_of_file_paths: List contains ordered files that are results of extracting features

    :type file_output_path: string
    :param file_output_path: path of output file

    :rtype: a file TEXT contains all features that is merged lines from ordered files
    """
    if len(list_of_file_paths) == 0:
        raise Exception("You should check the list of file paths: "+list_of_file_paths)

    current_config = load_configuration()
    list_of_commands = []

    command_line = "paste "

    for item in list_of_file_paths:
        command_line += " " + item

    #append output
    #command_line += " > " + current_config.OUTPUT_MERGED_FEATURES
    command_line += " > " + file_output_path

    print(command_line)

    #Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
def concat_all_features(list_of_file_paths, file_output_path):
    """
    Using command paste to merge lines of files in list_of_file_paths

    :type list_of_file_paths: string
    :param list_of_file_paths: List contains ordered files that are results of extracting features

    :type file_output_path: string
    :param file_output_path: path of output file

    :rtype: a file TEXT contains all features that is merged lines from ordered files
    """
    if len(list_of_file_paths) == 0:
        raise Exception("You should check the list of file paths")

    current_config = load_configuration()
    list_of_commands = []

    command_line = "cat "

    for item in list_of_file_paths:
        command_line += " " + item

    #append output
    #command_line += " > " + current_config.OUTPUT_MERGED_FEATURES
    command_line += " > " + file_output_path

    #Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
#B3: Dung wapiti voi cac template cho truoc de tao CRF model.
#Sau do, wapiti dung model de kiem tra lai du lieu dung ?%
#training CRF
def generating_CRF_models(demo_name, is_has_dev_corpus, template_path, order_of_template = 1):
    """
    Training CRF model with K number of templates.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type is_has_dev_corpus: boolean
    :param is_has_dev_corpus: True/False

    :type template_path: string
    :param template_path: path of template file

    :type order_of_template: int
    :param order_of_template: order of template
    """

    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #Goi ham Wapiti + Ung voi tung template --> train ra tung model cu the
    #wapiti train -a sgd-l1  --stopeps 0.000005 --stopwin 6 --maxiter 200 -p ./template.en DO_FOR_LUCIA/train_1881  DO_FOR_LUCIA/model
    #wapiti train -a sgd-l1  --stopeps 0.000005 --stopwin 6 --maxiter 200 -p training-10000/template.en_NBESTRESCORING  training-10000/trainingfile-binary-16072013-NBESTLIST.CRF  model_NBESTRESCORING
    #wapiti train -a l-bfgs/sgd-l1/bcd/rprop -i 200 -e 0.000005 -w 7  -d dev_file_path -p template_file_path train_file_path model_file_path

    #wapiti train -a sgd-l1 -i 200 -e 0.00005 -w 6 -d dev_file_path -p template_file_path train_file_path model_file_path

    #wapiti train -a sgd-l1 -i 200 -e 0.00005 -w 6 -p template_file_path train_file_path model_file_path

    command_line = ""
    #script_path = current_config.TOOL_WAPITI
    script_path = config_end_user.TOOL_WAPITI
    train_file_path = current_config.TRAIN_FILE_PATH  + "_" + demo_name + ".txt"
    dev_file_path = current_config.DEV_FILE_PATH  + "_" + demo_name + ".txt"
    #template_path_pattern = current_config.TEMPLATE_PATH
    model_file_path_pattern = current_config.MODEL_PATH
    log_file_pattern = current_config.LOG_FILE_TRAINING_WAPITI


    if is_has_dev_corpus:
        command_line = script_path + " train -a sgd-l1 -i 200 -e 0.00005 -w 6  -d " + dev_file_path + " -p "
    else:
        #there is not any corpus for developing phase
        command_line = script_path + " train -a sgd-l1 -i 200 -e 0.00005 -w 6 -p "
    #end if

    #template_path = template_path_pattern + str(item+1)
    model_path = model_file_path_pattern + str(order_of_template)  + "_" + demo_name + ".txt"
    log_path = log_file_pattern + str(order_of_template) +  "_" + demo_name + ".txt"

    command_line += template_path + " " + train_file_path + " " + model_path  + " --nthread " +str(current_config.THREADS) + " 2>&1 | tee " + log_path

    print("Demo: " + demo_name + " - Training with template " + str(order_of_template))
    print("Template path: %s" %template_path)
    print(command_line)

    #call_script(command_line, script_path)
    list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)

#**************************************************************************#
def generating_CRF_models_original(demo_name, number_of_template, is_has_dev_corpus):
    """
    Training CRF model with K number of templates.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type number_of_template: string
    :param number_of_template: number of file-templates

    :type is_has_dev_corpus: boolean
    :param is_has_dev_corpus: True/False
    """
    if number_of_template < 1:
        raise Exception("You should show me how many templates you would like to train CRF model.")

    current_config = load_configuration()


    #Goi ham Wapiti + Ung voi tung template --> train ra tung model cu the
    #wapiti train -a sgd-l1  --stopeps 0.000005 --stopwin 6 --maxiter 200 -p ./template.en DO_FOR_LUCIA/train_1881  DO_FOR_LUCIA/model
    #wapiti train -a sgd-l1  --stopeps 0.000005 --stopwin 6 --maxiter 200 -p training-10000/template.en_NBESTRESCORING  training-10000/trainingfile-binary-16072013-NBESTLIST.CRF  model_NBESTRESCORING
    #wapiti train -a l-bfgs/sgd-l1/bcd/rprop -i 200 -e 0.000005 -w 7  -d dev_file_path -p template_file_path train_file_path model_file_path

    command_line = ""
    script_path = current_config.TOOL_WAPITI
    run_chmod(script_path)

    train_file_path = current_config.TRAIN_FILE_PATH  + "_" + demo_name + ".txt"
    dev_file_path = current_config.DEV_FILE_PATH  + "_" + demo_name + ".txt"
    template_path_pattern = current_config.TEMPLATE_PATH
    model_file_path_pattern = current_config.MODEL_PATH
    log_file_pattern = current_config.LOG_FILE_TRAINING_WAPITI

    range_templates = range(number_of_template)

    for item in range_templates:
        if is_has_dev_corpus:
            command_line = script_path + " train -a sgd-l1 -i 200 -e 0.00005 -w 6  -d " + dev_file_path + " -p "
        else:
            #there is not any corpus for developing phase
            command_line = script_path + " train -a sgd-l1 -i 200 -e 0.00005 -w 6 -p "
        #end if

        template_path = template_path_pattern + str(item+1)
        model_path = model_file_path_pattern + str(item+1)  + "_" + demo_name + ".txt"
        log_path = log_file_pattern + str(item+1) +  "_" + demo_name + ".txt"

        command_line += template_path + " " + train_file_path + " " + model_path  + " 2>&1 | tee " + log_path

        print("Demo: " + demo_name + " - Training with template " + str(item+1))
        print(command_line)

        #call_script(command_line, script_path)
        list_of_commands = []

        ##Generate Shell Script
        list_of_commands.append(command_line)
        create_script_temp(list_of_commands)

        #Run Script
        call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
    #end for
#**************************************************************************#
#test model CRF
#./wapiti label -m ./model_NBESTRESCORING  -c -s -p /home/nluong/FEATURE_EXTRACTION_NBEST/FEATURES/881.NBEST.CRF   /home/nluong/FEATURE_EXTRACTION_NBEST/FEATURES/881.NBEST.rs
#./wapiti label -m DO_FOR_LUCIA/model  -c -s -p DO_FOR_LUCIA/test_9000  DO_FOR_LUCIA/rs

#./wapiti label -m model_path -c -s -p test_file_path result_file_path

#/home/lent/Develops/Solution/eval_agent/eval_agent/config/../../tool/wapiti-1.5.0/./wapiti label -c -s -p /home/lent/Develops/Solution/eval_agent/eval_agent/config/../extracted_features/en.column.CRF_model_test_file.txt -m /home/lent/Develops/Solution/eval_agent/eval_agent/config/../extracted_features/CRF_model_with_template2 /home/lent/Develops/Solution/eval_agent/eval_agent/config/../extracted_features/CRF_model_result_testing_with_model2 2>&1 | tee /home/lent/Develops/Solution/eval_agent/eval_agent/config/../extracted_features/CRF_model_result_testing_with_model_log_file2

#./wapiti-1.5.0/./wapiti label -c -s -p test_file.txt -m CRF_model CRF_result 2>&1 | tee CRF_result_log_file
def get_result_testing_CRF_models(demo_name, order_of_template = 1):
    """
    Testing phase of labeling within CRF model with K number of model.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type order_of_template: int
    :param order_of_template: order of template
    """

    current_config = load_configuration()
    config_end_user = load_config_end_user()

    command_line = ""
    #script_path = current_config.TOOL_WAPITI
    script_path = config_end_user.TOOL_WAPITI
    model_file_path_pattern = current_config.MODEL_PATH
    result_testing_wapiti_pattern = current_config.RESULT_TESTING_WAPITI
    log_file_pattern = current_config.LOG_FILE_TESTING_WAPITI
    test_file_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    command_line = script_path + " label -c -s -p " + test_file_path + " -m "

    model_path = model_file_path_pattern + str(order_of_template) + "_" + demo_name + ".txt"
    result_file_path = result_testing_wapiti_pattern + str(order_of_template) +  "_" + demo_name + ".txt"
    log_path = log_file_pattern + str(order_of_template) +  "_" + demo_name + ".txt"

    #For writing log file
    command_line += model_path + " " + result_file_path + " 2>&1 | tee " + log_path
    #command_line += model_path + " " + result_file_path

    print("Demo: " + demo_name + " - Testing with template " + str(order_of_template))
    print(command_line)

    #khong chay duoc khi chay truc tiep --> ERROR: "error: too much input files on command line"
    #call_script(command_line, script_path)

    list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)


    #######################################################################
    #Tinh bang 'tay'
    #Ket qua cua wapiti: result_file_path
    #tinh bang tay: output path:
    log_path_manual = log_file_pattern + str(order_of_template) +  "_" + demo_name + "_manual.txt"
    file_writer = open(log_path_manual, mode = 'w', encoding = 'utf-8')

    #lay danh sach oracle (list_of_oracle_label) va danh sach (list_of_wapiti_label)
    list_of_oracle_label, list_of_wapiti_label = get_list_of_oracle_label_and_list_of_wapiti_label_from_result_wapiti_labeling(result_file_path)

    line_separate = "-"*63

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    #* classifier Good/Bad.
    X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good = get_precision_recall_fscore_within_list(list_of_oracle_label, list_of_wapiti_label)

    str_baseline = "*** Template_" + str(order_of_template) + "_" + demo_name + " classifier Good/Bad:"
    print(str_baseline)
    file_writer.write(str_baseline)
    file_writer.write("\n")

    #B
    str_B_baseline = "X-Bad = %d \t Y-Bad = %d \t Z-Bad = %d" %(X_bad, Y_bad, Z_bad)
    print(str_B_baseline)
    file_writer.write(str_B_baseline)
    file_writer.write("\n")

    #G
    str_G_baseline = "X-Good = %d \t Y-Good = %d \t Z-Good = %d" %(X_good, Y_good, Z_good)
    print(str_G_baseline)
    file_writer.write(str_G_baseline)
    file_writer.write("\n")

    ##########################
    #B
    str_result = "B \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_bad, Rc_bad, F_bad)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #G
    str_result = "G \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_good, Rc_good, F_good)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    file_writer.close()
#**************************************************************************#
def get_result_testing_CRF_models_within_given_list_of_models(demo_name, order_of_template, test_file_path, extension = ""):
    """
    Testing phase of labeling within CRF model with K number of model.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type order_of_template: int
    :param order_of_template: order of template

    :type test_file_path: string
    :param test_file_path: path of test file
    """

    current_config = load_configuration()
    config_end_user = load_config_end_user()

    command_line = ""
    #script_path = current_config.TOOL_WAPITI
    script_path = config_end_user.TOOL_WAPITI
    model_file_path_pattern = current_config.MODEL_PATH
    result_testing_wapiti_pattern = current_config.RESULT_TESTING_WAPITI
    log_file_pattern = current_config.LOG_FILE_TESTING_WAPITI
    #test_file_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    command_line = script_path + " label -c -s -p " + test_file_path + " -m "

    #Khong thay doi duong dan den model
    model_path = model_file_path_pattern + str(order_of_template) + "_" + demo_name + ".txt"

    #cap nhat
    result_file_path = result_testing_wapiti_pattern + str(order_of_template) +  "_" + demo_name + "_testing_wmt" + ".txt" + extension
    log_path = log_file_pattern + str(order_of_template) +  "_" + demo_name + "_testing_wmt" + ".txt"  + extension

    #For writing log file
    command_line += model_path + " " + result_file_path + " 2>&1 | tee " + log_path
    #command_line += model_path + " " + result_file_path

    print("Demo: " + demo_name + " - Testing WMT with template " + str(order_of_template))
    print(command_line)

    #khong chay duoc khi chay truc tiep --> ERROR: "error: too much input files on command line"
    #call_script(command_line, script_path)

    list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)


    #######################################################################
    #Tinh bang 'tay'
    #Ket qua cua wapiti: result_file_path
    #tinh bang tay: output path:
    #cap nhat
    log_path_manual = log_file_pattern + str(order_of_template) +  "_" + demo_name + "_testing_wmt" + "_manual.txt" + extension

    file_writer = open(log_path_manual, mode = 'w', encoding = 'utf-8')

    #lay danh sach oracle (list_of_oracle_label) va danh sach (list_of_wapiti_label)
    list_of_oracle_label, list_of_wapiti_label = get_list_of_oracle_label_and_list_of_wapiti_label_from_result_wapiti_labeling(result_file_path)

    line_separate = "-"*63

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    #* classifier Good/Bad.
    X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good = get_precision_recall_fscore_within_list(list_of_oracle_label, list_of_wapiti_label)

    str_baseline = "*** Template_" + str(order_of_template) + "_" + demo_name + " classifier Good/Bad:"
    print(str_baseline)
    file_writer.write(str_baseline)
    file_writer.write("\n")

    #B
    str_B_baseline = "X-Bad = %d \t Y-Bad = %d \t Z-Bad = %d" %(X_bad, Y_bad, Z_bad)
    print(str_B_baseline)
    file_writer.write(str_B_baseline)
    file_writer.write("\n")

    #G
    str_G_baseline = "X-Good = %d \t Y-Good = %d \t Z-Good = %d" %(X_good, Y_good, Z_good)
    print(str_G_baseline)
    file_writer.write(str_G_baseline)
    file_writer.write("\n")

    ##########################
    #B
    str_result = "B \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_bad, Rc_bad, F_bad)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #G
    str_result = "G \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_good, Rc_good, F_good)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    file_writer.close()
#**************************************************************************#
def get_result_testing_CRF_models_within_given_list_of_models_without_manual_estimation(demo_name, order_of_template, test_file_path, extension = ""):
    """
    Testing phase of labeling within CRF model with K number of model.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type order_of_template: int
    :param order_of_template: order of template

    :type test_file_path: string
    :param test_file_path: path of test file
    """

    current_config = load_configuration()
    config_end_user = load_config_end_user()

    command_line = ""
    #script_path = current_config.TOOL_WAPITI
    script_path = config_end_user.TOOL_WAPITI
    model_file_path_pattern = current_config.MODEL_PATH
    result_testing_wapiti_pattern = current_config.RESULT_TESTING_WAPITI
    log_file_pattern = current_config.LOG_FILE_TESTING_WAPITI
    #test_file_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    command_line = script_path + " label -c -s -p " + test_file_path + " -m "

    #Khong thay doi duong dan den model
    model_path = model_file_path_pattern + str(order_of_template) + "_" + demo_name + ".txt"

    #cap nhat
    result_file_path = result_testing_wapiti_pattern + str(order_of_template) +  "_" + demo_name + "_testing_wmt" + ".txt" + extension
    log_path = log_file_pattern + str(order_of_template) +  "_" + demo_name + "_testing_wmt" + ".txt"  + extension

    #For writing log file
    command_line += model_path + " " + result_file_path + " 2>&1 | tee " + log_path
    #command_line += model_path + " " + result_file_path

    print("Demo: " + demo_name + " - Testing WMT with template " + str(order_of_template))
    print(command_line)

    #khong chay duoc khi chay truc tiep --> ERROR: "error: too much input files on command line"
    #call_script(command_line, script_path)

    list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)

    #Return testing_result's path
    return result_file_path
#**************************************************************************#
def get_result_testing_CRF_models_original(demo_name, number_of_template):
    """
    Testing phase of labeling within CRF model with K number of model.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type number_of_template: string
    :param number_of_template: number of file-models
    """
    if number_of_template < 1:
        raise Exception("You should show me how many models you would like to test CRF model.")

    current_config = load_configuration()

    command_line = ""
    script_path = current_config.TOOL_WAPITI
    model_file_path_pattern = current_config.MODEL_PATH
    result_testing_wapiti_pattern = current_config.RESULT_TESTING_WAPITI
    log_file_pattern = current_config.LOG_FILE_TESTING_WAPITI
    test_file_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    range_templates = range(number_of_template)

    for item in range_templates:
        command_line = script_path + " label -c -s -p " + test_file_path + " -m "

        model_path = model_file_path_pattern + str(item+1) + "_" + demo_name + ".txt"
        result_file_path = result_testing_wapiti_pattern + str(item+1) +  "_" + demo_name + ".txt"
        log_path = log_file_pattern + str(item+1) +  "_" + demo_name + ".txt"

        #For writing log file
        command_line += model_path + " " + result_file_path + " 2>&1 | tee " + log_path
        #command_line += model_path + " " + result_file_path

        print("Demo: " + demo_name + " - Testing with template " + str(item+1))
        print(command_line)

        #khong chay duoc khi chay truc tiep --> ERROR: "error: too much input files on command line"
        #call_script(command_line, script_path)

        list_of_commands = []

        ##Generate Shell Script
        list_of_commands.append(command_line)
        create_script_temp(list_of_commands)

        #Run Script
        call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
    #end for
#**************************************************************************#
#Sequential Corpus / Random Corpus
def demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template):
    """
    Demo System with 2 phases within CRF model such as training phase and labeling phase that we use tool WAPITI (ref: http://wapiti.limsi.fr/)

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type corpus_type: string
    :param corpus_type: the type of corpus after generating. For example: Sequential Corpus or Random Corpus

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :type number_of_template: string
    :param number_of_template: number of templates, if number_of_template == 0 then we use this method for subset
    """
    #B2: divide corpus to train, dev, test corpus
    #note: Number of sententences in file for testing if the number of sentences that remains.
    #creating_sequential_corpus_train_dev_test_file_from_merged_file(file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    current_config = load_configuration()

    if corpus_type == current_config.SEQUENTIAL_CORPUS:
        creating_sequential_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    elif corpus_type == current_config.RANDOM_CORPUS:
        creating_random_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    elif corpus_type == current_config.BOOSTING_CORPUS:
        #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, order_n_fold, number_of_sentences_in_n_fold_testing_set, number_of_sentences_in_file_for_developing)
        #order_n_fold >=1, phu thuoc NUMBER_OF_FOLDS
        num_range = range(current_config.NUMBER_OF_FOLDS)
        for i in num_range:
        #number_of_sentences_in_n_fold_testing_set ~ number_of_sentences_in_file_for_training (dung chung ten) !!! chu y phan nay nha!!!
            tmp_demo_name = demo_name + "_fold_" + str(i+1)
            creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(tmp_demo_name, current_config.OUTPUT_MERGED_FEATURES, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
            #print("demo_name - in creating: %s" %tmp_demo_name)
        #end for
    #end if

    #B3: CRF model using wapiti
    #Create models ~ depend on the templates that our system can generate the corresponding number of models
    #template file name: template.enN in directory "/lib/templates". For example: template.en1
    if number_of_sentences_in_file_for_developing > 0:
        is_has_dev_corpus = True
    else:
        is_has_dev_corpus = False #because number_of_sentences_in_file_for_developing = 0

    #Just for testing with the range of some templates
    num_of_template_start = 1
    num_of_template_end = 26

    if number_of_template >= 1: #dung cho demo WCE systems
        template_path_pattern = current_config.TEMPLATE_PATH
        item_range = range(number_of_template)
        for item in item_range:
            #Just for testing with the range of some templates
            if item >= num_of_template_start - 1 and item <= num_of_template_end -1:
                template_path = template_path_pattern + str(item+1)

                generating_CRF_models(demo_name, is_has_dev_corpus, template_path, item + 1)

                get_result_testing_CRF_models(demo_name, item + 1)
            #end if
        #end for
    else: #dung cho demo wce Subset, number_of_template < 0
        if corpus_type != current_config.BOOSTING_CORPUS:
            template_path = current_config.TEMPLATE_PATH_PATTERN + str(number_of_template) #ten template trong thu muc "extracted_features" co dang: template_subset-1
            generating_CRF_models(demo_name, is_has_dev_corpus, template_path, number_of_template)

            get_result_testing_CRF_models(demo_name, number_of_template)
        elif corpus_type == current_config.BOOSTING_CORPUS:
            template_path = current_config.BOOST_TEMPLATE_PATH_PATTERN + str(number_of_template) #ten template trong thu muc "extracted_features" co dang: boosting_subset_template_subset-1 for boosting
        #end if
            num_range = range(current_config.NUMBER_OF_FOLDS)
            for i in num_range:
                tmp_demo_name = demo_name + "_fold_" + str(i+1)
                #number_of_sentences_in_n_fold_testing_set ~ number_of_sentences_in_file_for_training (dung chung ten) !!! chu y phan nay nha!!!
                #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
                generating_CRF_models(tmp_demo_name, is_has_dev_corpus, template_path, number_of_template)
                get_result_testing_CRF_models(tmp_demo_name, number_of_template)

                #result_file_path = current_config.RESULT_TESTING_WAPITI + str(number_of_template) +  "_" + tmp_demo_name + ".txt"
                #print("result of output wapiti: %s" %result_file_path)

                #raise Exception("Just for testing")
            #end for
    #endif
#**************************************************************************#
#Sequential Corpus / Random Corpus
def demo_system_within_given_input_file(demo_name, file_input_path, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template):
    """
    Demo System with 2 phases within CRF model such as training phase and labeling phase that we use tool WAPITI (ref: http://wapiti.limsi.fr/)

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type corpus_type: string
    :param corpus_type: the type of corpus after generating. For example: Sequential Corpus or Random Corpus

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :type number_of_template: string
    :param number_of_template: number of templates, if number_of_template == 0 then we use this method for subset
    """
    #B2: divide corpus to train, dev, test corpus
    #note: Number of sententences in file for testing if the number of sentences that remains.
    #creating_sequential_corpus_train_dev_test_file_from_merged_file(file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    current_config = load_configuration()

    if corpus_type == current_config.SEQUENTIAL_CORPUS:
        #creating_sequential_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
        creating_sequential_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    elif corpus_type == current_config.RANDOM_CORPUS:
        #creating_random_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
        creating_random_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    elif corpus_type == current_config.BOOSTING_CORPUS:
        #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, order_n_fold, number_of_sentences_in_n_fold_testing_set, number_of_sentences_in_file_for_developing)
        #order_n_fold >=1, phu thuoc NUMBER_OF_FOLDS
        num_range = range(current_config.NUMBER_OF_FOLDS)
        for i in num_range:
        #number_of_sentences_in_n_fold_testing_set ~ number_of_sentences_in_file_for_training (dung chung ten) !!! chu y phan nay nha!!!
            tmp_demo_name = demo_name + "_fold_" + str(i+1)
            #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(tmp_demo_name, current_config.OUTPUT_MERGED_FEATURES, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
            creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(tmp_demo_name, file_input_path, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
            #print("demo_name - in creating: %s" %tmp_demo_name)
        #end for
    #end if

    #B3: CRF model using wapiti
    #Create models ~ depend on the templates that our system can generate the corresponding number of models
    #template file name: template.enN in directory "/lib/templates". For example: template.en1
    if number_of_sentences_in_file_for_developing > 0:
        is_has_dev_corpus = True
    else:
        is_has_dev_corpus = False #because number_of_sentences_in_file_for_developing = 0

    #Just for testing with the range of some templates
    num_of_template_start = 1
    num_of_template_end = 26

    if number_of_template >= 1: #dung cho demo WCE systems
        template_path_pattern = current_config.TEMPLATE_PATH
        item_range = range(number_of_template)
        for item in item_range:
            #Just for testing with the range of some templates
            if item >= num_of_template_start - 1 and item <= num_of_template_end -1:
                template_path = template_path_pattern + str(item+1)

                generating_CRF_models(demo_name, is_has_dev_corpus, template_path, item + 1)

                get_result_testing_CRF_models(demo_name, item + 1)
            #end if
        #end for
    else: #dung cho demo wce Subset, number_of_template < 0
        if corpus_type != current_config.BOOSTING_CORPUS:
            template_path = current_config.TEMPLATE_PATH_PATTERN + str(number_of_template) #ten template trong thu muc "extracted_features" co dang: template_subset-1
            generating_CRF_models(demo_name, is_has_dev_corpus, template_path, number_of_template)

            get_result_testing_CRF_models(demo_name, number_of_template)
        elif corpus_type == current_config.BOOSTING_CORPUS:
            template_path = current_config.BOOST_TEMPLATE_PATH_PATTERN + str(number_of_template) #ten template trong thu muc "extracted_features" co dang: boosting_subset_template_subset-1 for boosting
        #end if
            num_range = range(current_config.NUMBER_OF_FOLDS)
            for i in num_range:
                tmp_demo_name = demo_name + "_fold_" + str(i+1)
                #number_of_sentences_in_n_fold_testing_set ~ number_of_sentences_in_file_for_training (dung chung ten) !!! chu y phan nay nha!!!
                #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
                generating_CRF_models(tmp_demo_name, is_has_dev_corpus, template_path, number_of_template)
                get_result_testing_CRF_models(tmp_demo_name, number_of_template)

                #result_file_path = current_config.RESULT_TESTING_WAPITI + str(number_of_template) +  "_" + tmp_demo_name + ".txt"
                #print("result of output wapiti: %s" %result_file_path)

                #raise Exception("Just for testing")
            #end for
    #endif
#**************************************************************************#
def divide_merged_features_file_within_given_input_file(demo_name, file_input_path, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing):
    """
    Demo System with 2 phases within CRF model such as training phase and labeling phase that we use tool WAPITI (ref: http://wapiti.limsi.fr/)

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type corpus_type: string
    :param corpus_type: the type of corpus after generating. For example: Sequential Corpus or Random Corpus

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #B2: divide corpus to train, dev, test corpus
    #note: Number of sententences in file for testing if the number of sentences that remains.
    #creating_sequential_corpus_train_dev_test_file_from_merged_file(file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    current_config = load_configuration()

    if corpus_type == current_config.SEQUENTIAL_CORPUS:
        #creating_sequential_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
        creating_sequential_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    elif corpus_type == current_config.RANDOM_CORPUS:
        #creating_random_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
        creating_random_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    elif corpus_type == current_config.BOOSTING_CORPUS:
        #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, order_n_fold, number_of_sentences_in_n_fold_testing_set, number_of_sentences_in_file_for_developing)
        #order_n_fold >=1, phu thuoc NUMBER_OF_FOLDS
        num_range = range(current_config.NUMBER_OF_FOLDS)
        for i in num_range:
        #number_of_sentences_in_n_fold_testing_set ~ number_of_sentences_in_file_for_training (dung chung ten) !!! chu y phan nay nha!!!
            tmp_demo_name = demo_name + "_fold_" + str(i+1)
            #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(tmp_demo_name, current_config.OUTPUT_MERGED_FEATURES, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
            creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(tmp_demo_name, file_input_path, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
            #print("demo_name - in creating: %s" %tmp_demo_name)
        #end for
    #end if
#**************************************************************************#
#Sequential Corpus / Random Corpus
def wce_system_after_dividing_corpus(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template, num_of_template_start, num_of_template_end):
    """
    Demo System with 2 phases within CRF model such as training phase and labeling phase that we use tool WAPITI (ref: http://wapiti.limsi.fr/)

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type corpus_type: string
    :param corpus_type: the type of corpus after generating. For example: Sequential Corpus or Random Corpus

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :type number_of_template: string
    :param number_of_template: number of templates, if number_of_template == 0 then we use this method for subset
    """
    #B2: divide corpus to train, dev, test corpus
    #note: Number of sententences in file for testing if the number of sentences that remains.
    #creating_sequential_corpus_train_dev_test_file_from_merged_file(file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    current_config = load_configuration()

    #B3: CRF model using wapiti
    #Create models ~ depend on the templates that our system can generate the corresponding number of models
    #template file name: template.enN in directory "/lib/templates". For example: template.en1
    if number_of_sentences_in_file_for_developing > 0:
        is_has_dev_corpus = True
    else:
        is_has_dev_corpus = False #because number_of_sentences_in_file_for_developing = 0

    #Just for testing with the range of some templates
    #num_of_template_start = 1
    #num_of_template_end = 26

    if number_of_template >= 1: #dung cho demo WCE systems
        template_path_pattern = current_config.TEMPLATE_PATH
        item_range = range(number_of_template)
        for item in item_range:
            #Just for testing with the range of some templates
            if item >= num_of_template_start - 1 and item <= num_of_template_end -1:
                template_path = template_path_pattern + str(item+1)

                generating_CRF_models(demo_name, is_has_dev_corpus, template_path, item + 1)

                get_result_testing_CRF_models(demo_name, item + 1)
            #end if
        #end for
    else: #dung cho demo wce Subset, number_of_template < 0
        if corpus_type != current_config.BOOSTING_CORPUS:
            template_path = current_config.TEMPLATE_PATH_PATTERN + str(number_of_template) #ten template trong thu muc "extracted_features" co dang: template_subset-1
            generating_CRF_models(demo_name, is_has_dev_corpus, template_path, number_of_template)

            get_result_testing_CRF_models(demo_name, number_of_template)
        elif corpus_type == current_config.BOOSTING_CORPUS:
            template_path = current_config.BOOST_TEMPLATE_PATH_PATTERN + str(number_of_template) #ten template trong thu muc "extracted_features" co dang: boosting_subset_template_subset-1 for boosting
        #end if
            num_range = range(current_config.NUMBER_OF_FOLDS)
            for i in num_range:
                tmp_demo_name = demo_name + "_fold_" + str(i+1)
                #number_of_sentences_in_n_fold_testing_set ~ number_of_sentences_in_file_for_training (dung chung ten) !!! chu y phan nay nha!!!
                #creating_n_fold_cross_validation_corpus_train_dev_test_file_from_merged_file(demo_name, file_input_path, i+1, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
                generating_CRF_models(tmp_demo_name, is_has_dev_corpus, template_path, number_of_template)
                get_result_testing_CRF_models(tmp_demo_name, number_of_template)

                #result_file_path = current_config.RESULT_TESTING_WAPITI + str(number_of_template) +  "_" + tmp_demo_name + ".txt"
                #print("result of output wapiti: %s" %result_file_path)

                #raise Exception("Just for testing")
            #end for
    #endif
#**************************************************************************#
def demo_system_original(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing,  number_of_template):
    """
    Demo System with 2 phases within CRF model such as training phase and labeling phase that we use tool WAPITI (ref: http://wapiti.limsi.fr/)

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type corpus_type: string
    :param corpus_type: the type of corpus after generating. For example: Sequential Corpus or Random Corpus

    :type number_of_sentences_in_file_for_training: string
    :param number_of_sentences_in_file_for_training: the number of sentences for training corpus

    :type number_of_sentences_in_file_for_developing: string
    :param number_of_sentences_in_file_for_developing: the number of sentences for developing corpus

    :type number_of_template: string
    :param number_of_template: number of templates
    """
    #B2: divide corpus to train, dev, test corpus
    #note: Number of sententences in file for testing if the number of sentences that remains.
    #creating_sequential_corpus_train_dev_test_file_from_merged_file(file_input_path, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    current_config = load_configuration()

    if corpus_type == current_config.SEQUENTIAL_CORPUS:
        creating_sequential_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    else:
        creating_random_corpus_train_dev_test_file_from_merged_file(demo_name, current_config.OUTPUT_MERGED_FEATURES, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)

    #B3: CRF model using wapiti
    #Create models ~ depend on the templates that our system can generate the corresponding number of models
    #template file name: template.enN in directory "/lib/templates". For example: template.en1
    if number_of_sentences_in_file_for_developing > 0:
        is_has_dev_corpus = True
    else:
        is_has_dev_corpus = False #because number_of_sentences_in_file_for_developing = 0
    #end if
    generating_CRF_models(demo_name, number_of_template, is_has_dev_corpus)

    #Test model
    get_result_testing_CRF_models(demo_name, number_of_template)
#**************************************************************************#
def get_file_oracle_label_given_all_features_file(file_input_path, file_output_path):
    """
    Getting file that contains oracle label from file in which there is all extracted features

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :type file_output_path: string
    :param file_output_path: contains oracle label with format each "label" in each line is; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input')
    """
    str_message_if_not_existed = "Not Existed file corpus input ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #0        1        0        0        0        1        1        1        1        r        7        1        1        F        2        2        2        2        también        ADV        también        aumentó        VLfin        aumentar        _X-1        _X-1        _X-1        also        RB        also        rose        VVD        rise        it        PP        it        G
    for line in file_reader:
        line = line.strip()
        if len(line) == 0:
            file_writer.write("\n")
            continue
        #end if

        items = split_string_to_list_delimeter_tab(line)
        num_of_items = len(items)

        oracle_label = items[num_of_items - 1]
        oracle_label = oracle_label.strip()

        file_writer.write(oracle_label + "\n")
    #end for

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
#LIST_OF_SERVER_NAME
#Split input with the number of LIST_OF_SERVER_NAME
#TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_PATTERN
def split_input_within_given_list_of_servers(file_input_path, list_of_server_name, file_output_path_pattern):
    num_of_servers = len(list_of_server_name)

    if num_of_servers == 0:
        raise Exception("You should check List of Server_name in Configuration or contact Tien LE")
    #end if

    str_message_if_not_existed = "Not Existed file corpus input within format column ("+file_input_path+")"
    is_existed_file(file_input_path, str_message_if_not_existed)

    num_of_sent = count_number_of_sentences_in_file_within_format_column(file_input_path)

    #Tinh so cau co the co trong moi file duoc chia, lam tron den phan chuc
    delta = 50 #de so luong cau trong moi corpus cao hon AVG

    #y = round(x, -1)
    num_of_sent_in_each_splitted_file = num_of_sent // num_of_servers #div
    num_of_sent_in_each_splitted_file = round(num_of_sent_in_each_splitted_file, -1) + delta


    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')


    number_of_current_sentence = 1
    current_index_server_name = 0
    file_output_path = file_output_path_pattern + "_" + list_of_server_name[current_index_server_name]

    for line in file_reader:
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line) == 0: #cau moi xuat hien
            number_of_current_sentence += 1
        else:
            if number_of_current_sentence <= num_of_sent_in_each_splitted_file:
                #for writing: file_output_path
                file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

                file_writer.write(line)

                #close file
                file_writer.close()
            else:
                str_output = "corpus for server " + list_of_server_name[current_index_server_name] + " has " + str(number_of_current_sentence) + " sentences"
                print(str_output)

                str_output = "next server: " + list_of_server_name[current_index_server_name + 1 ]

                #for writing: file_output_path
                file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

                file_writer.write("\n")

                #close file
                file_writer.close()

                number_of_current_sentence = 1
                current_index_server_name += 1
                file_output_path = file_output_path_pattern + "_" + list_of_server_name[current_index_server_name]

                #for writing: file_output_path
                file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

                file_writer.write(line)

                #close file
                file_writer.close()
            #end if
        #end if

        if number_of_current_sentence <= num_of_sent_in_each_splitted_file:
            #file_output_path = file_output_path_pattern + "_" + list_of_server_name[current_index_server_name]

            #for writing: file_output_path
            file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

            file_writer.write("\n")

            #close file
            file_writer.close()
        #end if
    #end for

    #close file
    file_reader.close()
#**************************************************************************#
def merge_files_within_given_list_of_servers(file_output_path_pattern, list_of_server_name, file_output_path):
    num_of_servers = len(list_of_server_name)

    if num_of_servers == 0:
        raise Exception("You should check List of Server_name in Configuration or contact Tien LE")
    #end if

    list_of_file_paths = []
    for current_index_server_name in range(num_of_servers):
        file_input_path = file_output_path_pattern + "_" + list_of_server_name[current_index_server_name]

        #check existed paths
        if not os.path.exists(file_input_path):
            continue
        #end if

        #neu ton tai thi dua vao list de concat
        list_of_file_paths.append(file_input_path)
    #end for

    concatenating_files(list_of_file_paths, file_output_path)
    #concat_all_features(list_of_file_paths, file_output_path)
#**************************************************************************#
def remove_empty_line_in_file(file_input_path, file_output_path):
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    for line in file_reader:
        line = line.strip()

        if len(line) == 0:
            continue
        #end if

        file_writer.write(line + "\n")
    #end for

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
#replace_substring_in_string(str_input, str_find, str_replace)
def replace_substring_in_string_within_given_file(file_input_path, str_find, str_replace, file_output_path):
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    for line in file_reader:
        line = line.strip()

        if len(line) == 0:
            file_writer.write("\n")
            continue
        #end if

        str_output = replace_substring_in_string(line, str_find, str_replace)
        file_writer.write(str_output + "\n")
    #end for

    #close file
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def verify_result_old_and_new(file_input_path1, file_input_path2, file_output_path):
    """
    Checking each line "line_in1" (in file_input_path1) and each line "line_in2" (in file_input_path2)

    if line_in1 != line_in2 then
        write(the index of sentence that is different)

    :type file_input_path1: string
    :param file_input_path1: contains the data in file 1

    :type file_input_path2: string
    :param file_input_path2: contains the data in file 2

    :type file_output_path: string
    :param file_output_path: contains the index of sentence that is different and the number of sentence that is traversed

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path1):
        raise TypeError('Not Existed file 1')

    if not os.path.exists(file_input_path2):
        raise TypeError('Not Existed file 2')

    #open 1 file:
    #for writing: file_output_path
    #file_writer = open(file_output_path, 'w')
    file_writer = open(file_output_path, mode='w', encoding='utf-8')

    list_of_sentence1 = []
    list_of_sentence2 = []

    list_of_sentence1 = get_list_from_file_for_verify(file_input_path1)
    list_of_sentence2 = get_list_from_file_for_verify(file_input_path2)

    number_of_same_sentences = 0
    number_of_different_sentences = 0

    if len(list_of_sentence1) != len(list_of_sentence2):
        print("2 files file_input_path1 and file_input_path2 have not the same number of sentences.")
    else:
        for i in range(len(list_of_sentence1)):
            if len(list_of_sentence1[i].strip()) == 0:
                continue
            elif list_of_sentence1[i] != list_of_sentence2[i]: # different
                file_writer.write(str(i+1) + "\t" + list_of_sentence1[i] + "\t" + list_of_sentence2[i]) #De xac dinh theo so thu tu cua cau
                file_writer.write('\n')
                number_of_different_sentences = number_of_different_sentences +1
            else:
                number_of_same_sentences = number_of_same_sentences + 1
        file_writer.write('******************************************\n')
        file_writer.write('Number of different sentences: ' +  str(number_of_different_sentences) + '\n')

        file_writer.write('******************************************\n')
        file_writer.write('Number of same sentences: ' + str(number_of_same_sentences) + '\n')

    #close file
    file_writer.close()
#**************************************************************************#
def split_files(inputFile,numParts,outputName):
    """
    Split files in several parts.
    """
    print ("Splitting "+inputFile )
    str_message_if_not_existed = inputFile + " does not exist !!!"
    is_existed_file(inputFile, str_message_if_not_existed)
    
    tot_lines = sum(1 for line in open(inputFile))
    if (tot_lines % numParts != 0 ):
        nbr_lines = int((tot_lines)/numParts) + 1
    else:
        nbr_lines = int((tot_lines)/numParts)
    #nbr_lines = int((tot_lines)/numParts) + 1
    print ("in "+str(numParts) + " into " + outputName)
    #fileSize=os.stat(inputFile).st_size
    #parts=FileSizeParts(fileSize,numParts)
    #print ("%d parties pour decouper %s et le mettre dans %s", numParts, inputFile,outputName)
    openInputFile = open(inputFile, 'r')
    outPart=1
    cpt_lines = 0
    for line in openInputFile:
        cpt_lines+=1
        if cpt_lines > nbr_lines:
            outPart+=1
            cpt_lines=1
        if cpt_lines <= nbr_lines:            
            fullOutputName=outputName+os.extsep+str(outPart)
            if cpt_lines == 1:
                openOutputFile=open(fullOutputName,'w')
            else:
                openOutputFile=open(fullOutputName,'a')
            openOutputFile.write(line)
            openOutputFile.close()
    openInputFile.close()
    return outPart-1

#**************************************************************************#
def split_files_moses_alignment_output(inputFile,numParts,outputName):
    """
    Split files in several parts.
    """
    for line in open(inputFile):
        nbest_line = int(line.split('|||')[0])
    nbest_line+=1
    tot_lines = nbest_line
    if (tot_lines % numParts != 0 ):
        nbr_lines = int((tot_lines)/numParts) + 1
    else:
        nbr_lines = int((tot_lines)/numParts)
    #nbr_lines = int((tot_lines)/numParts) + 1
    limit_lines = nbr_lines
    #fileSize=os.stat(inputFile).st_size
    #parts=FileSizeParts(fileSize,numParts)
    #print ("%d parties pour decouper %s et le mettre dans %s", numParts, inputFile,outputName)
    openInputFile = open(inputFile, 'r')
    outPart=1
    cpt_lines = 0
    old_nbest_line = 0
    nbest_line = 0
    for line in openInputFile:
        nbest_line = int(line.split('|||')[0])
        #if nbest_line != old_nbest_line:
            #cpt_lines+=1
            #print (str(cpt_lines)+" "+str(nbest_line)+" "+str(old_nbest_line)+" "+str(nbest_line))
        #old_nbest_line=nbest_line
        if nbest_line + 1 > limit_lines:
            outPart+=1
            limit_lines = limit_lines + nbr_lines
            cpt_lines=0
        if nbest_line <= limit_lines:
            cpt_lines+=1
            fullOutputName=outputName+os.extsep+str(outPart)
            if cpt_lines == 1:
                openOutputFile=open(fullOutputName,'w')
            else:
                openOutputFile=open(fullOutputName,'a')
            openOutputFile.write(line)
            openOutputFile.close()
    openInputFile.close()
    return outPart-1

#**************************************************************************#
def merge_files_threads(list_of_file_paths, current_config):
    for l_file in list_of_file_paths:
        message="WARNING: "+l_file+" already exists and will be deleted!\n"
        delete_already_existed_file(l_file, message)
    for l_file in list_of_file_paths:
        message="ERROR: "+l_file+" already exists\n"
        is_already_existed_file(l_file, message)
        target_file = open(l_file, "w")
        for l_inc in range(1,current_config.THREADS+1):
            message="ERROR: "+l_file+"."+str(l_inc)+" does not exists\n"
            is_existed_file(l_file+"."+str(l_inc), message)
            shutil.copyfileobj(open(l_file+"."+str(l_inc), 'r'), target_file)
        target_file.close()  
            
#**************************************************************************#

def generate_template_for_CRF_and_test(list_of_template, current_config, config_end_user):
    #new_template_file = os.path.dirname(current_config.FEATURE_LIST[list_of_template[0]] ) + "+".join(list_of_template)
    #if len(list_of_template) > 1 :
    new_template_file = os.path.dirname(current_config.FEATURE_LIST[list_of_template[0]] ) + "/feature_selection/" + "+".join(list_of_template)
    #else:
      #new_template_file = os.path.dirname(current_config.FEATURE_LIST[list_of_template[0]] ) + list_of_template
    print (new_template_file)
    
    for l_keys in list_of_template:
      print (current_config.FEATURE_LIST[l_keys])
      
    with open(new_template_file, 'w') as outfile:
      for l_keys in list_of_template:
        with open(current_config.FEATURE_LIST[l_keys]) as infile:
          outfile.write(infile.read())
     
    demo_name = "System_WCE"
    script_path = config_end_user.TOOL_WAPITI
    train_file_path = current_config.TRAIN_FILE_PATH  + "_" + demo_name + ".txt"
    dev_file_path = current_config.DEV_FILE_PATH  + "_" + demo_name + ".txt"
    #template_path_pattern = current_config.TEMPLATE_PATH
    model_file_path_pattern = current_config.MODEL_PATH
    log_file_pattern = current_config.LOG_FILE_TRAINING_WAPITI 
    log_path = log_file_pattern + "_" + "+".join(list_of_template) + "_" + demo_name + ".txt"
    model_path = model_file_path_pattern + "_" + "+".join(list_of_template) + "_" + demo_name + ".txt"

    test_file_path = current_config.TEST_FILE_PATH  + "_" + demo_name + ".txt"
    
    list_of_commands = []
    # train the model

    command_line = script_path + " train -a sgd-l1 -i 200 -e 0.00005 -w 6 -p " + new_template_file + " " + train_file_path + " " + model_path  + " --nthread " +str(current_config.THREADS) + " 2>&1 | tee " + log_path
    print(command_line)
    list_of_commands.append(command_line)
    
    # test the model
    command_line = ""
    
    #model_path = model_file_path_pattern + str(order_of_template) + "_" + demo_name + ".txt"
    result_file_path = test_file_path + "_" + "+".join(list_of_template) + "_" + demo_name + ".result" 
    log_path = test_file_path + "_" + "+".join(list_of_template) + "_" + demo_name + ".log"

    command_line = script_path + " label -c -s -p " + test_file_path + " -m " + model_path + " " + result_file_path + " 2>&1 | tee " + log_path

    #For writing log file
    #command_line += model_path 
    #command_line += model_path + " " + result_file_path

    #print("Demo: " + demo_name + " - Testing with template " + str(order_of_template))
    print(command_line)

    #khong chay duoc khi chay truc tiep --> ERROR: "error: too much input files on command line"
    #call_script(command_line, script_path)

    #list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
    list_of_oracle_label, list_of_wapiti_label = get_list_of_oracle_label_and_list_of_wapiti_label_from_result_wapiti_labeling(result_file_path)
    
    X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good = get_precision_recall_fscore_within_list(list_of_oracle_label, list_of_wapiti_label)
    
    
    line_separate = "-"*63
    file_writer = open(log_path, mode='a', encoding='utf-8')

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    str_baseline = "*** Template " + "+".join(list_of_template) + "_" + demo_name + " classifier Good/Bad:"
    print(str_baseline)
    file_writer.write(str_baseline)
    file_writer.write("\n")

    #B
    str_B_baseline = "X-Bad = %d \t Y-Bad = %d \t Z-Bad = %d" %(X_bad, Y_bad, Z_bad)
    print(str_B_baseline)
    file_writer.write(str_B_baseline)
    file_writer.write("\n")

    #G
    str_G_baseline = "X-Good = %d \t Y-Good = %d \t Z-Good = %d" %(X_good, Y_good, Z_good)
    print(str_G_baseline)
    file_writer.write(str_G_baseline)
    file_writer.write("\n")

    ##########################
    #B
    str_result = "B \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_bad, Rc_bad, F_bad)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #G
    str_result = "G \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_good, Rc_good, F_good)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    
    return Pr_bad, Rc_bad, F_bad, Pr_good, Rc_good, F_good
    #command_line += 

#**************************************************************************#

def get_result_testing_CRF_models_with_given_model_and_test(model_file_path, test_file_path, current_config, config_end_user):
    """
    Testing phase of labeling within CRF model with K number of model.

    :type demo_name: string
    :param demo_name: name of Demo. For example: System_1

    :type order_of_template: int
    :param order_of_template: order of template
    """

    #current_config = load_configuration()
    #config_end_user = load_config_end_user()

    command_line = ""
    #script_path = current_config.TOOL_WAPITI
    script_path = config_end_user.TOOL_WAPITI
    #model_file_path_pattern = current_config.MODEL_PATH
    #result_testing_wapiti_pattern = current_config.RESULT_TESTING_WAPITI
    log_file_pattern = current_config.LOG_FILE_TESTING_WAPITI
    #test_file_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"

    command_line = script_path + " label -c -s -p " + test_file_path + " -m " + model_file_path

    #model_path = model_file_path_pattern + str(order_of_template) + "_" + demo_name + ".txt"
    result_file_path = test_file_path + ".result" 
    log_path = test_file_path + ".log"

    #For writing log file
    command_line += model_path + " " + result_file_path + " 2>&1 | tee " + log_path
    #command_line += model_path + " " + result_file_path

    #print("Demo: " + demo_name + " - Testing with template " + str(order_of_template))
    print(command_line)

    #khong chay duoc khi chay truc tiep --> ERROR: "error: too much input files on command line"
    #call_script(command_line, script_path)

    list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)


    #######################################################################
    #Tinh bang 'tay'
    #Ket qua cua wapiti: result_file_path
    #tinh bang tay: output path:
    #log_path_manual = log_file_pattern + str(order_of_template) +  "_" + demo_name + "_manual.txt"
    #file_writer = open(log_path_manual, mode = 'w', encoding = 'utf-8')

    #lay danh sach oracle (list_of_oracle_label) va danh sach (list_of_wapiti_label)
    list_of_oracle_label, list_of_wapiti_label = get_list_of_oracle_label_and_list_of_wapiti_label_from_result_wapiti_labeling(result_file_path)

    line_separate = "-"*63

    #######################################################################
    #print(line_separate)
    #print(line_separate)
    #file_writer.write(line_separate)
    #file_writer.write("\n")
    #file_writer.write(line_separate)
    #file_writer.write("\n")
    #######################################################################

    #* classifier Good/Bad.
    X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good = get_precision_recall_fscore_within_list(list_of_oracle_label, list_of_wapiti_label)
    return F_bad,F_good

    #str_baseline = "*** Template_" + str(order_of_template) + "_" + demo_name + " classifier Good/Bad:"
    #print(str_baseline)
    #file_writer.write(str_baseline)
    #file_writer.write("\n")

    ##B
    #str_B_baseline = "X-Bad = %d \t Y-Bad = %d \t Z-Bad = %d" %(X_bad, Y_bad, Z_bad)
    #print(str_B_baseline)
    #file_writer.write(str_B_baseline)
    #file_writer.write("\n")

    ##G
    #str_G_baseline = "X-Good = %d \t Y-Good = %d \t Z-Good = %d" %(X_good, Y_good, Z_good)
    #print(str_G_baseline)
    #file_writer.write(str_G_baseline)
    #file_writer.write("\n")

    ###########################
    ##B
    #str_result = "B \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_bad, Rc_bad, F_bad)
    #print(str_result)
    #file_writer.write(str_result)
    #file_writer.write("\n")

    ##G
    #str_result = "G \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_good, Rc_good, F_good)
    #print(str_result)
    #file_writer.write(str_result)
    #file_writer.write("\n")

    ########################################################################
    #print(line_separate)
    #print(line_separate)
    #file_writer.write(line_separate)
    #file_writer.write("\n")
    #file_writer.write(line_separate)
    #file_writer.write("\n")
    ########################################################################

    #file_writer.close()
#**************************************************************************#

if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    path = get_absolute_path_current_module()
    print(path)

    #Generating merged features file for WMT15
    """
    #B1: copy all extracted features files to /var/data
    #B2: Run 3 dong code sau
    #B3: result is: CRF_tgt.column.merged_features_wmt15.txt
    list_of_file_paths = get_list_of_file_paths_not_included_nbestlist_and_asr()
    file_output_path = current_config.OUTPUT_MERGED_FEATURES_WMT15
    generating_merged_features_within_given_list_of_file_paths(list_of_file_paths, file_output_path)
    """

    """
    #Generating merged features file for WMT14 & WMT13
    #B1: copy all extracted features files to /var/data
    #B2: Run 3 dong code sau
    #B3: result is: CRF_tgt.column.merged_features_wmt14_wmt13.txt
    list_of_file_paths = get_list_of_file_paths_not_included_nbestlist_and_asr()
    file_output_path = current_config.OUTPUT_MERGED_FEATURES_WMT14_WMT13
    generating_merged_features_within_given_list_of_file_paths(list_of_file_paths, file_output_path)
    """

    print("OK")
