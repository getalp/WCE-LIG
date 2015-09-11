# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 16:05:46 2014
#Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
"""
#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

"""
*** input:
0. file chua du lieu thong tin cua Source Language (FR)
1. file alignment cua moses
2. file output from TreeTagger cua Source Language (FR)
3. file output from TreeTagger cua Target Language (EN)

Chu y: the first word's alignment information will be prefixed with symbol "B-" (that means Beginning) and "I-" (Inside) will be added at the beginning of alignment information for each of the remaining ones. With the target words which are not aligned with any source word, alignment information will be represented as "O-" (ref: paper of Quang 2012, page 47)

*** output tra ve co dang nhu sau:

También ADV        B-it|also        B-PP|RB        _x-1        _x-1        rose        VBD
aumentó VLfin        B-rose        B-VBD        also        RB        in        IN
en PREP        B-in        B-IN        rose        VBD        Mexico        NP

Target_Word
Target_POS

Right_Source_Context
Right_Source_POS

Left_Source_Context
Left_Source_POS

Source_Word
Source_POS

--version 2--

+Target_Word
+Target_POS

+Right_Target_Context
+Right_Target_POS

+Left_Target_Context
+Left_Target_POS

-Source_Word
-Source_POS

-Right_Source_Context
-Right_Source_POS

-Left_Source_Context
-Left_Source_POS
"""

"""
Y tuong:
B1: Tao class Word_POS chua (word, pos_of_word, stemming): __init__, get, set
* Xay dung list chua cac alignment (ref: longest source gram length). Tu do, moi tu o cau dich se la mot doi tuong, chua cac yeu cau nhu tren:Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming.
-->
B2: Xay dung 2 danh sach cho Source_Language va Target_Language trong do moi phan tu cua danh sach la mot doi tuong Word_POS.

B3: Dua vao alignment cua moses chung ta co the biet duoc cac yeu cau cua bai toan. Sau do, ghi ket qua vao file output
"""

import os
import sys

# for call shell script
# import shlex, subprocess

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  #in order to test with line by line on the server

#from feature.common_functions import *
#from config.config_end_user import *
#from config.configuration import *

from preprocessing.alignment_giza import \
        get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE_after_optimising
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import is_existed_file, \
        get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE, \
        get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET, get_line_given_number_of_sentence, \
        get_list_alignment_target_to_source_from_line_output_fast_align_TARGET_To_SOURCE
from common_module.cm_util import is_in_string
#**************************************************************************#
#B1: Tao class Word_POS_Stemming chua (word, pos_of_word, stemming): __init__, get, set
class Word_POS_Stemming(object):
        """
        Containing the following items: Word, Part Of Speech, Stemming
        """
        word = ""
        pos = ""
        stemming = ""

        def __init__(self):
                self.word = ""
                self.pos = ""
                self.stemming = ""

        def __init__(self, word, pos, stemming):
                self.word = word
                self.pos = pos
                self.stemming = stemming

        def set_word(self, word=""):
                self.word = word

        def set_pos(self, pos=""):
                self.pos = pos

        def set_stemming(self, stemming=""):
                self.stemming = stemming

        def get_word(self):
                return self.word

        def get_pos(self):
                return self.pos

        def get_stemming(self):
                return self.stemming

        #operator overloadding
        def __add__(self, other):
                list_out = []
                list_out.append(self.word)
                list_out.append(self.pos)
                list_out.append(self.stemming)

                list_out.append(other.get_word())
                list_out.append(other.get_pos())
                list_out.append(other.get_stemming())

                str_out = "\t".join(list_out)
                return str_out

#**************************************************************************#
#B2: Xay dung 2 danh sach cho Source_Language va Target_Language trong do moi phan tu cua danh sach la mot doi tuong Word_POS.
#neu lam cach nay thi du lieu lon se nguy hiem :)
#cach nay khong hieu qua vi TreeTagger khong the phan biet duoc trong truong hop du lieu nhieu. vi du
# 16 . 17 . / + 23 . 24 --> cac dau cham, TreeTagger se hieu la SENT --> trot quot cham com :)))
"""
def get_list_word_pos_stemming_from_output_treetagger(file_input_path):

    Getting list of Word_POS_Stemming from output of TreeTagger

    :type file_input_path: string
    :param file_input_path: each line contains output of tool TreeTagger. If POS == SENT thi ket thuc cau do

    :type file_output_path: string
    :param file_output_path: contains corpus with format each "word" in each line; there is a empty line among the sentences. ABCDEFG ~ 7654321

    :raise ValueError: if any path is not existed

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output from TreeTagger')

    #open files:
    #for reading: file_input_path
    file_reader = open(file_input_path, 'r')


    result = [] # empty list
    str_unknown = "<unknown>"
    str_end_of_sentence = "SENT"

    # read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        line_split = split_string_to_list_delimeter_tab(line)

        if len(line_split) == 0:
            raise Exception("du lieu dua vao ham split_string_to_list_delimeter_tab khong dung. Kiem tra lai nha :)")
        else:
            line_word = line_split[0]
            line_pos = line_split[1]
            line_stemming = line_split[2]

            if line_stemming == str_unknown: #muc dich: De khi thong ke thi phan tu nay chiem rat nho trong csdl. Neu de unknown thi khi dua vao so luong unknown de tinh toan --> du lieu khong duoc tot
                line_stemming = line_word
            result.append(Word_POS_Stemming(line_word, line_pos, line_stemming))
    #end for

    file_reader.close()

    return result
