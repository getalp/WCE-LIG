# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 18:41:30 2015
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

import os
import sys

#**************************************************************************#
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from config.configuration import *
#from feature.common_functions import *
from common_module.cm_config import load_configuration
from common_module.cm_util import split_string_to_list_delimeter_comma
#**************************************************************************#
dict_character = {"à":"a2", "â":"a3", "ç":"c5", "è":"e2", "é":"e1", \
"ê":"e3", "ë":"e4", "î":"i3", "ï":"i4", "ô":"o3", "ù":"u2", \
"ü":"u4", "û":"u3"}
"""
Kinh nghiem: Sau khi co ket qua tu KALDI thi
1 é
2 à
3 â
4 ï
5 ç
"""
#**************************************************************************#
def get_encoding( char_and_num, dict_character):
    """
    Converting character+num --> french character. For example: "e3" --> "ê"

    :type char_and_num: string
    :param char_and_num: character+num. For example: e3

    :type dict_character: string
    :param dict_character: Dictionary contains charset for encoding

    :rtype: charset for encoding
    """
    result = ""

    for i in dict_character:
        if char_and_num in dict_character[i]:
            return i

    #if not existed in dict-tagset
    return result
#**************************************************************************#
def replace_substring( string_input, dict_character):
    """
    Converting string that is able to contain character+num --> french character. For example: "e3" --> "ê"

    :type string_input: string
    :param string_input: string that maybe contain character+num. For example: e3

    :type dict_character: string
    :param dict_character: Dictionary contains charset for encoding

    :rtype: string that be replaced french character (IF EXISTED). For example: ê
    """
    result = string_input

    for i in dict_character:
        #print(i + ", " + dict_character[i])
        result = result.replace(dict_character[i], i)

    return result
#**************************************************************************#
"""
file chua noi dung:
...
L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
L01P1_P1-2_33, la, 1, -4.49397, 1, 0, 0, 0.23, DET:ART, C.
...
"""

