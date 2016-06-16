# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 14:23:59 2015
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

# This module contains the common functions that use for other modules

import re
import sys, traceback
import os

#**************************************************************************#
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from config.configuration import *
#from feature.common_functions import *
from feature.convert_character_utf8 import generate_output_format_column_within_encoding, sort_result_of_features_values_asr_by_list_of_id_sentences_asr, generate_output_format_row_within_encoding
from feature.functions_asr import detectErrorWord, parseGraph, pareSentenceNgram, partOfSpeech, calculateGraphEverageValue
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import is_existed_file, get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE, get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET, get_filename
from common_module.cm_script import create_script_temp, call_script, run_chmod
from common_module.cm_util import is_match, is_in_string, split_string_to_list_delimeter_comma
#**************************************************************************#
"""
diff -y A_S_R W_C_E > filediff.txt

diff -y output_format_column_within_encoding.txt ../corpus/preprocessing/output_preprocessing.col.src > filediff.txt
"""
def get_diff_asr_and_wce(file_asr_path, file_ref_path, file_output_path):
    """
    Getting the differences between ASR format-column and WCE format-column.

    :type file_asr_path: string
    :param file_asr_path: each line contains word within format column.

    :type file_ref_path: string
    :param file_ref_path: each line contains word within format column.

    :type file_output_path: string
    :param file_output_path: result of command diff

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    """
    if not os.path.exists(file_asr_path):
        raise TypeError('Not Existed file ASR format-column')

    if not os.path.exists(file_ref_path):
        raise TypeError('Not Existed file WCE format-column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ASR"
    is_existed_file(file_asr_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file corpus input WCE"
    is_existed_file(file_ref_path, str_message_if_not_existed)

    current_config = load_configuration()

    script_path = current_config.TOOL_DIFF

    #chmod execute for script
    run_chmod(script_path)

    command_line = script_path + " " + file_asr_path + " " + file_ref_path + " " + file_output_path

    print(command_line)

    #Run Script
    call_script(command_line, script_path)
#**************************************************************************#
"""
Cach fix loi: Khi co loi lech dong, den file output_preprocessing.src xem thu noi dung cua dong; roi tim den cot trong
file diff, output, value_col
"""
def feature_asr_after_sorting_and_diff_with_ref(file_asr_path, file_ref_path, file_features_asr_path, file_output_path):
    """
    Getting the differences between ASR format-column and WCE format-column.

    :type file_asr_path: string
    :param file_asr_path: each line contains word within format column.

    :type file_ref_path: string
    :param file_ref_path: each line contains word within format column.

    :type file_features_asr_path: string
    :param file_features_asr_path: each line contains id-sentence, word & other features' values within format column. For example: L01P1_P1-0_01,0,les,0.509947,-4.38473,1,0,0,0.48,DET:ART,C.

    :type file_output_path: string
    :param file_output_path: result of command diff

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    """
    if not os.path.exists(file_asr_path):
        raise TypeError('Not Existed file ASR format-column')

    if not os.path.exists(file_ref_path):
        raise TypeError('Not Existed file WCE format-column')
    """
    str_message_if_not_existed = "Not Existed file corpus input ASR"
    is_existed_file(file_asr_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file corpus input WCE"
    is_existed_file(file_ref_path, str_message_if_not_existed)

    current_config = load_configuration()

    #current_config.OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING
    #current_config.SRC_REF_TEST_FORMAT_COL
    #current_config.OUTPUT_FORMAT_COLUMN_RESULT_DIFF
    #get_diff_asr_and_wce(file_asr_path, file_ref_path, file_output_path)
    #get_diff_asr_and_wce( current_config.OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING, current_config.SRC_REF_TEST_FORMAT_COL, current_config.OUTPUT_FORMAT_COLUMN_RESULT_DIFF)
    file_result_diff_path = current_config.OUTPUT_FORMAT_COLUMN_RESULT_DIFF
    get_diff_asr_and_wce( file_asr_path, file_ref_path, file_result_diff_path)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_result_diff_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    """Thuat toan:
    col1    col2    col3
TH1 NULL    >       char : ghi output voi current_config.DEFAULT_FEATURES_VALUES_ASR, co the th.doi tuy thuoc vao s.lg g.tri features cua ASR

TH2 char    |       char : luu vao list_string_temp; neu dong tiep theo khong thuoc TH3 thi ghi ra output (tam thoi ghi ra feature cua item dau tien, ve sau tinh trung binh); nguoc lai, neu thuoc TH3 thi them vao list_string_temp; quay tiep dong tiep theo va xet voi TH3.

TH3 char    <       NULL
    """

    #is_string_matching_pattern(pattern = '(.*?)\t+ +([|<>])[\t ]*(.*)', text)
    pattern = '(.*?)\t+ +([|<>])[\t ]*(.*)'
    char_greater = ">" #current_config.DEFAULT_FEATURES_VALUES_ASR
    char_lower = "<"
    char_other = "|"
    pattern_char_greater = '(.*?)\t+ +(>)[\t ]*(.*)'
    pattern_char_lower = '(.*?)\t+ +(<)[\t ]*(.*)'
    pattern_char_other = '(.*?)\t+ +(|)[\t ]*(.*)'

    previous_sign_char = ""
    current_sign_char = ""
    str_output = ""
    current_index_of_list_features_asr = 0
    list_temp = []
    #num_sent_break = 187
    num_cur_sent = 0
    num_of_line_should_have = 0

    #lay gia tri cua cac features ASR
    list_features_asr = get_list_from_file(file_features_asr_path)

    for line in file_reader:
        """
        if num_sent_break > 0:
            num_sent_break -= 1
        else:
            break
        """
        num_cur_sent += 1

        if len(line.strip()) == 0: #xuong dong
            """
            week	| week-end
            end  |	.
            """
            if len(list_temp) != 0:
                str_output = list_temp[0]
                #str_output = "|||".join(list_temp)
                file_writer.write(str_output)
                file_writer.write("\n")
                previous_sign_char = ""
                current_sign_char = ""
                list_temp = []
            #end if

            current_sign_char = "Xuong Dong"
            print(current_sign_char + str(num_cur_sent))
            file_writer.write("\n")
            previous_sign_char = ""
            current_sign_char = ""
            num_of_line_should_have += 1
            continue
        #end if

        #kiem tra cau truc cua noi dung trong line, co chua: |<>
        #is_string_matching_pattern(pattern = '(.*?)\t+ +([|<>])[\t ]*(.*)', text)
        #pattern = '(.*?)\t+ +([|<>])[\t ]*(.*)'
        #result = is_string_matching_pattern(pattern, line)
        result = is_match(pattern, line)

        #is_in_string(word, my_string)
        str_output = ""
        if result:
            if is_match(pattern_char_greater, line):#is_in_string(char_greater, line): #>
                """
                    maître	 |	,
							     >	me
                """
                if len(list_temp) != 0:
                    str_output = list_temp[0]
                    #str_output = "|||".join(list_temp)
                    file_writer.write(str_output)
                    file_writer.write("\n")
                    previous_sign_char = ""
                    current_sign_char = ""
                    list_temp = []
                #end if

                current_sign_char = char_greater
                print(current_sign_char + str(num_cur_sent))
                str_output = current_config.DEFAULT_FEATURES_VALUES_ASR
                file_writer.write(str_output)
                file_writer.write("\n")
                previous_sign_char = ""
                current_sign_char = ""
                list_temp = []
                num_of_line_should_have += 1

            elif is_match(pattern_char_lower, line):#is_in_string(char_lower, line): #<
                current_sign_char = char_lower
                print(current_sign_char + str(num_cur_sent))

                if previous_sign_char == char_other or previous_sign_char == char_lower:
                    list_temp.append(list_features_asr[current_index_of_list_features_asr])
                    current_index_of_list_features_asr += 1
                    previous_sign_char = char_lower
                else:
                    str_output = list_temp[0]
                    file_writer.write(str_output)
                    file_writer.write("\n")
                    previous_sign_char = ""
                    current_sign_char = ""
                    list_temp = []
                    num_of_line_should_have += 1
                #end if

            elif is_match(pattern_char_other, line):#is_in_string(char_other, line): #|
                """
                    venir       venir
                    a    | a-t-il
                    t    <
                    il   <
                    dix         dix
                """
                current_sign_char = char_other
                print(current_sign_char + str(num_cur_sent))

                if previous_sign_char == char_other: #|
                    str_output = list_temp[0]
                    file_writer.write(str_output)
                    file_writer.write("\n")
                    previous_sign_char = ""
                    list_temp = []
                #end if

                list_temp.append(list_features_asr[current_index_of_list_features_asr])
                current_index_of_list_features_asr += 1
                previous_sign_char = char_other
        else:
            current_sign_char = "Khong co"
            print(current_sign_char + str(num_cur_sent))
            #neu len(list_temp) != 0 thi ghi phan tu do ra ngoai roi lam tiep; trong truong hop chi chua 1 dong co |
            #tam thoi chi ghi output phan tu dau tien trong list_temp
            #version 2: Nen tao lop chua cac features va Nen tinh trung binh tat ca cac thuoc tinh thuoc so thuc;
            if len(list_temp) != 0:
                str_output = list_temp[0]
                #str_output = "|||".join(list_temp)
                file_writer.write(str_output)
                file_writer.write("\n")
                previous_sign_char = ""
                current_sign_char = ""
                list_temp = []
            #end if

            str_output = list_features_asr[current_index_of_list_features_asr]
            current_index_of_list_features_asr += 1
            file_writer.write(str_output)
            file_writer.write("\n")
            previous_sign_char = ""
            current_sign_char = ""
            list_temp = []
        #end if
    #end for

    #close files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
#B1: Tach cac gia tri cua features-ASR thanh list 2 chieu. Co nghia la: list_of_sentences; trong moi item cua cau chua list_of_word_features_values_asr
"""features' values of ASR in SOURCE LANGUAGE
L01P1_P1-0_01,0,les,0.509947,-4.38473,1,0,0,0.48,DET:ART,C.
L01P1_P1-0_01,1,chirurgiens,0.509947,-10.6568,2,1,0,0.11,NOM,C.
L01P1_P1-0_01,2,de,0.959214,-3.60662,2,2,-0.120692,0.22,PRP,C.
L01P1_P1-0_01,3,los,0.99977,-8.16717,2,2,-0.0687971,0.12,NOM,C.
L01P1_P1-0_01,4,angeles,1,-0.129242,3,2,0,0.24,NOM,C.
id_sent,0,punct,1,0,1,0,0,1,PUN,K.
L01P1_P1-0_01,5,on,0.509947,-5.21787,3,2,0,0.12,PRO:PER,E.
L01P1_P1-0_01,6,dit,0.501642,-5.06882,2,2,-0.123516,0.17,VER:pres,C.
L01P1_P1-0_01,7,qu',0.509947,-2.81294,3,2,0,0.42,VER:pper,C.
L01P1_P1-0_01,8,ils,0.997299,-2.54621,3,2,0,0.11,PUN,C.
L01P1_P1-0_01,9,étaient,1,-3.91892,3,2,0,0.22,PRO:PER,C.
L01P1_P1-0_01,10,outre,1,-9.73318,1,2,-0.768761,0.22,VER:cond,E.
id_sent,0,punct,1,0,1,0,0,1,PUN,K.
L01P1_P1-0_01,11,a,0.509947,-5.2968,2,1,0,0.22,ADV,C.
L01P1_P1-0_01,12,déclaré,0.99949,-3.51804,2,2,-0.194829,0.22,VER:pres,C.
L01P1_P1-0_01,13,m,0.509947,-4.36005,3,2,0,0.22,NOM,E.
L01P1_P1-0_01,14,se,0.701737,-5.8452,2,2,-0.15911,0.22,VER:simp,E.
L01P1_P1-0_01,15,camus,0.509947,-12.7847,1,2,-1.06601,0.22,PRO:PER,C.
id_sent,0,punct,1,0,1,0,0,1,PUN,K.
"""
def get_list_of_sentences_features_values_asr(file_input_path):
    """
    Getting the list of sentences whose items contains list of features' values of ASR.

    :type file_input_path: string
    :param file_input_path: result of command diff

    :rtype: list of sentences

    :raise ValueError: if any path is not existed
    """
    # check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file result of command diff')
    """
    str_message_if_not_existed = "Not Existed file corpus input that is result of command diff"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #for reading: file_output_from_moses_included_alignment_word_to_word_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    result = []
    list_of_words = []
    is_appended = False

    for line in file_reader:
        line = line.strip()

        if len(line) == 0: #xuong dong
            #them list of features' values of ASR vao list_of_sentences
            result.append(list_of_words)
            is_appended = True
            list_of_words = []
            continue
        #end if

        list_of_words.append(line)
        is_appended = False
    #end for

    if is_appended == False:
        #them list of features' values of ASR vao list_of_sentences
        result.append(list_of_words)
    #end if

    return result
#**************************************************************************#
"""Phuong phap:
B1: Tach cac gia tri cua features-ASR thanh list 2 chieu. Co nghia la: list_of_sentences; trong moi item cua cau chua list_of_word_features_values_asr

B2: Dua vao alignment cua moses chung ta co the biet duoc cac yeu cau cua bai toan. Sau do, ghi ket qua vao file output
"""
"""output 1-best-list of MOSES 2009
#0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
"""
"""features' values of ASR in SOURCE LANGUAGE
L01P1_P1-0_01,0,les,0.509947,-4.38473,1,0,0,0.48,DET:ART,C.
L01P1_P1-0_01,1,chirurgiens,0.509947,-10.6568,2,1,0,0.11,NOM,C.
L01P1_P1-0_01,2,de,0.959214,-3.60662,2,2,-0.120692,0.22,PRP,C.
L01P1_P1-0_01,3,los,0.99977,-8.16717,2,2,-0.0687971,0.12,NOM,C.
L01P1_P1-0_01,4,angeles,1,-0.129242,3,2,0,0.24,NOM,C.
id_sent,0,punct,1,0,1,0,0,1,PUN,K.
L01P1_P1-0_01,5,on,0.509947,-5.21787,3,2,0,0.12,PRO:PER,E.
L01P1_P1-0_01,6,dit,0.501642,-5.06882,2,2,-0.123516,0.17,VER:pres,C.
L01P1_P1-0_01,7,qu',0.509947,-2.81294,3,2,0,0.42,VER:pper,C.
L01P1_P1-0_01,8,ils,0.997299,-2.54621,3,2,0,0.11,PUN,C.
L01P1_P1-0_01,9,étaient,1,-3.91892,3,2,0,0.22,PRO:PER,C.
L01P1_P1-0_01,10,outre,1,-9.73318,1,2,-0.768761,0.22,VER:cond,E.
id_sent,0,punct,1,0,1,0,0,1,PUN,K.
L01P1_P1-0_01,11,a,0.509947,-5.2968,2,1,0,0.22,ADV,C.
L01P1_P1-0_01,12,déclaré,0.99949,-3.51804,2,2,-0.194829,0.22,VER:pres,C.
L01P1_P1-0_01,13,m,0.509947,-4.36005,3,2,0,0.22,NOM,E.
L01P1_P1-0_01,14,se,0.701737,-5.8452,2,2,-0.15911,0.22,VER:simp,E.
L01P1_P1-0_01,15,camus,0.509947,-12.7847,1,2,-1.06601,0.22,PRO:PER,C.
id_sent,0,punct,1,0,1,0,0,1,PUN,K.
"""
#DEFAULT_FEATURES_VALUES_ASR_NOT_HAVE_ALIGNMENT
def feature_asr_alignment_target_to_source(file_output_from_moses_included_alignment_word_to_word_path, file_feature_asr_after_sorting_and_diff_with_ref, default_value_not_have_alignment, file_output_path):
    """
    Getting the features' values of ASR format-column that is aligned from target to source.

    :type file_output_from_moses_included_alignment_word_to_word_path: string
    :param file_output_from_moses_included_alignment_word_to_word_path: the ouput included alignment word to word from target to source (MOSES format)

    :type file_feature_asr_after_sorting_and_diff_with_ref: string
    :param file_feature_asr_after_sorting_and_diff_with_ref: result of command diff

    :type default_value_not_have_alignment: string
    :param default_value_not_have_alignment: value in file config

    :type file_output_path: string
    :param file_output_path: each line contains features' values of ASR

    :raise ValueError: if any path is not existed
    """
    # check existed paths
    """
    if not os.path.exists(file_output_from_moses_included_alignment_word_to_word_path):
        raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

    if not os.path.exists(file_feature_asr_after_sorting_and_diff_with_ref):
        raise TypeError('Not Existed file result of command diff.')
    """
    str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path"
    is_existed_file(file_output_from_moses_included_alignment_word_to_word_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file result of command diff"
    is_existed_file(file_feature_asr_after_sorting_and_diff_with_ref, str_message_if_not_existed)

    #B1: Tach cac gia tri cua features-ASR thanh list 2 chieu. Co nghia la: list_of_sentences; trong moi item cua cau chua list_of_word_features_values_asr
    #get_list_of_sentences_features_values_asr(file_input_path)
    list_of_sentences_asr = get_list_of_sentences_features_values_asr(file_feature_asr_after_sorting_and_diff_with_ref)

    #for reading: file_output_from_moses_included_alignment_word_to_word_path
    file_reader_output_from_moses = open(file_output_from_moses_included_alignment_word_to_word_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
    number_of_sentence = 1
    #delimiter_char = "|||"
    str_not_having_alignment = default_value_not_have_alignment

    for line_in_output_moses in file_reader_output_from_moses:
        #list_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
        #trim string
        line_in_output_moses = line_in_output_moses.strip()

        if len(line_in_output_moses) == 0:
            print("Xuat hien dong trong - Empty line ... You should check corpus...")
            print("Xem lai cau %d nha!!!???" %number_of_sentence)
            continue

        #Duyet Tung cau dich va cau moses va xet
        #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
        #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_moses) #version 1 - Target - Source _ nhom cuoi cua MOSES output
        #updated 2015.Jan.06 by Tien LE

        #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)
        config_end_user = load_config_end_user()
        list_alignment_target_to_source = []

        if config_end_user.VERSION_MOSES == 2009:
            list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(line_in_output_moses)
        else:
            list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)

        """
        print("*list_alignment_target_to_source*")
        print(list_alignment_target_to_source)
        print("*list_alignment_target_to_source*")
        """

        #source language
        #number_of_sentence = 1
        id_sentence =number_of_sentence - 1
        list_of_words_source = list_of_sentences_asr[id_sentence]

        #xu ly danh sach ket qua
        #0  1  2    3  ... n-1
        #0  1  2,3  '' ....    #'' co nghia la khong co phan tu nao lien ket, list_alignment_target_to_source
        #1  2  3,2  0  ....   #list_longest_source_gram_length
        comma_char = ","

        #raise Exception("Just for testing ... :) ")
        #den day la ok doi voi version 2, co nghia la: hieu nhom cuoi cua MOSES output la Source to Target

        #xet danh sach cac phan tu ket noi tu dich den nguon
        #xet tung tu trong danh sach tu dich
        for i in range(len(list_alignment_target_to_source)):
            index_alignment_to_source = list_alignment_target_to_source[i]

            """
            print("*index_alignment_to_source**********************")
            print(index_alignment_to_source)
            print("*index_alignment_to_source**********************")
            """
            #index cua tu nguon duoc giong den
            index_alignment_of_source_word = -1 #khong co tu nao giong den

            list_temp = [] # empty list

            #lay chuoi ra, neu chua dau phay ,
            if is_in_string(comma_char, index_alignment_to_source): #co tu 2 lien ket voi nguon tro len
                list_temp = index_alignment_to_source.split(comma_char)
                index_alignment_of_source_word = int(list_temp[0]) #chi can xet tu dau tien duoc giong len Source

            else: #neu chi la 1 so nguyen, khong chua dau phay , co nghia la: chi chua 1 phan tu
                list_temp.append(str(index_alignment_to_source))
                try:
                    index_alignment_of_source_word = int(index_alignment_to_source)
                except ValueError:
                    pass #index_alignment_of_source_word = index_alignment_to_source #neu chua "" thi bi loi cho nay
                #end try
            #end if

            #index_of_target_word = i #index cua tu dich

            if index_alignment_of_source_word == -1:
                #ghi gia tri mac dinh
                line_output = str_not_having_alignment
            else:
                line_output = list_of_words_source[index_alignment_of_source_word]
            #end if

            #ghi ra file output voi format la column
            file_writer.write(line_output)
            file_writer.write("\n") # new line
            """
            print("*line_output*")
            print(line_output)
            print("*line_output*")
            """
        #end for

        #print("Da xu ly xong cau thu %d" %number_of_sentence)
        number_of_sentence = number_of_sentence + 1
        file_writer.write("\n") # new line for new sentence

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
    #end for

    #close files
    file_reader_output_from_moses.close()

    #for writing: file_output_path
    file_writer.close()
#**************************************************************************#
def filter_feature_asr(file_input_path, file_output_path):
    """
    Filter the result of feature ASR.

    For example: Note: output - not containing 3 items which have index 0, 1, n-1
    input: L15P5_P5-3_45,0,en,1,-4.37061,1,0,0,0.25,PRP,C.
    output: en \t 1 \t -4.37061 \t 1 \t 0 \t 0 \t 0.25 \t PRP

    :type file_input_path: string
    :param file_input_path: each line contains features' values of ASR. For example: L15P5_P5-3_45,0,en,1,-4.37061,1,0,0,0.25,PRP,C.

    :type file_output_path: string
    :param file_output_path: each line contains features' values of ASR after filtering. Note: output - not containing 3 items which have index 0, 1, n-1. For example: output: en \t 1 \t -4.37061 \t 1 \t 0 \t 0 \t 0.25 \t PRP

    :raise ValueError: if any path is not existed
    """
    # check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file that contains features-values of ASR')
    """
    str_message_if_not_existed = "Not Existed file corpus input that contains features-values of ASR"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #for reading:
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing:
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    for line in file_reader:
        line = line.strip()
        if len(line) == 0:
            #xuong dong
            file_writer.write("\n")
            continue
        #end if

        items = split_string_to_list_delimeter_comma(line)

        #Note: output - not containing 3 items which have index 0, 1, n-1
        #L15P5_P5-3_45,0,en,1,-4.37061,1,0,0,0.25,PRP,C.
        str_output = ""
        list_output = []
        if len(items) <= 3:
            raise Exception("You should check result of features-values of ASR BEFORE filtering.")
        #end if

        num_of_items = len(items)
        for i in range(num_of_items):
            if i == 0 or i == 1 or i == num_of_items:
                continue #khong dua ra file output
            else:
                list_output.append(items[i].strip())
        #end for

        str_output = "\t".join(list_output)

        #ghi ra file output
        file_writer.write(str_output)
        file_writer.write("\n")
    #end for

    #close files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def get_feature_asr():
    current_config = load_configuration()

    #cac buoc sau can xem chi tiet o convert_character_utf8.py
    #Buoc 1: Sort theo list of id-sentence
    #AFTER_SORTING_FEATURES_VALUES_ASR_PATH
    #sort_result_of_features_values_asr_by_list_of_id_sentences_asr(file_input_path, file_list_of_id_sentences_asr, file_output_path)
    sort_result_of_features_values_asr_by_list_of_id_sentences_asr( current_config.FEATURES_VALUES_ASR_PATH, current_config.LIST_OF_ID_SENTENCES_ASR, current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH)

    #Buoc 2: generate_output_format_column_within_encoding
    #OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING
    #generate_output_format_column_within_encoding(file_input_path, file_output_path)
    generate_output_format_column_within_encoding( current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH, current_config.OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING)
    #output: les

    #Tao file chua gia tri cua cac features cua ASR
    #OUTPUT_FORMAT_ROW_WITHIN_ENCODING
    #generate_output_format_row_within_encoding(file_input_path, file_output_path)
    generate_output_format_row_within_encoding( current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH, current_config.OUTPUT_FORMAT_ROW_WITHIN_ENCODING)
    #output: L01P1_P1-0_01,0,les,0.509947,-4.38473,1,0,0,0.48,DET:ART,C.

    ##current_config.OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING
    #current_config.SRC_REF_TEST_FORMAT_COL
    #current_config.OUTPUT_FORMAT_ROW_WITHIN_ENCODING
    #current_config.FEATURES_ASR_NOT_ALIGNMENT
    feature_asr_after_sorting_and_diff_with_ref(current_config.OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING, current_config.SRC_REF_TEST_FORMAT_COL, current_config.OUTPUT_FORMAT_ROW_WITHIN_ENCODING, current_config.FEATURES_ASR_NOT_ALIGNMENT)

    #DEFAULT_FEATURES_VALUES_ASR_NOT_HAVE_ALIGNMENT
    #feature_asr_alignment_target_to_source(file_output_from_moses_included_alignment_word_to_word_path, file_feature_asr_after_sorting_and_diff_with_ref, default_value_not_have_alignment, file_output_path)
    feature_asr_alignment_target_to_source( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.FEATURES_ASR_NOT_ALIGNMENT, current_config.DEFAULT_FEATURES_VALUES_ASR_NOT_HAVE_ALIGNMENT, current_config.FEATURES_ASR_ALIGNED)

    #filter_feature_asr(file_input_path, file_output_path)
    filter_feature_asr( current_config.FEATURES_ASR_ALIGNED, current_config.FEATURES_ASR_ALIGNED_LAST)
#**************************************************************************#
"""
Usage: sh run.sh <Hyp_File> <Ref_File> <Lattice_Dir> <Output_formate [table,csv]> [-cluster <Number_process>]
Options: -cluster number_of_process: using cluster to run the script. !!!Note, log into cluster server is need.

*** Buoc 1:
# load variables
# tools configuration
#-------------------
LATTICE_TOOL="/home/lecouteu/Srilm/bin/i686-m64/lattice-tool"
GETPRO="/home/lecouteu/KALDI.V2/fst2slf/bentoolkit/lm/bin/getprob"
TREETAGGER="/home/kaing/TreeTagger/cmd/tree-tagger-french"



# models configuration
#---------------------
#lm="/home/lecouteu/KALDI.V2/exp/nnet5c/decode_dev_ant_2g/out_myconvert/"
#base_name="BigLM4"
lm="/home/lecouteu/KALDI.FR/exp_full_big/sgmm2_5b2_mixedubm_big/decode_bref/"
base_name="nouveaumodele"
lmscale="10"
acscale="0"


# label name
#--------------------
GOODLABEL="C"
BADLABEL="E"


# table formate configuration
#---------------------
print_template="{0:20}{1:12}{2:15}{3:12}{4:12}{5:15}{6:12}{7:12}{8:15}{9:12}{10:12}{11:12}"


# the temporary file name, to avoid conflict with other file. !!not important
#--------------------
tmp_file_name="list"

script_dir=$(dirname $0) #thu muc chinh
libs=$script_dir/libs #thu muc chua cac lib can su dung
sclite_files=$script_dir/sclite_files #thu muc chua ket qua "compute-sclite"

Them vao script: path to sclite
export PATH=/home/lent/Develops/Solution/ce_agent/tool/sctk-2.4.9/bin:$PATH

*** Buoc 2: VD: sh run.sh 10.tramots test.refASR HTK_fr/ csv
hyp_path=$1
ref_path=$2
lat_dir=$3
format=$4
compute-sclite -h $hyp_path -r $ref_path -o all -O $sclite_files

*** Buoc 3: ??? y nghia
#pra_path=$sclite_files/$(basename $hyp_path).pra
pra_filename = get_filename(hyp_path) #chu y co doi la pra
pra_path = $sclite_files/pra_filename


*** Buoc 4: Neu dung cluster (mac dinh - Bo qua)
if [ $# -gt 4 ];
then
	if [ $# -lt 6 ] || [ $5 != "-cluster" ];
	then
		echo "Usage: sh run.sh <Hyp_File> <Lattice_Dir> <PRA_File> [-cluster <Number_process>]" >&2
        	echo >&2
		echo "Options:" >&2
       		echo "-cluster number_of_process: using cluster to run the script. !!!Note, log into cluster server is need." >&2
		echo >&2
        	exit 1
	fi
	echo "Cluster mode runing..." >&2
	echo " -> $libs/cluster.sh $6 $hyp_path $lat_dir $pra_path $format"
	sh $libs/cluster.sh $6 $hyp_path $lat_dir $pra_path $format
	exit 1
fi

*** Buoc 5: Sequecial runing...
sh $libs/extract_feature.sh $lat_dir $pra_path $hyp_path $format 1>> $script_dir/out.txt 2>> $script_dir/log.txt

Usage: extract_feature <GRAPH_PATH> <PRA_FILE> <INPUT_FILE> <Output_formate [table,csv]>

graph_path=$1 #duong dan den thu muc chua lattice
pra_file=$2 #duong dan den file pra
list_file=$3 #file hyp_path
format=$4 #csv

while IFS= read line; # read user pass uid gid full home shell
do
    trans_id=$(echo $line | cut -d" " -f1)
    sentence=$(echo $line | cut -d" " -f2-)
    graph_file=$(ls $graph_path | grep -i $trans_id".lat$")
    if [ $format == "csv" ];
    then
        python $libs/boonzaiboostFormat.py $graph_path$graph_file $trans_id $pra_file $sentence
    elif [ $format == "table" ];
    then
        python $libs/tableFeatureFormat.py $graph_path$graph_file $trans_id $pra_file $sentence
    fi
done < $list_file
"""
#**************************************************************************#
def run_test_asr(hypothesis_asr_path, reference_asr_path, file_output_path):
    """
    Running testing ASR
    input:
        hypothesis file, for example: L01P1_P1-0_01 les chirurgiens de los angeles on dit qu' ils e1taient outre a de1clare1 m se camus
        reference file, for example: L01P1_P1-0_01 les chirurgiens de los angeles ont dit qu' ils e1taient outre1s a de1clare1 monsieur camus
        lattice_directory_path, for example: HTK_lat/
        format type: csv or table

    output: file within format csv that contains the lines which is like "L01P1_P1-0_01, les, 0.509947, -4.38473, 1, 0, 0, 0.48, DET:ART, C."
    """
    #output: FEATURES_VALUES_ASR_PATH
    #command: compute-sclite -h $hyp_path -r $ref_path -o all -O $sclite_files
    current_config = load_configuration()
    config_end_user = load_config_end_user()
    list_of_commands = []

    #script_path = current_config.TOOL_COMPUTE_SCLITE
    script_path = config_end_user.TOOL_COMPUTE_SCLITE

    #chmod execute for script
    run_chmod(script_path)

    #nen de duong dan o config_end_user roi cong vao day !!!
    #command_line = "export PATH=/home/lent/Develops/Solution/ce_agent/tool/sctk-2.4.9/bin:/home/lent/Develops/DevTools/srilm-1.7.1/bin/i686-m64:$PATH"
    command_line = "export " + config_end_user.PATH_TO_SENDID_TO_SCLITE
    list_of_commands.append(command_line)

    sclite_files_directory_path = current_config.SCLITE_FILES_DIRECTORY_PATH

    command_line = script_path + " -h " + hypothesis_asr_path + " -r " + reference_asr_path + "  -o all -O " + sclite_files_directory_path
    list_of_commands.append(command_line)

    print(command_line)

    ##Generate Shell Script
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)

    #pra_filename = get_filename(hyp_path) #chu y co doi la pra
    pra_filename = get_filename(hypothesis_asr_path) + ".pra"

    #pra_path = $sclite_files/pra_filename
    pra_path = sclite_files_directory_path + pra_filename

    print("pra_path-BEGIN")
    print(pra_path)
    print("pra_path-END")

    #check existed paths
    """
    if not os.path.exists(pra_path):
        raise TypeError('You should check the result of tool sclite!!!')
    #end if
    """
    str_message_if_not_existed = "Not Existed file corpus input that is output of tool sclite"
    is_existed_file(pra_path, str_message_if_not_existed)

    #Duyet tung cau trong hyp_file
    #tach id_sentence va content_sentence
    #kiem tra graph file co ton tai hay khong. Neu khong co thi warning: file_name = id_sentence.lat
    #Goi ham: python $libs/boonzaiboostFormat.py $graph_path$graph_file $trans_id $pra_file $sentence
    #         python boonzaiboostFormat.py graph_file_path id_sentence pra_file_path content_sentence
    #echo "Sequecial runing..." >&2
    #sh $libs/extract_feature.sh $lat_dir $pra_path $hyp_path $format 1>> $script_dir/out.txt 2>> $script_dir/log.txt
    #for reading: file_input_path
    file_reader = open(hypothesis_asr_path, mode = 'r', encoding = 'utf-8')

    index_sentence_begin = 0
    index_sentence_end = 0 #neu bang 0, thi test toan bo du lieu; neu duong va khac 0 thi test so luong cau han chi
    index_current_sentence_execute = 0

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

        ############################
        #just for testing ... BEGIN
        if index_sentence_end == 0:
            pass
        elif index_current_sentence_execute >= index_sentence_begin and index_current_sentence_execute <= index_sentence_end:
            index_current_sentence_execute += 1
        else:
            raise Exception("Just for testing... From index-sentence %d to index-sentence %d" %(index_sentence_begin, index_sentence_end))
        #end if
        #just for testing ... END
        ############################

        items = line.split() #split within default = " "
        id_sentence = items[0]
        list_content_sentence = []
        for i in range(len(items)):
            if i != 0:
                list_content_sentence.append(items[i])
            #end if
        #end for
        content_sentence = " ".join(list_content_sentence)

        #graph_file_path = current_config.LATTICE_DIRECTORY_PATH + id_sentence + ".lat"
        graph_file_path = config_end_user.LATTICE_DIRECTORY_PATH + id_sentence + ".lat"

        #check existed paths
        if not os.path.exists(graph_file_path):
            #raise TypeError('You should check file graph for sentence id = %s !!!' %id_sentence)
            print('You should check file graph for sentence id = %s !!! at path: %s' %(id_sentence, graph_file_path))
        #end if

        boonzaiboostFormat(graph_file_path, id_sentence, pra_path, content_sentence, file_output_path)

    #end for

    #close file
    file_reader.close()

#**************************************************************************#
#================================================================= Showing Information
def boonzaiboost_Format_original(graph_path, sentence_id, pra_path, sentence):
    current_config = load_configuration()

    lm = current_config.LM_ASR
    base_name = current_config.BASE_NAME
    lmscale = current_config.LMSCALE
    GoodLabel= current_config.LABEL_GOOD
    BadLabel = current_config.LABEL_BAD

    NO_BALI_INDEX=1
    WORD_INDEX=0
    try:
        sys.stderr.write("id:"+sentence_id+"\n")
        sys.stderr.write("Calculating words state...\n")
        if pra_path:
            #word_error_dict = functions.detectErrorWord(pra_path)
            word_error_dict = detectErrorWord(pra_path)
        #end if

        sys.stderr.write("Calculating posterior probability for each words...\n")
        #[graph, word_length_list] = functions.parseGraph(graph_path, sentence, lmscale)
        [graph, word_length_list] = parseGraph(graph_path, sentence, lmscale)
        sys.stderr.write("Calculating ngram info...\n")
        #(ngram, logprob, ppl, ppl1) = functions.pareSentenceNgram(sentence, lm+" "+base_name)
        (ngram, logprob, ppl, ppl1) = pareSentenceNgram(sentence, lm+" "+base_name)
        sys.stderr.write("Reading ctm file...\n")
        sys.stderr.write("Computing part of speech...\n")
        #part_of_speech_list=functions.partOfSpeech(sentence)
        part_of_speech_list = partOfSpeech(sentence)
        sys.stderr.write("Showing information...\n")
        ################################## format: word, *logprob, *ppl, *ppl1, postPr, log, *log10, *sum, *log10, ngram, Ucon, Bo, length, POS, state
        for word in filter(None, (sentence).split()):
            col=[]
            col.append(word)		# word column
            #col.append(str(logprob))	# logprob column
            #col.append(str(ppl))		# perplexity log(ppl)  column
            #col.append(str(ppl1))		# perplexity log 1(ppl1) column
            #col.append(graph[WORD_INDEX][1] if len(graph) > WORD_INDEX and str(graph[WORD_INDEX][1]) != "?" else str(functions.calculateGraphEverageValue(graph)))                # posterior probability(postPr) column
            col.append(graph[WORD_INDEX][1] if len(graph) > WORD_INDEX and str(graph[WORD_INDEX][1]) != "?" else str(calculateGraphEverageValue(graph)))                # posterior probability(postPr) column
            col.append(ngram[word][0].split("=")[1] if word in ngram else "")					# log column
            #col.append(ngram[word][1].split("=")[1][:-1] if word in ngram else "")					# log10 column
            #col.append(filter(None, ngram[word][2].split(" "))[0].split("=")[1] if word in ngram else "")		# sum column
            #col.append(filter(None, ngram[word][2].split(" "))[1].split("=")[1][:-1] if word in ngram else "")	# log10(sum) column
            col.append(ngram[word][3].split(" ")[1] if word in ngram else "") # ngram column
            col.append(ngram[word][4].split(" : ")[1][1:-2] if word in ngram else "") # used context(Ucon) column
            col.append(ngram[word][5].split(" : ")[1][:-2] if word in ngram else "") # back off probability column
            if word != "<s>" and word != "</s>":
                #col.append(word_length_list[WORD_INDEX] if len(word_length_list) > WORD_INDEX and str(word_length_list[WORD_INDEX]) != "?" else str(functions.calculateWordLengthEverageValue(word_length_list))[:4]) # word length column
                col.append(word_length_list[WORD_INDEX] if len(word_length_list) > WORD_INDEX and str(word_length_list[WORD_INDEX]) != "?" else str(calculateWordLengthEverageValue(word_length_list))[:4]) # word length column

                col.append(part_of_speech_list[NO_BALI_INDEX-1][1]) # part of speech column

            #not yet test the case of deletion
            if pra_path: # state column
                tmp_word_ele=word_error_dict[sentence_id.lower()][NO_BALI_INDEX].split(" ")
                if re.match("\*+", tmp_word_ele[1]):
                    col.append(BadLabel)
                elif tmp_word_ele[0] != tmp_word_ele[1]:
                    col.append(BadLabel)
                elif tmp_word_ele[0] == tmp_word_ele[1]:
                    col.append(GoodLabel)
                else:
                    col.append(BadLabel)
            else:
                col.append("C")
                NO_BALI_INDEX+=1
        else:
            col.append("") # word length column
            col.append("")	 # part of speech column
            col.append("?") # state column
        #end if

        WORD_INDEX+=1
        if len(col) != 9:
            sys.stderr.write("Error: \""+sentence_id+"\" row number "+str(NO_BALI_INDEX)+" lack of attribute.\nAttribute number:  "+str(len(col)))
            print(sentence_id+", "+", ".join(col)+".")
        #print "\n"
        sys.stderr.write("Done "+sentence_id+"\n")
    except:
        #sys.stderr.write("\nError Command: python "+libs+"/boonzaiboostFormat.py "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4]+" "+' '.join(sys.argv[5:])+"\n")
        sys.stderr.write("\nError Command: python boonzaiboostFormat.py ")

        traceback.print_exc(file=sys.stdout)
    #end try
#**************************************************************************#
def boonzaiboostFormat(graph_path, sentence_id, pra_path, sentence, file_output_path):
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    """
    lm = current_config.LM_ASR
    base_name = current_config.BASE_NAME
    lmscale = current_config.LMSCALE
    """
    lm = config_end_user.LM_ASR
    base_name = config_end_user.BASE_NAME
    lmscale = config_end_user.LMSCALE
    GoodLabel= current_config.LABEL_GOOD #G
    BadLabel = current_config.LABEL_BAD #B

    NO_BALI_INDEX=1
    WORD_INDEX=0

    #open file output for appending
    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

    sys.stderr.write("id:"+sentence_id+"\n")
    sys.stderr.write("Calculating words state...\n")

    word_error_dict = {} #empty dictionary
    if pra_path:
        #word_error_dict = functions.detectErrorWord(pra_path)
        word_error_dict = detectErrorWord(pra_path)
    #end if


    sys.stderr.write("Calculating posterior probability for each words...\n")
    #[graph, word_length_list] = functions.parseGraph(graph_path, sentence, lmscale)
    #Sentence_id, so tu, starting time, duration, word, posterior probability
    #hien tai:
    #graph: [word, posterior probability] For example: ['chirurgiens', '?'] hay ['chirurgien', '0.959214']
    #word_length_list: [duration] For example: 0.48
    [graph, word_length_list] = parseGraph(graph_path, sentence, lmscale)

    #raise Exception("Just for testing... End of task: Calculating posterior probability for each words...")

    sys.stderr.write("Calculating ngram info...\n")
    #(ngram, logprob, ppl, ppl1) = functions.pareSentenceNgram(sentence, lm+" "+base_name)
    (ngram, logprob, ppl, ppl1) = pareSentenceNgram(sentence, lm + " " + base_name)

    print("ngram:BEGIN")
    for item in ngram:
        print(item)
    print("ngram:END")

    #raise Exception("Just for testing... End of task: Calculating ngram info...")

    sys.stderr.write("Reading ctm file...\n")
    sys.stderr.write("Computing part of speech...\n")
    #part_of_speech_list=functions.partOfSpeech(sentence)
    part_of_speech_list = partOfSpeech(sentence)

    print("part_of_speech_list:BEGIN")
    for item in part_of_speech_list:
        print(item)
    print("part_of_speech_list:END")

    #raise Exception("Just for testing... End of task: Computing part of speech...")

    sys.stderr.write("Showing information...\n")
    ################################## format: word, *logprob, *ppl, *ppl1, postPr, log, *log10, *sum, *log10, ngram, Ucon, Bo, length, POS, state
    print("sentence:BEGIN")
    for item in filter(None, (sentence).split()):
        print(item)
    print("sentence:END")

    #for word in filter(None, (sentence).split()):
    for word in sentence.split():
        print("********************************************")
        print("NO_BALI_INDEX = %d" %NO_BALI_INDEX)
        col=[]
        col.append(word)		# word column
        print("word:BEGIN")
        print(word)
        print("word:END")

        #col.append(str(logprob))	# logprob column
        #col.append(str(ppl))		# perplexity log(ppl)  column
        #col.append(str(ppl1))		# perplexity log 1(ppl1) column
        #col.append(graph[WORD_INDEX][1] if len(graph) > WORD_INDEX and str(graph[WORD_INDEX][1]) != "?" else str(functions.calculateGraphEverageValue(graph)))                # posterior probability(postPr) column
        """col.append(graph[WORD_INDEX][1] if len(graph) > WORD_INDEX and str(graph[WORD_INDEX][1]) != "?" else str(calculateGraphEverageValue(graph)))                # posterior probability(postPr) column"""
        # posterior probability(postPr) column
        if len(graph) > WORD_INDEX and str(graph[WORD_INDEX][1]) != "?":
            col.append(graph[WORD_INDEX][1])
            print("posterior probability(postPr) column:BEGIN")
            print(graph[WORD_INDEX][1])
            print("posterior probability(postPr) column:END")
        else:
            col.append(str(calculateGraphEverageValue(graph)))
            print("posterior probability(postPr) column 2:BEGIN")
            print(str(calculateGraphEverageValue(graph)))
            print("posterior probability(postPr) column 2:END")
        #end if

        """col.append(ngram[word][0].split("=")[1] if word in ngram else "") # log column"""

        if word in ngram:
            # log column
            col.append(ngram[word][0].split("=")[1])
            print("log column:BEGIN")
            print(ngram[word][0].split("=")[1])
            print("log column:END")

            # ngram column
            col.append(ngram[word][3].split(" ")[1])
            print("ngram column:BEGIN")
            print(ngram[word][3].split(" ")[1])
            print("ngram column:END")

            # used context(Ucon) column
            col.append(ngram[word][4].split(" : ")[1][1:-2])
            print("used context(Ucon) column:BEGIN")
            print(ngram[word][4].split(" : ")[1][1:-2])
            print("used context(Ucon) column:END")

            # back off probability column
            col.append(ngram[word][5].split(" : ")[1][:-2])
            print("back off probability column:BEGIN")
            print(ngram[word][5].split(" : ")[1][:-2])
            print("back off probability column:END")
        else:
            col.append("") # log column
            col.append("") # ngram column
            col.append("") # used context(Ucon) column
            col.append("") # back off probability column
        #end if


        #col.append(ngram[word][1].split("=")[1][:-1] if word in ngram else "")					# log10 column
        #col.append(filter(None, ngram[word][2].split(" "))[0].split("=")[1] if word in ngram else "")		# sum colum
        #col.append(filter(None, ngram[word][2].split(" "))[1].split("=")[1][:-1] if word in ngram else "")	# log10(sum) column
        """col.append(ngram[word][3].split(" ")[1] if word in ngram else "") # ngram column"""
        """col.append(ngram[word][4].split(" : ")[1][1:-2] if word in ngram else "") # used context(Ucon) column"""
        """col.append(ngram[word][5].split(" : ")[1][:-2] if word in ngram else "") # back off probability column"""
        if word != "<s>" and word != "</s>":
            #col.append(word_length_list[WORD_INDEX] if len(word_length_list) > WORD_INDEX and str(word_length_list[WORD_INDEX]) != "?" else str(functions.calculateWordLengthEverageValue(word_length_list))[:4]) # word length column
            # word length column
            col.append(word_length_list[WORD_INDEX] if len(word_length_list) > WORD_INDEX and str(word_length_list[WORD_INDEX]) != "?" else str(calculateWordLengthEverageValue(word_length_list))[:4]) # word length column

            print("part_of_speech_list")
            print(part_of_speech_list[NO_BALI_INDEX-1])

            #raise Exception("Just for testing")

            col.append(part_of_speech_list[NO_BALI_INDEX-1][1]) # part of speech column

            """
            #not yet test the case of deletion #error in line: L14P4_P4-2_33
            if pra_path: # state column
                tmp_word_ele=word_error_dict[sentence_id.lower()][NO_BALI_INDEX].split(" ")
                if re.match("\*+", tmp_word_ele[1]):
                    col.append(BadLabel)
                elif tmp_word_ele[0] != tmp_word_ele[1]:
                    col.append(BadLabel)
                elif tmp_word_ele[0] == tmp_word_ele[1]:
                    col.append(GoodLabel)
                else:
                    col.append(BadLabel)
            else:
                col.append("C")
            #end if
            """
            NO_BALI_INDEX+=1
        else:
            col.append("") # word length column
            col.append("")	 # part of speech column
            #col.append("?") # state column
        #end if

        WORD_INDEX+=1

        str_output = ""
        if len(col) != 8: #Khong dung cot state column
            sys.stderr.write("Error: \""+sentence_id+"\" row number "+str(NO_BALI_INDEX)+" lack of attribute.\nAttribute number:  "+str(len(col)))
        #end if

        #str_output = sentence_id+", "+", ".join(col)+"."
        str_output = sentence_id+", "+", ".join(col)
        file_writer.write(str_output + "\n")

        str_output += str(len(col))
        print(str_output)
        """
        if len(col) != 9:
				sys.stderr.write("Error: \""+sentence_id+"\" row number "+str(NO_BALI_INDEX)+" lack of attribute.\nAttribute number:  "+str(len(col)))
        print sentence_id+", "+", ".join(col)+"."

        str_output = sentence_id+", "+", ".join(col)+"."
        print(str_output)
        file_writer.write(str_output + "\n")
        """

        #print "\n"
        sys.stderr.write("Done "+sentence_id+"\n")
    #end for

    #close file
    file_writer.close()
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
if __name__=="__main__":
    #Test case:
    current_config = load_configuration()

    #Buoc 1: Trich cac feature cua ASR
    #run_test_asr(hypothesis_asr_path, reference_asr_path, format_output = "csv")
    #run_test_asr(current_config.HYPOTHESIS_ASR_PATH, current_config.REFERENCE_ASR_PATH, "csv")
    run_test_asr(current_config.HYPOTHESIS_ASR_PATH, current_config.REFERENCE_ASR_PATH, current_config.FEATURES_VALUES_ASR_PATH)
    #error in line 995

    #Buoc 2: loc lai cac feature va alignment
    get_feature_asr()
    """word; posterior probability(postPr); log column; ngram column; used context(Ucon); back off probability; word length column; POS
les	0.509947	-4.38473	1	0	0	0.48	DET:ART
de	0.959214	-3.60662	2	2	-0.120692	0.22	PRP
    """

    print("OK")