"""
#**************************************************************************#
#y tuong: moi cau sau khi dung TreeTagger tach ra, chung ta doc len va dua vao trong cau va cach nhau bang ky hieu dac biet ti :) ||||||
#convert_format_column_to_format_row_from_output_treetagger(file_input_path, file_output_path)
#in common_functions
#**************************************************************************#
#B3: Dua vao alignment cua moses chung ta co the biet duoc cac yeu cau cua bai toan. Sau do, ghi ket qua vao file output
def get_alignment_features(file_output_from_moses_included_alignment_word_to_word_path,
                           file_output_treetagger_ref_test_source_language,
                           file_output_treetagger_mt_test_target_language, file_output_path):
        """
        Creating the requirements for extracting features such as:
        --version 2-- --> version 3 co them stemming

        FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
        EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

        +Target_Word
        +Target_POS

        +Right_Target_Context
        +Right_Target_POS

        +Left_Target_Context
        +Left_Target_POS

        -Source_Word
        -Source_POS

        -Right_Source_Context
        -Right_Source_POS

        -Left_Source_Context
        -Left_Source_POS
        ======================================================================================================
        :type file_output_from_moses_included_alignment_word_to_word_path: string
        :param file_output_from_moses_included_alignment_word_to_word_path: the ouput included alignment word to word from target to source (MOSES format)

        :type file_output_treetagger_ref_test_source_language: string
        :param file_output_treetagger_ref_test_source_language: Reference Test in Source Language - each line contains output of tool TreeTagger in row format

        :type file_output_treetagger_mt_test_target_language: string
        :param file_output_treetagger_mt_test_target_language: Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger in row format

        :type file_output_path: string
        :param file_output_path:each line contains (Word; POS; Stemming) of Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

        :raise ValueError: if any path is not existed
        """
        # check existed paths
        """
        if not os.path.exists(file_output_from_moses_included_alignment_word_to_word_path):
                raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

        if not os.path.exists(file_output_treetagger_ref_test_source_language):
                raise TypeError('Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger.')

        if not os.path.exists(file_output_treetagger_mt_test_target_language):
                raise TypeError('Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger.')
        """
        str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path"
        is_existed_file(file_output_from_moses_included_alignment_word_to_word_path, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_ref_test_source_language, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_mt_test_target_language, str_message_if_not_existed)

        #for reading: file_output_from_moses_included_alignment_word_to_word_path
        file_reader_output_from_moses = open(file_output_from_moses_included_alignment_word_to_word_path, mode='r',  encoding='utf-8')

        #for writing: file_output_path
        file_writer = open(file_output_path, mode='w', encoding='utf-8')

        # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
        number_of_sentence = 1
        delimiter_char = "|||"
        str_not_existed = "_X+2"
        str_not_existed_in_front = "_X-1"
        str_not_existed_back = "_X+1"

        for line_in_output_moses in file_reader_output_from_moses:
                """
                #can kiem tra lai du lieu cau thu 881
                #da kiem tra ok, ly do: tu format column chuyen sang format row bi mat sentence column cuoi cung, vi trong file format column khong co dong trong cuoi cung
                #--> giai phap: cap nhat ham convert them flag de kiem tra "da duoc luu" hay
                chua True/False ?
                if number_of_sentence != 881:
                        number_of_sentence = number_of_sentence +1
                        continue
                """
                """
                print("*******************************************")
                print("Dang duyet cau thu: %d " %number_of_sentence)
                print("*******************************************")
                print(line_in_output_moses)
                print("*******************************************")
                """
                #list_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source.
                # Moi phan tu tren la mot doi tuong Word_POS_Stemming
                #trim string
                line_in_output_moses = line_in_output_moses.strip()

                if len(line_in_output_moses) == 0:
                        #print("Xuat hien dong trong - Empty line ... You should check corpus...")
                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                        continue

                # Duyet Tung cau dich va cau moses va xet
                # 0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16
                # PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15
                # ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
                # list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_moses) #version 1 - Target - Source _ nhom cuoi cua MOSES output
                # updated 2015.Jan.06 by Tien LE

                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)
                config_end_user = load_config_end_user()
                list_alignment_target_to_source = []

                if config_end_user.VERSION_MOSES == 2009:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(
                                line_in_output_moses)
                else:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(
                                line_in_output_moses)

                """
                print("*list_alignment_target_to_source*")
                print(list_alignment_target_to_source)
                print("*list_alignment_target_to_source*")
                """

                #***************************can update cho nay
                #file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

                #get temp_longest_source_gram_length_not_aligned_target_row
                #line_longest_source_gram_length = get_line_given_number_of_sentence(file_temp_longest_source_gram_length_not_aligned_target_row_path, number_of_sentence)
                #list_longest_source_gram_length = line_longest_source_gram_length.split() #Delimiter default = " "

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                list_source = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_ref_test = get_line_given_number_of_sentence(
                        file_output_treetagger_ref_test_source_language, number_of_sentence)

                line_output_treetagger_ref_test = line_output_treetagger_ref_test.replace("\n", "")
                """
                print("*line_output_treetagger_ref_test*")
                print(line_output_treetagger_ref_test)
                print("*line_output_treetagger_ref_test*")
                """
                #trim
                line_output_treetagger_ref_test = line_output_treetagger_ref_test.strip()  #strim line

                #split
                list_output_treetagger_ref_test = line_output_treetagger_ref_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_ref_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_ref_test:  #les|||DET|||le
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_source.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))

                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                list_target = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_mt_test = get_line_given_number_of_sentence(
                        file_output_treetagger_mt_test_target_language, number_of_sentence)

                line_output_treetagger_mt_test = line_output_treetagger_mt_test.replace("\n", "")
                """
                print("*line_output_treetagger_mt_test*")
                print(line_output_treetagger_mt_test)
                print("*line_output_treetagger_mt_test*")
                """
                line_output_treetagger_mt_test = line_output_treetagger_mt_test.strip()  #strim line

                list_output_treetagger_mt_test = line_output_treetagger_mt_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_mt_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_mt_test:  #the|||DT|||the
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_target.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))
                """
                print("*number_of_sentence*")
                print(number_of_sentence)
                print("*number_of_sentence*")

                print("*list_source*")
                print(list_source)
                print("*list_source*")

                print("*list_target*")
                print(list_target)
                print("*list_target*")
                """

                #line_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                ##Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #list_source = []
                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                #list_target = []

                #Danh sach cac tu dich voi moi phan tu la 1 object Word_Target_Language
                #list_of_words_alignment_target_to_source = []

                #target_sentence = get_target_sentence_from_output_moses(line_in_output_moses)

                #number_of_words_in_target_sentence = len(target_sentence.split())

                """
                print("***************************************")
                print("So tu trong target sentence la: %d " %number_of_words_in_target_sentence)
                print("***************************************")
                """

                #range_sentence = range(number_of_words_in_target_sentence)

                """
                print("*range_sentence*")
                print(range_sentence)
                print("*range_sentence*")
                """

                #Khoi tao danh sach ket qua
                #for i in range_sentence:
                #    obj_word_target_language = Word_Target_Language() # create instance

                #    list_of_words_alignment_target_to_source.append(obj_word_target_language)
                #end for

                #xu ly danh sach ket qua
                #0  1  2    3  ... n-1
                #0  1  2,3  '' ....    #'' co nghia la khong co phan tu nao lien ket, list_alignment_target_to_source
                #1  2  3,2  0  ....   #list_longest_source_gram_length
                comma_char = ","

                """
                print("*list_alignment_target_to_source**********************")
                print(list_alignment_target_to_source)
                print("*len**list_alignment_target_to_source*****************")
                print(len(list_alignment_target_to_source))
                print("*list_alignment_target_to_source**********************")
                """

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
                        index_alignment_of_source_word = -1  #khong co tu nao giong den

                        list_temp = []  # empty list

                        #lay chuoi ra, neu chua dau phay ,
                        if is_in_string(comma_char, index_alignment_to_source):  #co tu 2 lien ket voi nguon tro len
                                list_temp = index_alignment_to_source.split(comma_char)
                                index_alignment_of_source_word = int(list_temp[0])  #chi can xet tu dau tien duoc giong len Source

                        else:  #neu chi la 1 so nguyen, khong chua dau phay , co nghia la: chi chua 1 phan tu
                                list_temp.append(str(index_alignment_to_source))
                                try:
                                        index_alignment_of_source_word = int(index_alignment_to_source)
                                except ValueError:
                                        pass  #index_alignment_of_source_word = index_alignment_to_source #neu chua "" thi bi loi cho nay
                        #end if

                        index_of_target_word = i  #index cua tu dich

                        """
                        print("*index_of_target_word*")
                        print(index_of_target_word)
                        print("*index_of_target_word*")

                        print("*index_alignment_of_source_word*")
                        print(index_alignment_of_source_word)
                        print("*index_alignment_of_source_word*")
                        """
                        #print("*list_source*")
                        #print(list_source)
                        #print("*list_source*")

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        #Word_POS_Stemming
                        #str_not_existed = "_X+2"
                        #str_not_existed_in_front = "_X-1"
                        #str_not_existed_back = "_X+1"
                        target_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_target_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_target_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)
                        source_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_source_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_source_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)

                        try:
                                #xet target
                                target_res = list_target[index_of_target_word]

                                if index_of_target_word == 0:
                                        #khong co: Left_Target
                                        right_target_res = list_target[index_of_target_word + 1]

                                elif index_of_target_word == len(list_alignment_target_to_source) - 1:  #tu cuoi cau
                                        #khong co: Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                else:  #co ca 2 Left_Target & Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                        right_target_res = list_target[index_of_target_word + 1]
                        except IndexError:
                                #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                pass

                        #xet source
                        #index_alignment_of_source_word = -1 #khong co tu nao giong den
                        if index_alignment_of_source_word == -1:  #khong co lien ket nao den tu nguon
                                pass
                        else:
                                try:
                                        source_res = list_source[index_alignment_of_source_word]

                                        if index_alignment_of_source_word == 0:
                                                #khong co: Left_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                        elif index_alignment_of_source_word == len(list_source) - 1:  #tu cuoi cua NGUON
                                                #khong co: Right_Source
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                        else:  #co ca 2 Left_Source va Right_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                except IndexError:
                                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                        #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                        pass

                        #end if

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        cap1 = target_res + right_target_res
                        cap2 = left_target_res + source_res
                        cap3 = right_source_res + left_source_res

                        line_output = cap1 + "\t" + cap2 + "\t" + cap3

                        #ghi ra file output voi format la column
                        file_writer.write(line_output)
                        file_writer.write("\n")  # new line
                        """
                        print("*line_output*")
                        print(line_output)
                        print("*line_output*")
                        """
                #end for

                #print("Da xu ly xong cau thu %d" %number_of_sentence)
                number_of_sentence = number_of_sentence + 1
                file_writer.write("\n")  # new line for new sentence

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
        #end for

        #close files
        file_reader_output_from_moses.close()

        #for writing: file_output_path
        file_writer.close()


#**************************************************************************#
#**************************************************************************#
#y tuong: moi cau sau khi dung TreeTagger tach ra, chung ta doc len va dua vao trong cau va cach nhau bang ky hieu dac biet ti :) ||||||
#convert_format_column_to_format_row_from_output_treetagger(file_input_path, file_output_path)
#in common_functions
#**************************************************************************#
#B3: Dua vao alignment cua moses chung ta co the biet duoc cac yeu cau cua bai toan. Sau do, ghi ket qua vao file output
def get_alignment_features_threads(file_output_from_moses_included_alignment_word_to_word_path,
                           file_output_treetagger_ref_test_source_language,
                           file_output_treetagger_mt_test_target_language, file_output_path, config_end_user):
        """
        Creating the requirements for extracting features such as:
        --version 2-- --> version 3 co them stemming

        FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
        EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

        +Target_Word
        +Target_POS

        +Right_Target_Context
        +Right_Target_POS

        +Left_Target_Context
        +Left_Target_POS

        -Source_Word
        -Source_POS

        -Right_Source_Context
        -Right_Source_POS

        -Left_Source_Context
        -Left_Source_POS
        ======================================================================================================
        :type file_output_from_moses_included_alignment_word_to_word_path: string
        :param file_output_from_moses_included_alignment_word_to_word_path: the ouput included alignment word to word from target to source (MOSES format)

        :type file_output_treetagger_ref_test_source_language: string
        :param file_output_treetagger_ref_test_source_language: Reference Test in Source Language - each line contains output of tool TreeTagger in row format

        :type file_output_treetagger_mt_test_target_language: string
        :param file_output_treetagger_mt_test_target_language: Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger in row format

        :type file_output_path: string
        :param file_output_path:each line contains (Word; POS; Stemming) of Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

        :raise ValueError: if any path is not existed
        """
        # check existed paths
        """
        if not os.path.exists(file_output_from_moses_included_alignment_word_to_word_path):
                raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

        if not os.path.exists(file_output_treetagger_ref_test_source_language):
                raise TypeError('Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger.')

        if not os.path.exists(file_output_treetagger_mt_test_target_language):
                raise TypeError('Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger.')
        """
        str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path ("+file_output_from_moses_included_alignment_word_to_word_path + ")"
        is_existed_file(file_output_from_moses_included_alignment_word_to_word_path, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger ("+file_output_treetagger_ref_test_source_language + ")"
        is_existed_file(file_output_treetagger_ref_test_source_language, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger (" + file_output_treetagger_mt_test_target_language + ")"
        is_existed_file(file_output_treetagger_mt_test_target_language, str_message_if_not_existed)

        #for reading: file_output_from_moses_included_alignment_word_to_word_path
        file_reader_output_from_moses = open(file_output_from_moses_included_alignment_word_to_word_path, mode='r',  encoding='utf-8')

        #for writing: file_output_path
        file_writer = open(file_output_path, mode='w', encoding='utf-8')

        # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
        number_of_sentence = 1
        delimiter_char = "|||"
        str_not_existed = "_X+2"
        str_not_existed_in_front = "_X-1"
        str_not_existed_back = "_X+1"
        print (file_output_from_moses_included_alignment_word_to_word_path)
        print (file_output_treetagger_ref_test_source_language)
        print (file_output_treetagger_mt_test_target_language)
        
        for line_in_output_moses in file_reader_output_from_moses:
                """
                #can kiem tra lai du lieu cau thu 881
                #da kiem tra ok, ly do: tu format column chuyen sang format row bi mat sentence column cuoi cung, vi trong file format column khong co dong trong cuoi cung
                #--> giai phap: cap nhat ham convert them flag de kiem tra "da duoc luu" hay
                chua True/False ?
                if number_of_sentence != 881:
                        number_of_sentence = number_of_sentence +1
                        continue
                """
                """
                print("*******************************************")
                print("Dang duyet cau thu: %d " %number_of_sentence)
                print("*******************************************")
                print(line_in_output_moses)
                print("*******************************************")
                """
                #list_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source.
                # Moi phan tu tren la mot doi tuong Word_POS_Stemming
                #trim string
                line_in_output_moses = line_in_output_moses.strip()

                if len(line_in_output_moses) == 0:
                        #print("Xuat hien dong trong - Empty line ... You should check corpus...")
                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                        continue

                # Duyet Tung cau dich va cau moses va xet
                # 0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16
                # PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15
                # ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
                # list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_moses) #version 1 - Target - Source _ nhom cuoi cua MOSES output
                # updated 2015.Jan.06 by Tien LE

                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)
                #config_end_user = load_config_end_user()
                list_alignment_target_to_source = []

                if config_end_user.VERSION_MOSES == 2009:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(
                                line_in_output_moses)
                else:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(
                                line_in_output_moses)

                """
                print("*list_alignment_target_to_source*")
                print(list_alignment_target_to_source)
                print("*list_alignment_target_to_source*")
                """

                #***************************can update cho nay
                #file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

                #get temp_longest_source_gram_length_not_aligned_target_row
                #line_longest_source_gram_length = get_line_given_number_of_sentence(file_temp_longest_source_gram_length_not_aligned_target_row_path, number_of_sentence)
                #list_longest_source_gram_length = line_longest_source_gram_length.split() #Delimiter default = " "

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                list_source = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_ref_test = get_line_given_number_of_sentence(
                        file_output_treetagger_ref_test_source_language, number_of_sentence)

                line_output_treetagger_ref_test = line_output_treetagger_ref_test.replace("\n", "")
                """
                print("*line_output_treetagger_ref_test*")
                print(line_output_treetagger_ref_test)
                print("*line_output_treetagger_ref_test*")
                """
                #trim
                line_output_treetagger_ref_test = line_output_treetagger_ref_test.strip()  #strim line

                #split
                list_output_treetagger_ref_test = line_output_treetagger_ref_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_ref_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_ref_test:  #les|||DET|||le
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_source.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))

                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                list_target = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_mt_test = get_line_given_number_of_sentence(
                        file_output_treetagger_mt_test_target_language, number_of_sentence)

                line_output_treetagger_mt_test = line_output_treetagger_mt_test.replace("\n", "")
                """
                print("*line_output_treetagger_mt_test*")
                print(line_output_treetagger_mt_test)
                print("*line_output_treetagger_mt_test*")
                """
                line_output_treetagger_mt_test = line_output_treetagger_mt_test.strip()  #strim line

                list_output_treetagger_mt_test = line_output_treetagger_mt_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_mt_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_mt_test:  #the|||DT|||the
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_target.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))
                """
                print("*number_of_sentence*")
                print(number_of_sentence)
                print("*number_of_sentence*")

                print("*list_source*")
                print(list_source)
                print("*list_source*")

                print("*list_target*")
                print(list_target)
                print("*list_target*")
                """

                #line_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                ##Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #list_source = []
                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                #list_target = []

                #Danh sach cac tu dich voi moi phan tu la 1 object Word_Target_Language
                #list_of_words_alignment_target_to_source = []

                #target_sentence = get_target_sentence_from_output_moses(line_in_output_moses)

                #number_of_words_in_target_sentence = len(target_sentence.split())

                """
                print("***************************************")
                print("So tu trong target sentence la: %d " %number_of_words_in_target_sentence)
                print("***************************************")
                """

                #range_sentence = range(number_of_words_in_target_sentence)

                """
                print("*range_sentence*")
                print(range_sentence)
                print("*range_sentence*")
                """

                #Khoi tao danh sach ket qua
                #for i in range_sentence:
                #    obj_word_target_language = Word_Target_Language() # create instance

                #    list_of_words_alignment_target_to_source.append(obj_word_target_language)
                #end for

                #xu ly danh sach ket qua
                #0  1  2    3  ... n-1
                #0  1  2,3  '' ....    #'' co nghia la khong co phan tu nao lien ket, list_alignment_target_to_source
                #1  2  3,2  0  ....   #list_longest_source_gram_length
                comma_char = ","

                """
                print("*list_alignment_target_to_source**********************")
                print(list_alignment_target_to_source)
                print("*len**list_alignment_target_to_source*****************")
                print(len(list_alignment_target_to_source))
                print("*list_alignment_target_to_source**********************")
                """

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
                        index_alignment_of_source_word = -1  #khong co tu nao giong den

                        list_temp = []  # empty list

                        #lay chuoi ra, neu chua dau phay ,
                        if is_in_string(comma_char, index_alignment_to_source):  #co tu 2 lien ket voi nguon tro len
                                list_temp = index_alignment_to_source.split(comma_char)
                                index_alignment_of_source_word = int(list_temp[0])  #chi can xet tu dau tien duoc giong len Source

                        else:  #neu chi la 1 so nguyen, khong chua dau phay , co nghia la: chi chua 1 phan tu
                                list_temp.append(str(index_alignment_to_source))
                                try:
                                        index_alignment_of_source_word = int(index_alignment_to_source)
                                except ValueError:
                                        pass  #index_alignment_of_source_word = index_alignment_to_source #neu chua "" thi bi loi cho nay
                        #end if

                        index_of_target_word = i  #index cua tu dich

                        """
                        print("*index_of_target_word*")
                        print(index_of_target_word)
                        print("*index_of_target_word*")

                        print("*index_alignment_of_source_word*")
                        print(index_alignment_of_source_word)
                        print("*index_alignment_of_source_word*")
                        """
                        #print("*list_source*")
                        #print(list_source)
                        #print("*list_source*")

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        #Word_POS_Stemming
                        #str_not_existed = "_X+2"
                        #str_not_existed_in_front = "_X-1"
                        #str_not_existed_back = "_X+1"
                        target_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_target_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_target_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)
                        source_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_source_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_source_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)

                        try:
                                #xet target
                                target_res = list_target[index_of_target_word]

                                if index_of_target_word == 0:
                                        #khong co: Left_Target
                                        right_target_res = list_target[index_of_target_word + 1]

                                elif index_of_target_word == len(list_alignment_target_to_source) - 1:  #tu cuoi cau
                                        #khong co: Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                else:  #co ca 2 Left_Target & Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                        right_target_res = list_target[index_of_target_word + 1]
                        except IndexError:
                                #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                pass

                        #xet source
                        #index_alignment_of_source_word = -1 #khong co tu nao giong den
                        if index_alignment_of_source_word == -1:  #khong co lien ket nao den tu nguon
                                pass
                        else:
                                try:
                                        source_res = list_source[index_alignment_of_source_word]

                                        if index_alignment_of_source_word == 0:
                                                #khong co: Left_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                        elif index_alignment_of_source_word == len(list_source) - 1:  #tu cuoi cua NGUON
                                                #khong co: Right_Source
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                        else:  #co ca 2 Left_Source va Right_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                except IndexError:
                                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                        #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                        pass

                        #end if

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        cap1 = target_res + right_target_res
                        cap2 = left_target_res + source_res
                        cap3 = right_source_res + left_source_res

                        line_output = cap1 + "\t" + cap2 + "\t" + cap3

                        #ghi ra file output voi format la column
                        file_writer.write(line_output)
                        file_writer.write("\n")  # new line
                        """
                        print("*line_output*")
                        print(line_output)
                        print("*line_output*")
                        """
                #end for

                #print("Da xu ly xong cau thu %d" %number_of_sentence)
                number_of_sentence = number_of_sentence + 1
                file_writer.write("\n")  # new line for new sentence

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
        #end for

        #close files
        file_reader_output_from_moses.close()

        #for writing: file_output_path
        file_writer.close()


#**************************************************************************#
def get_alignment_features_with_output_giza(file_output_from_giza_path, file_output_treetagger_ref_test_source_language,
                                            file_output_treetagger_mt_test_target_language, file_output_path):
        """
        Creating the requirements for extracting features such as:
        --version 2-- --> version 3 co them stemming

        FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
        EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

        +Target_Word
        +Target_POS

        +Right_Target_Context
        +Right_Target_POS

        +Left_Target_Context
        +Left_Target_POS

        -Source_Word
        -Source_POS

        -Right_Source_Context
        -Right_Source_POS

        -Left_Source_Context
        -Left_Source_POS
        ======================================================================================================
        :type file_output_from_giza_path: string
        :param file_output_from_giza_path: the ouput included alignment word to word from target to source (GIZA++ format)

        :type file_output_treetagger_ref_test_source_language: string
        :param file_output_treetagger_ref_test_source_language: Reference Test in Source Language - each line contains output of tool TreeTagger in row format

        :type file_output_treetagger_mt_test_target_language: string
        :param file_output_treetagger_mt_test_target_language: Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger in row format

        :type file_output_path: string
        :param file_output_path:each line contains (Word; POS; Stemming) of Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

        :raise ValueError: if any path is not existed
        """
        # check existed paths
        """
        if not os.path.exists(file_output_from_giza_path):
                raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

        if not os.path.exists(file_output_treetagger_ref_test_source_language):
                raise TypeError('Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger.')

        if not os.path.exists(file_output_treetagger_mt_test_target_language):
                raise TypeError('Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger.')
        """
        str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path"
        is_existed_file(file_output_from_giza_path, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_ref_test_source_language, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_mt_test_target_language, str_message_if_not_existed)

        #for reading: file_output_from_giza_path
        #file_reader_output_from_moses = open(file_output_from_giza_path, mode = 'r', encoding = 'utf-8')
        """
        current_config = load_configuration()

        path_to_tool_giza = current_config.PATH_TO_TOOL_GIZA
        path_to_tool_mkcls = current_config.PATH_TO_TOOL_MKCLS
        path_to_corpus = current_config.PATH_TO_CORPUS
        source_corpus_name = current_config.SOURCE_CORPUS_NAME
        target_corpus_name = current_config.TARGET_CORPUS_NAME

        get_alignment_by_giza(path_to_tool_giza, path_to_tool_mkcls, path_to_corpus, source_corpus_name, target_corpus_name)
        """

        #get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE
        #target_source_A3_final: ../extracted_features/en_es.A3.final
        ##current_config.TARGET_SOURCE_A3_FINAL)
        alignment_target_to_source = get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE(
                file_output_from_giza_path)

        #print(alignment_target_to_source) #[1, 3, 4, 5, 6, 6, -1, 6, 6, 7]

        #print("len = %d" %len(alignment_target_to_source))

        #for writing: file_output_path
        file_writer = open(file_output_path, mode='w', encoding='utf-8')

        # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
        number_of_sentence = 1
        delimiter_char = "|||"
        str_not_existed = "_X+2"
        str_not_existed_in_front = "_X-1"
        str_not_existed_back = "_X+1"

        #for line_in_output_moses in file_reader_output_from_moses:
        for list_alignment_target_to_source in alignment_target_to_source:
                """
                #can kiem tra lai du lieu cau thu 881
                #da kiem tra ok, ly do: tu format column chuyen sang format row bi mat sentence column cuoi cung, vi trong file format column khong co dong trong cuoi cung --> giai phap: cap nhat ham convert them flag de kiem tra "da duoc luu" hay chua True/False ?
                if number_of_sentence != 881:
                        number_of_sentence = number_of_sentence +1
                        continue
                """
                """
                print("*******************************************")
                print("Dang duyet cau thu: %d " %number_of_sentence)
                print("*******************************************")
                print(line_in_output_moses)
                print("*******************************************")
                """
                #list_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                #trim string
                #line_in_output_moses = line_in_output_moses.strip()

                if len(list_alignment_target_to_source) == 0:
                        #print("Xuat hien dong trong - Empty line ... You should check corpus...")
                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                        continue

                #Duyet Tung cau dich va cau moses va xet
                #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_moses) #version 1 - Target - Source _ nhom cuoi cua MOSES output
                #updated 2015.Jan.06 by Tien LE

                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)
                """
                config_end_user = load_config_end_user()


                if config_end_user.VERSION_MOSES == 2009:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(line_in_output_moses)
                else:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)
                """
                #list_alignment_target_to_source = []
                #list_alignment_target_to_source = line

                """
                print("*list_alignment_target_to_source*")
                print(list_alignment_target_to_source)
                print("*list_alignment_target_to_source*")
                """

                #***************************can update cho nay
                #file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

                #get temp_longest_source_gram_length_not_aligned_target_row
                #line_longest_source_gram_length = get_line_given_number_of_sentence(file_temp_longest_source_gram_length_not_aligned_target_row_path, number_of_sentence)
                #list_longest_source_gram_length = line_longest_source_gram_length.split() #Delimiter default = " "

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                list_source = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_ref_test = get_line_given_number_of_sentence(
                        file_output_treetagger_ref_test_source_language, number_of_sentence)

                line_output_treetagger_ref_test = line_output_treetagger_ref_test.replace("\n", "")
                """
                print("*line_output_treetagger_ref_test*")
                print(line_output_treetagger_ref_test)
                print("*line_output_treetagger_ref_test*")
                """
                #trim
                line_output_treetagger_ref_test = line_output_treetagger_ref_test.strip()  #strim line

                #split
                list_output_treetagger_ref_test = line_output_treetagger_ref_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_ref_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_ref_test:  #les|||DET|||le
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_source.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))

                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                list_target = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_mt_test = get_line_given_number_of_sentence(
                        file_output_treetagger_mt_test_target_language, number_of_sentence)

                line_output_treetagger_mt_test = line_output_treetagger_mt_test.replace("\n", "")
                """
                print("*line_output_treetagger_mt_test*")
                print(line_output_treetagger_mt_test)
                print("*line_output_treetagger_mt_test*")
                """
                line_output_treetagger_mt_test = line_output_treetagger_mt_test.strip()  #strim line

                list_output_treetagger_mt_test = line_output_treetagger_mt_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_mt_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_mt_test:  #the|||DT|||the
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_target.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))
                """
                print("*number_of_sentence*")
                print(number_of_sentence)
                print("*number_of_sentence*")

                print("*list_source*")
                print(list_source)
                print("*list_source*")

                print("*list_target*")
                print(list_target)
                print("*list_target*")
                """

                #line_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                ##Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #list_source = []
                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                #list_target = []

                #Danh sach cac tu dich voi moi phan tu la 1 object Word_Target_Language
                #list_of_words_alignment_target_to_source = []

                #target_sentence = get_target_sentence_from_output_moses(line_in_output_moses)

                #number_of_words_in_target_sentence = len(target_sentence.split())

                """
                print("***************************************")
                print("So tu trong target sentence la: %d " %number_of_words_in_target_sentence)
                print("***************************************")
                """

                #range_sentence = range(number_of_words_in_target_sentence)

                """
                print("*range_sentence*")
                print(range_sentence)
                print("*range_sentence*")
                """

                #Khoi tao danh sach ket qua
                #for i in range_sentence:
                #    obj_word_target_language = Word_Target_Language() # create instance

                #    list_of_words_alignment_target_to_source.append(obj_word_target_language)
                #end for

                #xu ly danh sach ket qua
                #0  1  2    3  ... n-1
                #0  1  2,3  '' ....    #'' co nghia la khong co phan tu nao lien ket, list_alignment_target_to_source
                #1  2  3,2  0  ....   #list_longest_source_gram_length
                comma_char = ","

                """
                print("*list_alignment_target_to_source**********************")
                print(list_alignment_target_to_source)
                print("*len**list_alignment_target_to_source*****************")
                print(len(list_alignment_target_to_source))
                print("*list_alignment_target_to_source**********************")
                """

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
                        index_alignment_of_source_word = -1  #khong co tu nao giong den

                        list_temp = []  # empty list

                        """
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
                        #end if
                        """
                        try:
                                index_alignment_of_source_word = index_alignment_to_source
                        except ValueError:
                                pass

                        index_of_target_word = i  #index cua tu dich

                        """
                        print("*index_of_target_word*")
                        print(index_of_target_word)
                        print("*index_of_target_word*")

                        print("*index_alignment_of_source_word*")
                        print(index_alignment_of_source_word)
                        print("*index_alignment_of_source_word*")
                        """
                        #print("*list_source*")
                        #print(list_source)
                        #print("*list_source*")

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        #Word_POS_Stemming
                        #str_not_existed = "_X+2"
                        #str_not_existed_in_front = "_X-1"
                        #str_not_existed_back = "_X+1"
                        target_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_target_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_target_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)
                        source_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_source_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_source_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)

                        try:
                                #xet target
                                target_res = list_target[index_of_target_word]

                                if index_of_target_word == 0:
                                        #khong co: Left_Target
                                        right_target_res = list_target[index_of_target_word + 1]

                                elif index_of_target_word == len(list_alignment_target_to_source) - 1:  #tu cuoi cau
                                        #khong co: Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                else:  #co ca 2 Left_Target & Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                        right_target_res = list_target[index_of_target_word + 1]
                        except IndexError:
                                #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                pass

                        #xet source
                        #index_alignment_of_source_word = -1 #khong co tu nao giong den
                        if index_alignment_of_source_word == -1:  #khong co lien ket nao den tu nguon
                                pass
                        else:
                                try:
                                        source_res = list_source[index_alignment_of_source_word]

                                        if index_alignment_of_source_word == 0:
                                                #khong co: Left_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                        elif index_alignment_of_source_word == len(list_source) - 1:  #tu cuoi cua NGUON
                                                #khong co: Right_Source
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                        else:  #co ca 2 Left_Source va Right_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                except IndexError:
                                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                        #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                        pass

                        #end if

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        cap1 = target_res + right_target_res
                        cap2 = left_target_res + source_res
                        cap3 = right_source_res + left_source_res

                        line_output = cap1 + "\t" + cap2 + "\t" + cap3

                        #ghi ra file output voi format la column
                        file_writer.write(line_output)
                        file_writer.write("\n")  # new line
                        """
                        print("*line_output*")
                        print(line_output)
                        print("*line_output*")
                        """
                #end for

                #print("Da xu ly xong cau thu %d" %number_of_sentence)
                number_of_sentence = number_of_sentence + 1
                file_writer.write("\n")  # new line for new sentence

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
        #end for

        #close files
        #file_reader_output_from_moses.close()

        #for writing: file_output_path
        file_writer.close()


#**************************************************************************#
def get_alignment_features_with_output_giza_after_optimising(file_output_from_giza_path,
                                                             file_output_treetagger_ref_test_source_language,
                                                             file_output_treetagger_mt_test_target_language,
                                                             file_target_ref_test_format_row, file_output_path):
        """
        Creating the requirements for extracting features such as:
        --version 2-- --> version 3 co them stemming

        FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
        EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

        +Target_Word
        +Target_POS

        +Right_Target_Context
        +Right_Target_POS

        +Left_Target_Context
        +Left_Target_POS

        -Source_Word
        -Source_POS

        -Right_Source_Context
        -Right_Source_POS

        -Left_Source_Context
        -Left_Source_POS
        ======================================================================================================
        :type file_output_from_giza_path: string
        :param file_output_from_giza_path: the ouput included alignment word to word from target to source (GIZA++ format)

        :type file_output_treetagger_ref_test_source_language: string
        :param file_output_treetagger_ref_test_source_language: Reference Test in Source Language - each line contains output of tool TreeTagger in row format

        :type file_output_treetagger_mt_test_target_language: string
        :param file_output_treetagger_mt_test_target_language: Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger in row format

        :type file_output_path: string
        :param file_output_path:each line contains (Word; POS; Stemming) of Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

        :raise ValueError: if any path is not existed
        """
        # check existed paths
        """
        if not os.path.exists(file_output_from_giza_path):
                raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

        if not os.path.exists(file_output_treetagger_ref_test_source_language):
                raise TypeError('Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger.')

        if not os.path.exists(file_output_treetagger_mt_test_target_language):
                raise TypeError('Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger.')
        """
        str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path"
        is_existed_file(file_output_from_giza_path, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_ref_test_source_language, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_mt_test_target_language, str_message_if_not_existed)

        #for reading: file_output_from_giza_path
        #file_reader_output_from_moses = open(file_output_from_giza_path, mode = 'r', encoding = 'utf-8')
        """
        current_config = load_configuration()

        path_to_tool_giza = current_config.PATH_TO_TOOL_GIZA
        path_to_tool_mkcls = current_config.PATH_TO_TOOL_MKCLS
        path_to_corpus = current_config.PATH_TO_CORPUS
        source_corpus_name = current_config.SOURCE_CORPUS_NAME
        target_corpus_name = current_config.TARGET_CORPUS_NAME

        get_alignment_by_giza(path_to_tool_giza, path_to_tool_mkcls, path_to_corpus, source_corpus_name, target_corpus_name)
        """

        #get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE
        #target_source_A3_final: ../extracted_features/en_es.A3.final
        ##current_config.TARGET_SOURCE_A3_FINAL)
        #alignment_target_to_source = get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE(file_output_from_giza_path)
        alignment_target_to_source = get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE_after_optimising(
                file_output_from_giza_path, file_target_ref_test_format_row)

        #print(alignment_target_to_source) #[1, 3, 4, 5, 6, 6, -1, 6, 6, 7]

        print("len = %d" % len(alignment_target_to_source))

        #for writing: file_output_path
        file_writer = open(file_output_path, mode='w', encoding='utf-8')

        # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
        number_of_sentence = 1
        delimiter_char = "|||"
        str_not_existed = "_X+2"
        str_not_existed_in_front = "_X-1"
        str_not_existed_back = "_X+1"

        #for line_in_output_moses in file_reader_output_from_moses:
        for list_alignment_target_to_source in alignment_target_to_source:
                """
                #can kiem tra lai du lieu cau thu 881
                #da kiem tra ok, ly do: tu format column chuyen sang format row bi mat sentence column cuoi cung, vi trong file format column khong co dong trong cuoi cung --> giai phap: cap nhat ham convert them flag de kiem tra "da duoc luu" hay chua True/False ?
                if number_of_sentence != 881:
                        number_of_sentence = number_of_sentence +1
                        continue
                """
                """
                print("*******************************************")
                print("Dang duyet cau thu: %d " %number_of_sentence)
                print("*******************************************")
                print(line_in_output_moses)
                print("*******************************************")
                """
                #list_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                #trim string
                #line_in_output_moses = line_in_output_moses.strip()

                if len(list_alignment_target_to_source) == 0:
                        #print("Xuat hien dong trong - Empty line ... You should check corpus...")
                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                        continue

                #Duyet Tung cau dich va cau moses va xet
                #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_moses) #version 1 - Target - Source _ nhom cuoi cua MOSES output
                #updated 2015.Jan.06 by Tien LE

                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)
                """
                config_end_user = load_config_end_user()


                if config_end_user.VERSION_MOSES == 2009:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(line_in_output_moses)
                else:
                        list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)
                """
                #list_alignment_target_to_source = []
                #list_alignment_target_to_source = line

                """
                print("*list_alignment_target_to_source*")
                print(list_alignment_target_to_source)
                print("*list_alignment_target_to_source*")
                """

                #***************************can update cho nay
                #file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

                #get temp_longest_source_gram_length_not_aligned_target_row
                #line_longest_source_gram_length = get_line_given_number_of_sentence(file_temp_longest_source_gram_length_not_aligned_target_row_path, number_of_sentence)
                #list_longest_source_gram_length = line_longest_source_gram_length.split() #Delimiter default = " "

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                list_source = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_ref_test = get_line_given_number_of_sentence(
                        file_output_treetagger_ref_test_source_language, number_of_sentence)

                line_output_treetagger_ref_test = line_output_treetagger_ref_test.replace("\n", "")
                """
                print("*line_output_treetagger_ref_test*")
                print(line_output_treetagger_ref_test)
                print("*line_output_treetagger_ref_test*")
                """
                #trim
                line_output_treetagger_ref_test = line_output_treetagger_ref_test.strip()  #strim line

                #split
                list_output_treetagger_ref_test = line_output_treetagger_ref_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_ref_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_ref_test:  #les|||DET|||le
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_source.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))

                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                list_target = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_mt_test = get_line_given_number_of_sentence(
                        file_output_treetagger_mt_test_target_language, number_of_sentence)

                line_output_treetagger_mt_test = line_output_treetagger_mt_test.replace("\n", "")
                """
                print("*line_output_treetagger_mt_test*")
                print(line_output_treetagger_mt_test)
                print("*line_output_treetagger_mt_test*")
                """
                line_output_treetagger_mt_test = line_output_treetagger_mt_test.strip()  #strim line

                list_output_treetagger_mt_test = line_output_treetagger_mt_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_mt_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_mt_test:  #the|||DT|||the
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_target.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))
                """
                print("*number_of_sentence*")
                print(number_of_sentence)
                print("*number_of_sentence*")

                print("*list_source*")
                print(list_source)
                print("*list_source*")

                print("*list_target*")
                print(list_target)
                print("*list_target*")
                """

                #line_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                ##Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #list_source = []
                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                #list_target = []

                #Danh sach cac tu dich voi moi phan tu la 1 object Word_Target_Language
                #list_of_words_alignment_target_to_source = []

                #target_sentence = get_target_sentence_from_output_moses(line_in_output_moses)

                #number_of_words_in_target_sentence = len(target_sentence.split())

                """
                print("***************************************")
                print("So tu trong target sentence la: %d " %number_of_words_in_target_sentence)
                print("***************************************")
                """

                #range_sentence = range(number_of_words_in_target_sentence)

                """
                print("*range_sentence*")
                print(range_sentence)
                print("*range_sentence*")
                """

                #Khoi tao danh sach ket qua
                #for i in range_sentence:
                #    obj_word_target_language = Word_Target_Language() # create instance

                #    list_of_words_alignment_target_to_source.append(obj_word_target_language)
                #end for

                #xu ly danh sach ket qua
                #0  1  2    3  ... n-1
                #0  1  2,3  '' ....    #'' co nghia la khong co phan tu nao lien ket, list_alignment_target_to_source
                #1  2  3,2  0  ....   #list_longest_source_gram_length
                comma_char = ","

                """
                print("*list_alignment_target_to_source**********************")
                print(list_alignment_target_to_source)
                print("*len**list_alignment_target_to_source*****************")
                print(len(list_alignment_target_to_source))
                print("*list_alignment_target_to_source**********************")
                """

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
                        index_alignment_of_source_word = -1  #khong co tu nao giong den

                        list_temp = []  # empty list

                        """
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
                        #end if
                        """
                        try:
                                index_alignment_of_source_word = index_alignment_to_source
                        except ValueError:
                                pass

                        index_of_target_word = i  #index cua tu dich

                        """
                        print("*index_of_target_word*")
                        print(index_of_target_word)
                        print("*index_of_target_word*")

                        print("*index_alignment_of_source_word*")
                        print(index_alignment_of_source_word)
                        print("*index_alignment_of_source_word*")
                        """
                        #print("*list_source*")
                        #print(list_source)
                        #print("*list_source*")

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        #Word_POS_Stemming
                        #str_not_existed = "_X+2"
                        #str_not_existed_in_front = "_X-1"
                        #str_not_existed_back = "_X+1"
                        target_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_target_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_target_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)
                        source_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_source_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_source_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)

                        try:
                                #xet target
                                target_res = list_target[index_of_target_word]

                                if index_of_target_word == 0:
                                        #khong co: Left_Target
                                        right_target_res = list_target[index_of_target_word + 1]

                                elif index_of_target_word == len(list_alignment_target_to_source) - 1:  #tu cuoi cau
                                        #khong co: Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                else:  #co ca 2 Left_Target & Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                        right_target_res = list_target[index_of_target_word + 1]
                        except IndexError:
                                #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                pass

                        #xet source
                        #index_alignment_of_source_word = -1 #khong co tu nao giong den
                        if index_alignment_of_source_word == -1:  #khong co lien ket nao den tu nguon
                                pass
                        else:
                                try:
                                        source_res = list_source[index_alignment_of_source_word]

                                        if index_alignment_of_source_word == 0:
                                                #khong co: Left_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                        elif index_alignment_of_source_word == len(list_source) - 1:  #tu cuoi cua NGUON
                                                #khong co: Right_Source
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                        else:  #co ca 2 Left_Source va Right_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                except IndexError:
                                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                        #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                        pass

                        #end if

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        cap1 = target_res + right_target_res
                        cap2 = left_target_res + source_res
                        cap3 = right_source_res + left_source_res

                        line_output = cap1 + "\t" + cap2 + "\t" + cap3

                        #ghi ra file output voi format la column
                        file_writer.write(line_output)
                        file_writer.write("\n")  # new line
                        """
                        print("*line_output*")
                        print(line_output)
                        print("*line_output*")
                        """
                #end for

                #print("Da xu ly xong cau thu %d" %number_of_sentence)
                number_of_sentence = number_of_sentence + 1
                file_writer.write("\n")  # new line for new sentence

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
        #end for

        #close files
        #file_reader_output_from_moses.close()

        #for writing: file_output_path
        file_writer.close()


#**************************************************************************#
def get_alignment_features_with_output_fast_align(file_output_from_fast_align_path,
                                                  file_output_treetagger_ref_test_source_language,
                                                  file_output_treetagger_mt_test_target_language,
                                                  file_target_ref_test_format_row, file_output_path):
        """
        Creating the requirements for extracting features such as:
        --version 2-- --> version 3 co them stemming

        FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
        EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

        +Target_Word
        +Target_POS

        +Right_Target_Context
        +Right_Target_POS

        +Left_Target_Context
        +Left_Target_POS

        -Source_Word
        -Source_POS

        -Right_Source_Context
        -Right_Source_POS

        -Left_Source_Context
        -Left_Source_POS
        ======================================================================================================
        :type file_output_from_fast_align_path: string
        :param file_output_from_fast_align_path: the ouput included alignment word to word from target to source (Phraoh format)

        :type file_output_treetagger_ref_test_source_language: string
        :param file_output_treetagger_ref_test_source_language: Reference Test in Source Language - each line contains output of tool TreeTagger in row format

        :type file_output_treetagger_mt_test_target_language: string
        :param file_output_treetagger_mt_test_target_language: Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger in row format

        :type file_target_ref_test_format_row: string
        :param file_target_ref_test_format_row: Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger in row format

        :type file_output_path: string
        :param file_output_path:each line contains (Word; POS; Stemming) of Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

        :raise ValueError: if any path is not existed
        """
        # check existed paths
        """
        if not os.path.exists(file_output_from_fast_align_path):
                raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

        if not os.path.exists(file_output_treetagger_ref_test_source_language):
                raise TypeError('Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger.')

        if not os.path.exists(file_output_treetagger_mt_test_target_language):
                raise TypeError('Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger.')
        """
        str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path"
        is_existed_file(file_output_from_fast_align_path, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Reference Test in Source Language - each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_ref_test_source_language, str_message_if_not_existed)

        str_message_if_not_existed = "Not Existed file Result of Machine Translation (n-best-list given by MOSES) in Target Language each line contains output of tool TreeTagger"
        is_existed_file(file_output_treetagger_mt_test_target_language, str_message_if_not_existed)

        #for reading: file_output_from_fast_align_path
        file_reader_output_from_fast_align = open(file_output_from_fast_align_path, mode='r', encoding='utf-8')
        """
        current_config = load_configuration()

        path_to_tool_giza = current_config.PATH_TO_TOOL_GIZA
        path_to_tool_mkcls = current_config.PATH_TO_TOOL_MKCLS
        path_to_corpus = current_config.PATH_TO_CORPUS
        source_corpus_name = current_config.SOURCE_CORPUS_NAME
        target_corpus_name = current_config.TARGET_CORPUS_NAME

        get_alignment_by_giza(path_to_tool_giza, path_to_tool_mkcls, path_to_corpus, source_corpus_name, target_corpus_name)
        """

        #get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE
        #target_source_A3_final: ../extracted_features/en_es.A3.final
        ##current_config.TARGET_SOURCE_A3_FINAL)
        #alignment_target_to_source = get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE(file_output_from_fast_align_path)
        #alignment_target_to_source = get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE_after_optimising(file_output_from_fast_align_path, file_target_ref_test_format_row)

        #print(alignment_target_to_source) #[1, 3, 4, 5, 6, 6, -1, 6, 6, 7]

        #print("len = %d" %len(alignment_target_to_source))

        #for writing: file_output_path
        file_writer = open(file_output_path, mode='w', encoding='utf-8')

        # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
        number_of_sentence = 1
        delimiter_char = "|||"
        str_not_existed = "_X+2"
        str_not_existed_in_front = "_X-1"
        str_not_existed_back = "_X+1"

        for line_in_output_from_fast_align in file_reader_output_from_fast_align:
                #for list_alignment_target_to_source in alignment_target_to_source:
                """
                #can kiem tra lai du lieu cau thu 881
                #da kiem tra ok, ly do: tu format column chuyen sang format row bi mat sentence column cuoi cung, vi trong file format column khong co dong trong cuoi cung --> giai phap: cap nhat ham convert them flag de kiem tra "da duoc luu" hay chua True/False ?
                if number_of_sentence != 881:
                        number_of_sentence = number_of_sentence +1
                        continue
                """
                """
                print("*******************************************")
                print("Dang duyet cau thu: %d " %number_of_sentence)
                print("*******************************************")
                print(line_in_output_from_fast_align)
                print("*******************************************")
                """
                #list_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                #trim string
                #line_in_output_from_fast_align = line_in_output_from_fast_align.strip()

                if len(line_in_output_from_fast_align.strip()) == 0:
                        #print("Xuat hien dong trong - Empty line ... You should check corpus...")
                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                        continue

                #Duyet Tung cau dich va cau moses va xet
                #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_from_fast_align) #version 1 - Target - Source _ nhom cuoi cua MOSES output
                #updated 2015.Jan.06 by Tien LE

                #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_from_fast_align)

                #config_end_user = load_config_end_user()

                line_target_ref_test_format_row = get_line_given_number_of_sentence(file_target_ref_test_format_row,
                                                                                    number_of_sentence)

                list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_fast_align_TARGET_To_SOURCE(
                        line_in_output_from_fast_align, line_target_ref_test_format_row)


                #list_alignment_target_to_source = []
                #list_alignment_target_to_source = line

                """
                print("*list_alignment_target_to_source*")
                print(list_alignment_target_to_source)
                print("*list_alignment_target_to_source*")
                """

                #***************************can update cho nay
                #file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of

                #get temp_longest_source_gram_length_not_aligned_target_row
                #line_longest_source_gram_length = get_line_given_number_of_sentence(file_temp_longest_source_gram_length_not_aligned_target_row_path, number_of_sentence)
                #list_longest_source_gram_length = line_longest_source_gram_length.split() #Delimiter default = " "

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                list_source = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_ref_test = get_line_given_number_of_sentence(
                        file_output_treetagger_ref_test_source_language, number_of_sentence)

                line_output_treetagger_ref_test = line_output_treetagger_ref_test.replace("\n", "")
                """
                print("*line_output_treetagger_ref_test*")
                print(line_output_treetagger_ref_test)
                print("*line_output_treetagger_ref_test*")
                """
                #trim
                line_output_treetagger_ref_test = line_output_treetagger_ref_test.strip()  #strim line

                #split
                list_output_treetagger_ref_test = line_output_treetagger_ref_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_ref_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_ref_test:  #les|||DET|||le
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_source.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))

                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                list_target = []  #gom danh sach voi moi tu la mot doi tuong lop Word_POS_Stemming
                line_output_treetagger_mt_test = get_line_given_number_of_sentence(
                        file_output_treetagger_mt_test_target_language, number_of_sentence)

                line_output_treetagger_mt_test = line_output_treetagger_mt_test.replace("\n", "")
                """
                print("*line_output_treetagger_mt_test*")
                print(line_output_treetagger_mt_test)
                print("*line_output_treetagger_mt_test*")
                """
                line_output_treetagger_mt_test = line_output_treetagger_mt_test.strip()  #strim line

                list_output_treetagger_mt_test = line_output_treetagger_mt_test.split()  #Delimiter default = " "

                #duyet danh sach va dua moi tu vao 1 doi tuong lop Word_POS_Stemming
                if len(list_output_treetagger_mt_test) == 0:
                        raise Exception("You should check data in list_output_treetagger_ref_test")
                else:
                        for item_temp in list_output_treetagger_mt_test:  #the|||DT|||the
                                list_item_temp = item_temp.split(delimiter_char)

                                if len(list_item_temp) == 0:
                                        raise Exception("You should check data in list_item_temp")

                                #list_item_temp[0],list_item_temp[1],list_item_temp[2]
                                list_target.append(Word_POS_Stemming(list_item_temp[0], list_item_temp[1], list_item_temp[2]))
                """
                print("*number_of_sentence*")
                print(number_of_sentence)
                print("*number_of_sentence*")

                print("*list_source*")
                print(list_source)
                print("*list_source*")

                print("*list_target*")
                print(list_target)
                print("*list_target*")
                """

                #line_output = [] #mang luu ket qua cac tu ket noi theo dinh danh da mo ta o phia dau file; Target; Right_Target; Left_Target; Source; Right_Source; Left_Source. Moi phan tu tren la mot doi tuong Word_POS_Stemming
                ##Target; Right_Target; Left_Target; Source; Right_Source; Left_Source

                #source language
                #FR: les|||DET|||le chirurgiens|||NOM|||chirurgien de|||PRP|||de
                #list_source = []
                #hypothesis
                #EN: the|||DT|||the chirurgiens|||NNS|||chirurgiens of|||IN|||of
                #list_target = []

                #Danh sach cac tu dich voi moi phan tu la 1 object Word_Target_Language
                #list_of_words_alignment_target_to_source = []

                #target_sentence = get_target_sentence_from_output_moses(line_in_output_moses)

                #number_of_words_in_target_sentence = len(target_sentence.split())

                """
                print("***************************************")
                print("So tu trong target sentence la: %d " %number_of_words_in_target_sentence)
                print("***************************************")
                """

                #range_sentence = range(number_of_words_in_target_sentence)

                """
                print("*range_sentence*")
                print(range_sentence)
                print("*range_sentence*")
                """

                #Khoi tao danh sach ket qua
                #for i in range_sentence:
                #    obj_word_target_language = Word_Target_Language() # create instance

                #    list_of_words_alignment_target_to_source.append(obj_word_target_language)
                #end for

                #xu ly danh sach ket qua
                #0  1  2    3  ... n-1
                #0  1  2,3  '' ....    #'' co nghia la khong co phan tu nao lien ket, list_alignment_target_to_source
                #1  2  3,2  0  ....   #list_longest_source_gram_length
                comma_char = ","

                """
                print("*list_alignment_target_to_source**********************")
                print(list_alignment_target_to_source)
                print("*len**list_alignment_target_to_source*****************")
                print(len(list_alignment_target_to_source))
                print("*list_alignment_target_to_source**********************")
                """

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
                        index_alignment_of_source_word = -1  #khong co tu nao giong den

                        list_temp = []  # empty list

                        #lay chuoi ra, neu chua dau phay ,
                        if is_in_string(comma_char, index_alignment_to_source):  #co tu 2 lien ket voi nguon tro len
                                list_temp = index_alignment_to_source.split(comma_char)
                                index_alignment_of_source_word = int(list_temp[0])  #chi can xet tu dau tien duoc giong len Source

                        else:  #neu chi la 1 so nguyen, khong chua dau phay , co nghia la: chi chua 1 phan tu
                                list_temp.append(str(index_alignment_to_source))
                                try:
                                        index_alignment_of_source_word = int(index_alignment_to_source)
                                except ValueError:
                                        pass  #index_alignment_of_source_word = index_alignment_to_source #neu chua "" thi bi loi cho nay
                        #end if

                        index_of_target_word = i  #index cua tu dich

                        """
                        print("*index_of_target_word*")
                        print(index_of_target_word)
                        print("*index_of_target_word*")

                        print("*index_alignment_of_source_word*")
                        print(index_alignment_of_source_word)
                        print("*index_alignment_of_source_word*")
                        """
                        #print("*list_source*")
                        #print(list_source)
                        #print("*list_source*")

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        #Word_POS_Stemming
                        #str_not_existed = "_X+2"
                        #str_not_existed_in_front = "_X-1"
                        #str_not_existed_back = "_X+1"
                        target_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_target_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_target_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)
                        source_res = Word_POS_Stemming(str_not_existed, str_not_existed, str_not_existed)
                        right_source_res = Word_POS_Stemming(str_not_existed_back, str_not_existed_back, str_not_existed_back)
                        left_source_res = Word_POS_Stemming(str_not_existed_in_front, str_not_existed_in_front,
                                                            str_not_existed_in_front)

                        try:
                                #xet target
                                target_res = list_target[index_of_target_word]

                                if index_of_target_word == 0:
                                        #khong co: Left_Target
                                        right_target_res = list_target[index_of_target_word + 1]

                                elif index_of_target_word == len(list_alignment_target_to_source) - 1:  #tu cuoi cau
                                        #khong co: Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                else:  #co ca 2 Left_Target & Right_Target
                                        left_target_res = list_target[index_of_target_word - 1]
                                        right_target_res = list_target[index_of_target_word + 1]
                        except IndexError:
                                #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                pass

                        #xet source
                        #index_alignment_of_source_word = -1 #khong co tu nao giong den
                        if index_alignment_of_source_word == -1:  #khong co lien ket nao den tu nguon
                                pass
                        else:
                                try:
                                        source_res = list_source[index_alignment_of_source_word]

                                        if index_alignment_of_source_word == 0:
                                                #khong co: Left_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                        elif index_alignment_of_source_word == len(list_source) - 1:  #tu cuoi cua NGUON
                                                #khong co: Right_Source
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                        else:  #co ca 2 Left_Source va Right_Source
                                                right_source_res = list_source[index_alignment_of_source_word + 1]
                                                left_source_res = list_source[index_alignment_of_source_word - 1]
                                except IndexError:
                                        #print("Xem lai cau %d nha!!!???" % number_of_sentence)
                                        #print("Bi loi IndexError. Kiem tra lai nha :)))")
                                        pass

                        #end if

                        #Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
                        cap1 = target_res + right_target_res
                        cap2 = left_target_res + source_res
                        cap3 = right_source_res + left_source_res

                        line_output = cap1 + "\t" + cap2 + "\t" + cap3

                        #ghi ra file output voi format la column
                        file_writer.write(line_output)
                        file_writer.write("\n")  # new line
                        """
                        print("*line_output*")
                        print(line_output)
                        print("*line_output*")
                        """
                #end for

                #print("Da xu ly xong cau thu %d" %number_of_sentence)
                number_of_sentence = number_of_sentence + 1
                file_writer.write("\n")  # new line for new sentence

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
        #end for

        #close files
        file_reader_output_from_fast_align.close()

        #for writing: file_output_path
        file_writer.close()

#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
        #Test case:
        #feature_backoff_behaviour(file_input_path, file_output_path)

        current_config = load_configuration()
        config_end_user = load_config_end_user()

        #list1 = get_list_word_pos_stemming_from_output_treetagger(current_config.REF_TEST_OUTPUT_TREETAGGER_SOURCE_LANGUAGE)

        #list2 = get_list_word_pos_stemming_from_output_treetagger(current_config.MT_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE)

        #for item in list2:
        #    print(item.get_word())

        #get_file_contains_number_of_words_each_line(file_input_path, file_output_path)
        #get_file_contains_number_of_words_each_line(current_config.SRC_REF_TEST, current_config.SRC_REF_TEST_NUMBER_OF_WORDS)

        #get_file_contains_number_of_words_each_line(current_config.TARGET_REF_TEST, current_config.TARGET_REF_TEST_NUMBER_OF_WORDS)

        #convert_format_column_to_format_row_from_output_treetagger(file_input_path, file_number_of_words_path, file_output_path)
        #convert_format_column_to_format_row_from_output_treetagger(current_config.REF_TEST_OUTPUT_TREETAGGER_SOURCE_LANGUAGE, current_config.SRC_REF_TEST_NUMBER_OF_WORDS, current_config.REF_TEST_OUTPUT_TREETAGGER_SOURCE_LANGUAGE_FORMAT_ROW)


        #convert_format_column_to_format_row_from_output_treetagger(file_input_path, file_output_path)
        #in common_functions
        #convert_format_column_to_format_row_from_output_treetagger(current_config.REF_TEST_OUTPUT_TREETAGGER_SOURCE_LANGUAGE, current_config.REF_TEST_OUTPUT_TREETAGGER_SOURCE_LANGUAGE_FORMAT_ROW)

        #convert_format_column_to_format_row_from_output_treetagger(current_config.MT_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE, current_config.MT_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE_FORMAT_ROW)

        #chuyen sang cach khac lam viec voi treetagger trong moses
        #get_alignment_features(file_output_from_moses_included_alignment_word_to_word_path, file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language, file_output_path)
        print(current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW)
        print(current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW)
        #get_alignment_features( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.ALIGNMENT_FEATURES)

        #Cach 1: get_alignment_features(file_output_from_fast_align_path, file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language, file_output_path)
        #Voi cach lam nay thi xuat hien 7 dong bi alignment sai, lech 120 tu
        #get_alignment_features_with_output_giza( current_config.TARGET_SOURCE_A3_FINAL, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.ALIGNMENT_FEATURES)

        #Cach 2: voi cach lam nay thi khong bi lech, va khac phuc nhuoc diem cua cach tren bang cach gan ban dau la -1
        #get_alignment_features_with_output_giza_after_optimising( current_config.TARGET_SOURCE_A3_FINAL, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.ALIGNMENT_FEATURES)

        #Cach 3: Khong dung Giza++, dung fast-align --> tool nay dung khong tot doi voi EN_ES ???
        #B1: tao input phu hop voi fast-align
        #creating_input_format_for_tool_fast_align(file_input_source_language_path, file_input_target_language_path, file_output_path)
        #creating_input_format_for_tool_fast_align(current_config.SRC_REF_TEST_FORMAT_ROW, current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.SRC_TARGET_REF_TEST_FORMAT_ROW)

        #B2: Dung fast_align de lay alignment target-source
        #get_word_alignment_using_tool_fast_align(file_input_path, file_output_alignment_source_to_target_path, file_output_alignment_target_to_source_path)
        #get_word_alignment_using_tool_fast_align(current_config.SRC_TARGET_REF_TEST_FORMAT_ROW, current_config.ALIGNMENT_SRC_TGT_FORMAT_ROW, current_config.ALIGNMENT_TGT_SRC_FORMAT_ROW)

        #B3: get_alignment_features_with_output_fast_align( file_output_from_fast_align_path, file_output_treetagger_ref_test_source_language, file_output_treetagger_mt_test_target_language,  file_target_ref_test_format_row, file_output_path)
        #get_alignment_features_with_output_fast_align( current_config.ALIGNMENT_TGT_SRC_FORMAT_ROW, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.ALIGNMENT_FEATURES)

        #Cach 4: Dung tool moses de lay alignment va lay theo dang 1-best-list
        #get_file_alignments_target_to_source_word_alignment_using_moses(pattern_file_path, extension_source, extension_target, path_to_tool_giza, output_directory_path, file_output_path)
        #command_line = command_line + script_path + " -corpus "+ current_config.PATTERN_REF_TEST_FORMAT_ROW + " -f "+ current_config.EXTENSION_SOURCE +" -e "+ current_config.EXTENSION_TARGET + " -alignment grow-diag-final-and --first-step 1 --last-step 3 --external-bin-dir="+ config_end_user.PATH_TO_TOOL_GIZA +" --model-dir=" + current_config.MODEL_DIR_PATH
        #moved this function to pre-processing
        #get_file_alignments_target_to_source_word_alignment_using_moses( current_config.PATTERN_REF_TEST_FORMAT_ROW, current_config.EXTENSION_SOURCE, current_config.EXTENSION_TARGET, config_end_user.PATH_TO_TOOL_GIZA, current_config.MODEL_DIR_PATH, current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT)

        get_alignment_features(current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT,
                               current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW,
                               current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW,
                               current_config.ALIGNMENT_FEATURES)

        print('OK')
        #**************************************************************************#
        #**************************************************************************#
        #**************************************************************************#
        #**************************************************************************#
        #**************************************************************************#