#**************************************************************************#
"""
Ham tao file chi chua cac tu nhung chua duoc encoding
"""
def generate_output_sentences_not_encoding(file_input_path, file_output_path):
    """
    Generating the output file that contains sentences which is not encoded.

    :type file_input_path: string
    :param file_input_path: each line contains within format: L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.

    :type file_output_path: string
    :param file_output_path: each line contains within format: L01P1_P1-0_01 les chirurgiens de los angeles on dit qu' ils e1taient outre a de1clare1 m se camus

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    """
...
L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
L01P1_P1-2_33, la, 1, -4.49397, 1, 0, 0, 0.23, DET:ART, C.
...
    """
    str_current_sentence_id = ""
    pre_sentence_id = ""
    str_output = ""
    is_saved = False

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue
        #end if

        #split_string_to_list_delimeter_comma
        items = split_string_to_list_delimeter_comma(line)

        if len(items) <= 3:
            print("You should check data in input")
            continue
        #end if

        if pre_sentence_id == "": #first sentence
            pre_sentence_id = items[0]
            str_current_sentence_id = items[0]
            str_output = str_current_sentence_id + "\t"
        else:
            str_current_sentence_id = items[0]
            word_not_encoding = items[1].strip() + " "
            if pre_sentence_id == str_current_sentence_id:
                str_output += word_not_encoding
            else:
                #ghi ra output
                str_output = str_output.strip() + "\n"
                file_writer.write(str_output)
                is_saved = True
                print(str_output)

                pre_sentence_id = str_current_sentence_id
                str_output = str_current_sentence_id + "\t" + word_not_encoding
                is_saved = False
            #end if
        #end if
    #end for

    if is_saved == False:
        #ghi ra output
        str_output = str_output.strip() + "\n"
        file_writer.write(str_output)
        is_saved = True
        print(str_output)
    #end if

    #close files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
"""
Ham tao file chi chua cac tu VA chua cac tu da duoc encoding theo dict_character cho truoc
"""
def generate_output_sentences_within_encoding(file_input_path, file_output_path):
    """
    Generating the output file that contains sentences which is not encoded.

    :type file_input_path: string
    :param file_input_path: each line contains within format: L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.

    :type file_output_path: string
    :param file_output_path: each line contains within format: L01P1_P1-0_01 les chirurgiens de los angeles on dit qu' ils étaient outre a déclaré m se camus

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    #Generating the output file that contains sentences which is not encoded.
    generate_output_sentences_not_encoding( file_input_path, current_config.OUTPUT_SENTENCES_NOT_ENCODING)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(current_config.OUTPUT_SENTENCES_NOT_ENCODING, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue
        #end if

        str_output = replace_substring(line, dict_character)
        str_output = str_output.strip() + "\n"

        file_writer.write(str_output)
    #end for

    #close files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
"""
Ham them id_word doi voi tung tu trong cau, van GIU format, dong thoi encoding theo dict_character cho truoc
"""
"""
...
L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
L01P1_P1-2_33, la, 1, -4.49397, 1, 0, 0, 0.23, DET:ART, C.
...
"""

"""output
L01P1_P1-0_01, 0,  les, 0.509947, -4.38473, 1, 0, 0, 0.48, DET:ART, C.
L01P1_P1-0_01, 1,  chirurgiens, 0.509947, -10.6568, 2, 1, 0, 0.11, NOM, C.
"""
def generate_output_format_row_within_encoding(file_input_path, file_output_path):
    """
    Generating the output file that contains format row which is encoded. For example:
    input: L01P1_P1-0_01, tie3n, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
    output: L01P1_P1-0_01, tiên, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.

    :type file_input_path: string
    :param file_input_path: each line contains within format: L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.

    :type file_output_path: string
    :param file_output_path: each line contains within format: L01P1_P1-0_01,0,camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    """
...
L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
L01P1_P1-2_33, la, 1, -4.49397, 1, 0, 0, 0.23, DET:ART, C.
...
    """
    str_current_sentence_id = ""
    pre_sentence_id = ""
    str_output = ""
    list_output = []
    #is_saved = False
    comma = ","
    current_id_word = 0

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue
        #end if

        #split_string_to_list_delimeter_comma
        items = split_string_to_list_delimeter_comma(line)

        item_count = len(items)
        if item_count <= 3:
            print("You should check data in input")
            continue
        #end if

        """output: L01P1_P1-0_01,chirurgiens,de,los,angeles,on,dit,qu',ils,étaient,outre,a,déclaré,m,se,camus
        if pre_sentence_id == "": #first sentence
            pre_sentence_id = items[0]
            str_current_sentence_id = items[0]
            #str_output = str_current_sentence_id + "\t"
            list_output.append(str_current_sentence_id)
        else:
            str_current_sentence_id = items[0]
            word_not_encoding = items[1].strip()
            word_within_encoding = replace_substring(word_not_encoding, dict_character)

            if pre_sentence_id == str_current_sentence_id:
                #str_output += word_not_encoding
                list_output.append(word_within_encoding)
            else:
                #ghi ra output
                str_output = comma.join(list_output)
                str_output = str_output.strip() + "\n"
                file_writer.write(str_output)
                is_saved = True
                print(str_output)

                pre_sentence_id = str_current_sentence_id

                #str_output = str_current_sentence_id + "\t" + word_not_encoding
                list_output = []
                list_output.append(str_current_sentence_id)
                list_output.append(word_within_encoding)

                is_saved = False
            #end if
        #end if
        """

        """output
        L01P1_P1-0_01, 0,  les, 0.509947, -4.38473, 1, 0, 0, 0.48, DET:ART, C.
        L01P1_P1-0_01, 1,  chirurgiens, 0.509947, -10.6568, 2, 1, 0, 0.11, NOM, C.
        """

        #Tao id_word phu hop
        if pre_sentence_id == "": #first sentence
            current_id_word = 0
            pre_sentence_id = items[0]
            str_current_sentence_id = items[0]
        else:
            str_current_sentence_id = items[0]
            if pre_sentence_id == str_current_sentence_id: #neu co trung id_sentence
                current_id_word += 1
            else: # neu khac id_sentence
                pre_sentence_id = str_current_sentence_id
                current_id_word = 0
            #end if
        #end if

        #cac thanh phan item con lai, ngoai tru id_word
        item_range = range(item_count)
        list_output = []
        for i in item_range:
            if i == 1:
                word_not_encoding = items[1].strip()
                word_within_encoding = replace_substring(word_not_encoding, dict_character)

                #them id_word vao phia truoc word
                list_output.append(str(current_id_word))

                list_output.append(word_within_encoding)
            else:
                list_output.append(items[i].strip())
            #end if
        #end for

        #ghi ra output
        str_output = comma.join(list_output)
        str_output = str_output.strip() + "\n"
        file_writer.write(str_output)
        print(str_output)
    #end for

    """
    if is_saved == False:
        #ghi ra output
        str_output = comma.join(list_output)
        str_output = str_output.strip() + "\n"
        file_writer.write(str_output)
        is_saved = True
        print(str_output)
    #end if
    """

    #close files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
"""
Ham tao file chi chua cac tu sau khi da duoc encoding theo dict_character cho truoc
"""
"""
...
L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
L01P1_P1-2_33, la2, 1, -4.49397, 1, 0, 0, 0.23, DET:ART, C.
...
"""

"""
camus
là
"""
def generate_output_format_column_within_encoding(file_input_path, file_output_path):
    """
    Generating the output file that contains format column which is encoded. For example:
    input: L01P1_P1-0_01, tie3n, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
    output: tiên

    :type file_input_path: string
    :param file_input_path: each line contains within format: L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.

    :type file_output_path: string
    :param file_output_path: each line contains within format column: camus

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    """
...
L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.
L01P1_P1-2_33, la2, 1, -4.49397, 1, 0, 0, 0.23, DET:ART, C.
...
    """
    str_current_sentence_id = ""
    pre_sentence_id = ""
    str_output = ""

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue
        #end if

        #split_string_to_list_delimeter_comma
        items = split_string_to_list_delimeter_comma(line)

        item_count = len(items)
        if item_count <= 3:
            print("You should check data in input")
            continue
        #end if

        """
        camus
        là
        """

        #Tao id_word phu hop
        if pre_sentence_id == "": #first sentence
            pre_sentence_id = items[0]
            str_current_sentence_id = items[0]
        else:
            str_current_sentence_id = items[0]
            if pre_sentence_id != str_current_sentence_id: #neu khac id_sentence
                pre_sentence_id = str_current_sentence_id

                #xuong dong
                file_writer.write("\n")
            #end if
        #end if

        #word after encoding
        word_not_encoding = items[1].strip()
        word_within_encoding = replace_substring(word_not_encoding, dict_character)

        #ghi ra output
        str_output = word_within_encoding + "\n"
        file_writer.write(str_output)
        print(str_output)
    #end for

    #close files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
#Ham sap xep output theo list of id_sentences ASR
#Tu du lieu output cua asr chuyen sang sort theo list of id_sentences ASR
def sort_result_of_features_values_asr_by_list_of_id_sentences_asr(file_input_path, file_list_of_id_sentences_asr, file_output_path):
    """
    Sorting the result file that contains features' values ASR by given list of id sentences ASR.

    :type file_input_path: string
    :param file_input_path: each line contains within format: L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.

    :type file_list_of_id_sentences_asr: string
    :param file_list_of_id_sentences_asr: each line contains within format: L01P1_P1-0_01

    :type file_output_path: string
    :param file_output_path: each line contains within format row that is sorted.

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input that contains each line contains within format: L01P1_P1-0_01, camus, 0.509947, -12.7847, 1, 2, -1.06601, 0.22, PRO:PER, C.')

    if not os.path.exists(file_list_of_id_sentences_asr):
        raise TypeError('Not Existed file corpus input and each line contains within format: L01P1_P1-0_01')

    #open 2 files:
    #for reading: file_input_path
    file_reader_list = open(file_list_of_id_sentences_asr, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    num_of_sentences = 0

    #read data in openned file
    for line in file_reader_list:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue
        #end if

        #doc file input
        file_reader_input = open(file_input_path, mode = 'r', encoding = 'utf-8')
        str_current_sentence_id = ""
        str_output = ""
        for line_input in file_reader_input:
            line_input = line_input.strip()

            #split_string_to_list_delimeter_comma
            items = split_string_to_list_delimeter_comma(line_input)

            item_count = len(items)
            if item_count <= 3:
                print("You should check data in input")
                continue
            #end if

            str_current_sentence_id = items[0].strip()
            if str_current_sentence_id == line: #neu trung id_sentence thi ghi ra file
                #ghi ra output
                str_output = line_input + "\n"
                file_writer.write(str_output)
                #print(str_output)
            #end if
        #end for

        #close file
        file_reader_input.close()

        num_of_sentences += 1
        print("Finished line %d" %num_of_sentences)
    #end for

    #close files
    file_reader_list.close()
    file_writer.close()
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    #enc = get_encoding('a2', dict_character)
    #print(enc)

    #enc = replace_substring("e1taient de1nonce1 de1ja2 gra3ce noe4l commenc5ait commenc5ait tre2s", dict_character)
    #print(enc)

    #FEATURES_VALUES_ASR_PATH
    current_config = load_configuration()

    #input
    #L01P1_P1-0_01, les, 0.509947, -4.38473, 1, 0, 0, 0.48, DET:ART, C.

    #AFTER_SORTING_FEATURES_VALUES_ASR_PATH
    #sort_result_of_features_values_asr_by_list_of_id_sentences_asr(file_input_path, file_list_of_id_sentences_asr, file_output_path)
    sort_result_of_features_values_asr_by_list_of_id_sentences_asr( current_config.FEATURES_VALUES_ASR_PATH, current_config.LIST_OF_ID_SENTENCES_ASR, current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH)

    #OUTPUT_SENTENCES_NOT_ENCODING
    #generate_output_sentences_not_encoding(file_input_path, file_output_path)
    generate_output_sentences_not_encoding( current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH, current_config.OUTPUT_SENTENCES_NOT_ENCODING)
    #output: L01P1_P1-0_01	chirurgiens de los angeles on dit qu' ils e1taient outre a de1clare1 m se camus

    #OUTPUT_SENTENCES_WITHIN_ENCODING
    #generate_output_sentences_within_encoding(file_input_path, file_output_path)
    generate_output_sentences_within_encoding( current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH, current_config.OUTPUT_SENTENCES_WITHIN_ENCODING)
    #output: L01P1_P1-0_01	chirurgiens de los angeles on dit qu' ils étaient outre a déclaré m se camus

    #OUTPUT_FORMAT_ROW_WITHIN_ENCODING
    #generate_output_format_row_within_encoding(file_input_path, file_output_path)
    generate_output_format_row_within_encoding( current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH, current_config.OUTPUT_FORMAT_ROW_WITHIN_ENCODING)
    #output: L01P1_P1-0_01,0,les,0.509947,-4.38473,1,0,0,0.48,DET:ART,C.

    #OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING
    #generate_output_format_column_within_encoding(file_input_path, file_output_path)
    generate_output_format_column_within_encoding( current_config.AFTER_SORTING_FEATURES_VALUES_ASR_PATH, current_config.OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING)
    #output: les

    print('OK')
