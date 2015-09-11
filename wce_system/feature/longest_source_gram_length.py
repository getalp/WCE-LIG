# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 18:20:02 2014
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
#Tim n-gram dai nhat doi voi source language
Vi du:
Source FR S1 S2 S3 .
Target EN T1 T2 T3 T4 T5 .

*** Truong hop 1: T2 giong voi S1, S2, S3 --> Chi xet tu dau tien S1 (Trong truong hop co giong hang nhieu)

*** Truong hop 2: T3 giong voi S2, ta co:
S1: Source Left
S3: Source Right

T2: Target Left
T4: Target Right

*** Trong moses - decoder: co Align Target - Source
*** Cac file phai duoc tokenized va lowercased.
Buoc 0: + File chua aligned tu moses
		 + Tokenized va Lowercased file source language.

Buoc 1: File Source-4gram giong nhu cach lam Target-4gram
Buoc 2: ~GeTools/SourceLMFeature$ ./createSourceNGram.sh 3lines-aligned.es-en.aftercorrect 3lines-wmt13qe_t2.tr.source.tok.tc.lc 3lines-4gram-source-v1

#0 ||| at the end of trade , the stock market in prague in the negative bascula  ||| d: -5 -1.84123 0 -1.02296 -0.899405 0 -2.03688 lm: -173.642 tm: -12.3405 -21.3238 -6.29871 -17.3129 5.99938 w: -15 ||| -185.316 ||| 0-1=0-2 2-3=3-4 4-6=5-8 7-8=9-10 10=11 11-12=12-13 9=14 ||| 0=0,1 1=2 2=3 3=4 4=5 5=6 6=7,8 7=9 8=10 10=11 11=12 12=13 9=14 ||| 0=0 1=0 2=1 3=2 4=3 5=4 6=5 7=6 8=6 9=7 10=8 11=10 12=11 13=12 14=9

meaning: ref Manual MOSES pages 160, 161
0 --> sentence number (the first sentence)
at ... bascula --> output sentence the best n-list
d: -5 ... w: -15 --> individual component scores (unweighted)
-185.316: weighted overall score
0=0,1 ... 9=14: The SOURCE to TARGET alignment
0=0 ... 14=9: The SOURCE to TARGET alignment

Example (ref page 161 - Manual MOSES 2014)
SOURCE - DE (German): ich frage
TARGET - EN (English): i ask this
*** The SOURCE to TARGET alignment: 0=0 1=1
German --> English
ich    --> i
frage  --> ask

*** The TARGET to SOURCE alignment: 0=0 1=1 2=-1 means that:
English --> German
i       --> ich
ask     --> frage
this    -->

Explain: "2=-1" means that the word of index 2 is not associated with any word in the other language


Chu y: cap nhat dong code trong file 'createSourceNGram.sh' nhu sau:
#done < "aligned.en-fr";
done < $1;

*** Ket qua: trong file 'ngram-sources' co dang:
4
3
	0gram
2

Buoc 3: Thay the '0gram' thanh so 0

#Bo tab truoc 0gram
#awk '{print $1}' < ngram-sources > ngram-sources-bo-tab

#Bo chuoi 'gram'
#sed s/gram//g < ngram-sources-bo-tab > source-ngram

Da tong hop thanh dong lenh shell:
~GeTools/SourceLMFeature$ ./myCreate-source-ngram-feature.sh ngram-sources result-sources-ngram

result:
2 : means that "Tu DICH tai index 0 canh le voi tu NGUON co longest gram length la 2 trong Language Model cua ngon ngu NGUON "
3
4
2
3

....

"""

import os
import sys

#for call shell script
#import shlex, subprocess

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from feature.longest_target_gram_length import get_probability_from_language_model, create_longest_target_gram_length, get_probability_from_language_model_threads, create_longest_target_gram_length_threads
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import is_existed_file, get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE, get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET, convert_format_column_to_format_row, get_line_given_number_of_sentence
from common_module.cm_util import  is_in_string
#**************************************************************************#
#Buoc 1.0: File Source-ngram giong nhu cach lam Target-ngram
#ref: in module "longest_target_gram_length.py"
def get_temp_longest_source_gram_length_not_aligned_target(file_input_path, language_model_path,  n_gram, file_output_path):

    current_config = load_configuration()

    #Buoc 1: Tao file chua xac suat theo tung gram (Language Model)
    #Goi ham ngram tu SRILM
    #Test case: checking the function
    #get_probability_from_language_model(file_input_path, language_model_path,  n_gram, file_output_path)
    get_probability_from_language_model(file_input_path, language_model_path,  n_gram, current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE)

    #get_probability_from_language_model(current_config.ROW_CORPUS_SOURCE_LANGUAGE, current_config.LANGUAGE_MODEL_FR, 5, current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE)

    #Buoc 2:
    #create_longest_target_gram_length(file_input_path, file_output_path)
    #create_longest_target_gram_length(current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET)
    create_longest_target_gram_length(current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE, file_output_path)

#--------------------------------------------------------------------------#
#in common_functions
#convert_format_column_to_format_row(file_input_path, file_output_path)

#**************************************************************************#
def get_temp_longest_source_gram_length_not_aligned_target_threads(file_input_path, language_model_path,  n_gram, file_output_path, current_config, config_end_user):

    #current_config = load_configuration()

    #Buoc 1: Tao file chua xac suat theo tung gram (Language Model)
    #Goi ham ngram tu SRILM
    #Test case: checking the function
    #get_probability_from_language_model(file_input_path, language_model_path,  n_gram, file_output_path)
    get_probability_from_language_model_threads(file_input_path, language_model_path,  n_gram, current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE, current_config, config_end_user)

    #get_probability_from_language_model(current_config.ROW_CORPUS_SOURCE_LANGUAGE, current_config.LANGUAGE_MODEL_FR, 5, current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE)

    #Buoc 2:
    #create_longest_target_gram_length(file_input_path, file_output_path)
    #create_longest_target_gram_length(current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET)
    create_longest_target_gram_length_threads(current_config.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE, file_output_path, current_config)

#--------------------------------------------------------------------------#
#in common_functions
#convert_format_column_to_format_row(file_input_path, file_output_path)

#**************************************************************************#
class Word_Source(object):
    """
    Containing the following items: INDEX, LONGEST GRAM LENGTH of the source word
    """
    index = 0
    longest_gram_length = 0

    def __init__(self):
        self.index = 0
        self.longest_gram_length = 0

    def __init__(self, index, longest_gram_length):
        self.index = index
        self.longest_gram_length = longest_gram_length

    @property
    def p_index(self):
        return self.index

    @property
    def p_longest_gram_length(self):
        return self.longest_gram_length

    def set_index(self, index=0):
        self.index = index

    def set_longest_gram_length(self, longest_gram_length=0):
        self.longest_gram_length = longest_gram_length

    def get_index(self):
        return self.index

    def get_longest_gram_length(self):
        if self.longest_gram_length == "" or self.longest_gram_length == "-1":
            self.longest_gram_length = 0

        return int(self.longest_gram_length)
#---------------------------------------------------------------------------#
class Word_Target_Language(object):
    """
    Creating Class for containing the following items:
    + list_of_words_aligned_to_source: danh sach cac tu nguon duoc aligned voi tu dich hien tai, moi phan tu trong danh sach luu tru cac thong tin cua tu nguon nhu: INDEX, LONGEST GRAM LENGTH --> Moi doi tuong la object "Word_Source"
    + get first item, min, max, int(average) cua GRAM LENGTH ma tu dich hien tai aligned
    """
    #index = 0 #Khong can dung index nay, vi chung ta dung index cua list chua cac tu dich
    #list_of_words_aligned_to_source = []
    #first_item_longest_source_gram_length_aligned_target = 0
    #min_longest_source_gram_length_aligned_target = 0
    #max_longest_source_gram_length_aligned_target = 0
    #avg_longest_source_gram_length_aligned_target = 0

    """
    def __init__(self):
        #obj_Word_Source = Word_Source() #new instance

        self.list_of_words_aligned_to_source = []
        #self.list_of_words_aligned_to_source = obj_Word_Source
        self.first_item_longest_source_gram_length_aligned_target = 0
        self.min_longest_source_gram_length_aligned_target = 0
        self.max_longest_source_gram_length_aligned_target = 0
        self.avg_longest_source_gram_length_aligned_target = 0
    """

    def __init__(self, list_of_words_aligned_to_source):
        #print("Su dung ham khoi tao nay ... DUNG")

        #ban dau gan danh sach nay la rong
        self.list_of_words_aligned_to_source = []

        if len(list_of_words_aligned_to_source) == 0:
            print("Danh sach truyen vao khong co phan tu nao")
        else:

            for item in list_of_words_aligned_to_source:
                obj_word_source = Word_Source(item.get_index(), item.get_longest_gram_length())

                self.list_of_words_aligned_to_source.append(obj_word_source)
                #print(item.get_index())
                #print(item.get_longest_gram_length())

            """
            print("Danh sach truyen vao lop Word_Target_Language - BEGIN")
            for item_temp in self.list_of_words_aligned_to_source:
                print("index")
                print(item_temp.get_index())
                print("longest gram length")
                print(item_temp.get_longest_gram_length())

            print("Danh sach truyen vao lop Word_Target_Language - END")
            """

        self.first_item_longest_source_gram_length_aligned_target =0
        self.min_longest_source_gram_length_aligned_target = 0
        self.max_longest_source_gram_length_aligned_target = 0
        self.avg_longest_source_gram_length_aligned_target = 0

        """
        print("init*longest_source_gram_length_aligned_target*")
        print(self.first_item_longest_source_gram_length_aligned_target)
        print(self.min_longest_source_gram_length_aligned_target)
        print(self.max_longest_source_gram_length_aligned_target)
        print(self.avg_longest_source_gram_length_aligned_target)
        print("init*longest_source_gram_length_aligned_target*")
        """

    #set properties
    def set_list_of_words_aligned_to_source(self, list_of_words_aligned_to_source = []):
        self.list_of_words_aligned_to_source = list_of_words_aligned_to_source

    def set_first_item_longest_source_gram_length_aligned_target(self, first_item_longest_source_gram_length_aligned_target = 0):
        self.first_item_longest_source_gram_length_aligned_target = first_item_longest_source_gram_length_aligned_target

    def set_min_longest_source_gram_length_aligned_target(self, min_longest_source_gram_length_aligned_target = 0):
        self.min_longest_source_gram_length_aligned_target = min_longest_source_gram_length_aligned_target

    def set_max_longest_source_gram_length_aligned_target(self, min_longest_source_gram_length_aligned_target = 0):
        self.max_longest_source_gram_length_aligned_target = min_longest_source_gram_length_aligned_target

    def set_avg_longest_source_gram_length_aligned_target(self, min_longest_source_gram_length_aligned_target = 0):
        self.avg_longest_source_gram_length_aligned_target = min_longest_source_gram_length_aligned_target

    #get properties
    def get_list_of_words_aligned_to_source(self):
        return self.list_of_words_aligned_to_source

    def get_first_longest_source_gram_length_aligned_target(self):
        if len(self.list_of_words_aligned_to_source) == 0:
            return 0

        #Duyen list roi return phan tu co index nho nhat
        result = self.list_of_words_aligned_to_source[0].get_longest_gram_length()
        index_min = self.list_of_words_aligned_to_source[0].get_index()

        for item in self.list_of_words_aligned_to_source:
            if index_min > item.get_index():
                index_min = item.get_index()
                result = item.get_longest_gram_length()
                """
                print("index_min cap nhat la: %d" %index_min)
                print("gia tri cap nhat la: %d" %result)
                """
        return result

        #return self.list_of_words_aligned_to_source[0].get_longest_gram_length()

    def get_min_longest_source_gram_length_aligned_target(self):
        if len(self.list_of_words_aligned_to_source) == 0:
            return 0

        #Duyen list roi return phan tu nho nhat
        result = self.list_of_words_aligned_to_source[0].get_longest_gram_length()
        for item in self.list_of_words_aligned_to_source:
            if result > item.get_longest_gram_length():
                result = item.get_longest_gram_length()
        return result

    def get_max_longest_source_gram_length_aligned_target(self):
        if len(self.list_of_words_aligned_to_source) == 0:
            print("Khong co phan tu nao trong danh sach truyen vao lop nay ??? ")
            return 0

        """
        print("Kiem tra - Danh sach truyen vao lop Word_Target_Language - BEGIN")
        for item_temp in self.list_of_words_aligned_to_source:
            print("index")
            print(item_temp.get_index())
            print("longest gram length")
            print(item_temp.get_longest_gram_length())
        print("Kiem tra - Danh sach truyen vao lop Word_Target_Language - END")
        """

        #Duyen list roi return phan tu nho nhat
        result = self.list_of_words_aligned_to_source[0].get_longest_gram_length()
        for item in self.list_of_words_aligned_to_source:
            if result < item.get_longest_gram_length():
                result = item.get_longest_gram_length()
        return result

    #version 2
    def get_max_longest_source_gram_length_aligned_target_new(self, list_temp):
        if len(list_temp) == 0:
            print("Khong co phan tu nao trong danh sach truyen vao lop nay ??? ")
            return 0

        """
        print("Kiem tra - Danh sach truyen vao lop Word_Target_Language - BEGIN")
        for item_temp in list_temp:
            print("index")
            print(item_temp.get_index())
            print("longest gram length")
            print(item_temp.get_longest_gram_length())
        print("Kiem tra - Danh sach truyen vao lop Word_Target_Language - END")
        """

        #Duyen list roi return phan tu nho nhat
        result = list_temp[0].get_longest_gram_length()
        for item in list_temp:
            if result < item.get_longest_gram_length():
                result = item.get_longest_gram_length()
        return result

    def avg_integer(my_list):
        sum = 0
        for item in my_list:
            sum = sum + item.get_longest_gram_length()

        return sum//len(my_list) #lay phan nguyen

    def get_avg_longest_source_gram_length_aligned_target(self):
        if len(self.list_of_words_aligned_to_source) == 0:
            return 0

        sum = 0
        for item in self.list_of_words_aligned_to_source:
            sum = sum + item.get_longest_gram_length()
        """
        print("*sum*")
        print(sum)
        print("*sum*")
        """

        #return avg_integer(self.list_of_words_aligned_to_source)
        return sum//len(self.list_of_words_aligned_to_source)

#---------------------------------------------------------------------------#
#Tu file alignment cua moses, chung ta lay mang cua cac tu dich duoc lien ket (aligned) voi tu nguon
#can tra ve them so tu trong target language
def get_file_alignment_target_to_source(file_output_from_moses_included_alignment_word_to_word_path, file_output_alignment_target_to_source_path):
    """
    Creating a file of alignments The TARGET to SOURCE
    ======================================================
    0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15

    :type file_output_from_moses_included_alignment_word_to_word_path: string
    :param file_output_from_moses_included_alignment_word_to_word_path: the ouput from moses best_n_list included alignment word to word

    :type file_output_alignment_target_to_source_path: string
    :param file_output_alignment_target_to_source_path: the ouput included alignment word to word from target to source

    :rtype: return the number of the words in the target language

    :raise ValueError: if any path is not existed
    """
    #list_alignment_target_to_source = []

    # check existed path
    """
    if not os.path.exists(file_output_from_moses_included_alignment_word_to_word_path):
        raise TypeError('Not Existed file output from moses included alignment word to word path')
    """
    str_message_if_not_existed = "Not Existed file output from moses included alignment word to word pathn"
    is_existed_file(file_output_from_moses_included_alignment_word_to_word_path, str_message_if_not_existed)

    #for reading: file_output_from_moses_included_alignment_word_to_word_path
    file_reader_output_from_moses = open(file_output_from_moses_included_alignment_word_to_word_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_alignment_target_to_source_path
    file_writer = open(file_output_alignment_target_to_source_path, mode = 'w', encoding = 'utf-8')#, 'w')

    delimiter = "|||"
    num_of_sentence = 0

    for line in file_reader_output_from_moses:
        list_of_group = [] #gan danh sach cac nhom la RONG
        line = line.strip() #trim 2 dau cua chuoi line

        if len(line) == 0:
            print("Chu y: Kiem tra lai du lieu vi co dong TRONG - Empty line. Hay het file ?!?!... Contact to Tien LE :)")
            break

        # split cac nhom khac nhau --> chon nhom cuoi
        list_of_group = line.split(delimiter)

        #lay nhom cuoi
        alignment_target_to_source = list_of_group[len(list_of_group)-1]

        #trim string alignment
        alignment_target_to_source = alignment_target_to_source.strip()

        #print("Just for testing :) \nIndex-number of Sentence : %d " %num_of_sentence)
        num_of_sentence = num_of_sentence + 1
        #print(alignment_target_to_source)

        #ghi vao file output
        file_writer.write(alignment_target_to_source)
        file_writer.write("\n") # new line

    #close files
    file_reader_output_from_moses.close()
    file_writer.close()
#---------------------------------------------------------------------------#
def get_list_alignment_target_to_source2(string_output_alignment_target_to_source_path):
    """
    Creating list of alignment word to word from target to source
    =============================================================
    0-0 1-1 2-2 3-3 4-4 5-5 7-6 6-7 8-8 9-9 10-10 11-11 12-12 13-13 14-14 15-15 16-16 17-17 20-19 18-20 19-21 21-22 22-23 23-24

    :type string_output_alignment_target_to_source_path: string
    :param string_output_alignment_target_to_source_path: the string of ouput included alignment word to word from target to source

    :rtype: list of alignment word to word from target to source, Note: if value = '' then value=-1 that means there is no word in Source language associated.
    """
    result = [] # empty list
    list_after_split = [] # contains items after splitting
    char_equal = "=" # Source to Target (in lastest MOSES), Target To Source (in MOSES 2009)
    char_minus = "-" # Target To Source (in lastest MOSES)
    current_char = "" # contains which char in the string-input

    if is_in_string(char_equal,string_output_alignment_target_to_source_path):  # if string-input contains delimiter by "="
        current_char= char_equal
    else: # if string-input contains delimiter by "-"
        current_char= char_minus

    # split string --> {'0-0', '1-1',..., '23-25,26'}
    list_after_split = string_output_alignment_target_to_source_path.split()
    """
    print("*list_after_split*")
    print(list_after_split)
    print("*list_after_split*")
    """
    # find max-index of Target Side (left side) in string-input
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
    """
    #just for testing :)
    print("************************************")
    print("Max index target side in current line: %d" %max_index_target_side)
    print("************************************")
    """
    # tao mang result voi so phan tu bang max_index_target_side + 1
    range_result = range(max_index_target_side + 1)
    for item in range_result:
        result.append(-1) # gia su tu dich nay khong lien ket voi tu nao o nguon

    #duyet lai list_after_split de dua vao list result
    #tai sao lai lam 2 lan nhu vay? --> vi trong list_after_split cac index o left side khong theo tuan tu.
    #vi du: 0-0 1-1 2-2 3-3 4-4 5-5 7-6 6-8 8-9 9-9 11-11 10-12 12-14 15-15 16-16 13-17 14-18 17-19 18-20 19-21 20-22 22-23 21-24 23-25 24-26 25-27
    #left side: index 13 va 14 dung sau 15, 16 --> De bi lap trinh sai neu chi dung index
    #cach 2: chung ta co the gia su danh sach result co 100 phan tu ban dau. Nhung neu lam cach nay thi kho khan trong viec Debug de biet chinh xac so tu trong cau hien tai :) --> chap nhan lam cach 1 :)
    for item in list_after_split:
        split_temp = item.split(current_char) # list contain left and right side of each item in list_after_split
        if len(split_temp) == 0:
            print("Kiem tra lai phan tu trong alignment from Target To Source")
            continue

        value_index_0 = split_temp[0] # left side
        value_index_1 = split_temp[1] # right side

        int_value_index_0 = int(value_index_0)

        #gan gia tri voi index trong result
        result[int_value_index_0] = value_index_1
    """
    print("************************************")
    print("Danh sach result sau khi xu ly la: ")
    print(result)
    print("************************************")
    """
    return result

#---------------------------------------------------------------------------#
#list_of_word_source.append(Word_Source(int_index, list_longest_source_gram_length[int_index]))
#TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX = 1
#TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN = 2
#TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG = 3
#TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST = 4

"""
print("*list_of_word_source*")
for i_temp1 in list_of_word_source:
    print(i_temp1.get_index())
    print(i_temp1.get_longest_gram_length())
print("*list_of_word_source*")
"""


#---------------------------------------------------------------------------#
#longest_source_gram_length_aligned_target
"""
Muc dich them duong dan output aligned-1-best: Kiem tra phan tach tu cua moses va trong file dich co giong nhau hay khong? Neu khac nhau thi ket qua alignment khong the ap dung duoc.
"""
#can viet ham khac de kiem tra tinh hop le cua 2 file tren

#trong ham nay: mac dinh 2 file co cung so tu trong cau dich
def feature_longest_gram_source_length(file_output_from_moses_included_alignment_word_to_word_path,  file_temp_longest_source_gram_length_not_aligned_target_row_path, type_longest_gram_source_length, file_output_path):
    """
    Create longest gram source length
    =============================================================
    2 : means that "Tu DICH tai index 0 canh le voi tu NGUON co longest gram length la 2 trong Language Model cua ngon ngu NGUON "
    3
    4
    2
    3

    :type file_output_from_moses_included_alignment_word_to_word_path: string
    :param file_output_from_moses_included_alignment_word_to_word_path: the ouput included alignment word to word from target to source (MOSES format)

    :type file_temp_longest_source_gram_length_not_aligned_target_row_path: string
    :param file_temp_longest_source_gram_length_not_aligned_target_row_path: file longest source gram length not aligned target path

    :type type_longest_gram_source_length: string
    :param type_longest_gram_source_length: the type of longest gram source length of each target word in the following types {MIN, MAX, AVG, FIRST} ~ TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX

    :type file_output_path: string
    :param file_output_path: longest gram source length of each target word

    :raise ValueError: if any path is not existed
    """

    # check existed paths
    """
    if not os.path.exists(file_output_from_moses_included_alignment_word_to_word_path):
        raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

    if not os.path.exists(file_temp_longest_source_gram_length_not_aligned_target_row_path):
        raise TypeError('Not Existed file Temp Longest SOURCE gram length not aligned TARGET path')
    """
    str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path"
    is_existed_file(file_output_from_moses_included_alignment_word_to_word_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file Temp Longest SOURCE gram length not aligned TARGET path"
    is_existed_file(file_temp_longest_source_gram_length_not_aligned_target_row_path, str_message_if_not_existed)

    #for reading: file_output_from_moses_included_alignment_word_to_word_path
    file_reader_output_from_moses = open(file_output_from_moses_included_alignment_word_to_word_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
    number_of_sentence = 1
    number_of_line = 0
    number_of_word = 0

    for line_in_output_moses in file_reader_output_from_moses:
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
        #trim string
        line_in_output_moses = line_in_output_moses.strip()

        if len(line_in_output_moses) == 0:
            print("Xuat hien dong trong - Empty line ... You should check corpus...")
            print("Xem lai cau %d nha!!!???" %number_of_sentence)
            continue

        #Duyet Tung cau dich va cau moses va xet
        #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
        #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_moses) #version 1 - Target - Source _ nhom cuoi cua MOSES output
        config_end_user = load_config_end_user()
        list_alignment_target_to_source = []

        if config_end_user.VERSION_MOSES == 2009:
            list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(line_in_output_moses)
        else:
            list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)

        #cong 1 co nghia la het 1 cau
        number_of_word += len(list_alignment_target_to_source) + 1
        """
        print("*list_alignment_target_to_source*")
        print(list_alignment_target_to_source)
        print("*list_alignment_target_to_source*")
        """

        #get temp_longest_source_gram_length_not_aligned_target_row
        line_longest_source_gram_length = get_line_given_number_of_sentence(file_temp_longest_source_gram_length_not_aligned_target_row_path, number_of_sentence)
        list_longest_source_gram_length = line_longest_source_gram_length.split() #Delimiter default = " "
        """
        print("*number_of_sentence*")
        print(number_of_sentence)
        print("*number_of_sentence*")

        print("*line_longest_source_gram_length*")
        print(line_longest_source_gram_length)
        print("*line_longest_source_gram_length*")

        print("*list_longest_source_gram_length*")
        print(list_longest_source_gram_length)
        print("*list_longest_source_gram_length*")
        """

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

        for i in range(len(list_alignment_target_to_source)):
            index_alignment_to_source = list_alignment_target_to_source[i]

            """
            print("*index_alignment_to_source**********************")
            print(index_alignment_to_source)
            print("*index_alignment_to_source**********************")
            """

            list_temp = [] # empty list

            #lay chuoi ra, neu chua dau phay ,
            if is_in_string(comma_char, index_alignment_to_source): #co tu 2 lien ket voi nguon tro len
                list_temp = index_alignment_to_source.split(comma_char)

            else: #neu chi la 1 so nguyen, khong chua dau phay , co nghia la: chi chua 1 phan tu
                list_temp.append(str(index_alignment_to_source))
            #end if

            #Duyet cac phan tu trong list_temp de lay longest gram length cua source tuong thich
            """
            print("*list_temp**********************")
            print(list_temp)
            print("*list_temp**********************")
            print(len(list_temp))
            print("*list_temp**********************")
            """

            if len(list_temp) == 0:
                #ghi ra file output voi format la column
                #file_writer.write('0')
                #vi lay 4 gia tri nen lam 4 so 0
                file_writer.write('0\t0\t0\t0')
                file_writer.write("\n") # new line
                number_of_line += 1
                """
                print("*Gia tri la: 0 *")
                print(0)
                print("*Gia tri la: 0 *")
                """
                continue
            else:
                #neu trong list_temp co tu 2 tu nguon duoc noi voi tu dich thi phu thuoc vao type chung ta co ket qua tuong ung
                #print("*Gia tri khac 0 *")

                if list_temp[0] == "": #khong co lien ket
                    #ghi ra file output voi format la column
                    #file_writer.write("0")
                    #vi lay 4 gia tri nen lam 4 so 0
                    file_writer.write('0\t0\t0\t0')
                    file_writer.write("\n") # new line
                    number_of_line += 1
                    continue

                #Tim longest gram length tuong ung voi cac index nguon
                #list_of_word_source = Word_Source[len(list_temp)]
                list_of_word_source = [] # empty list
                """
                print("*list_longest_source_gram_length*")
                print(list_longest_source_gram_length)
                print("*list_longest_source_gram_length*")
                """
                for i_temp in range(len(list_temp)):
                    int_index = int(list_temp[i_temp])
                    """
                    print("*i_temp*")
                    print(i_temp)
                    print(len(list_temp))
                    print(list_temp)
                    print("*i_temp*")

                    print("*int_index* lan thu %d" %i_temp)
                    print(int_index)
                    print(list_longest_source_gram_length)
                    print("*int_index* lan thu %d" %i_temp)
                    """
                    #kiem tra neu vuot qua index. co nghia la khong ket noi voi tu nao
                    if int_index >= len(list_longest_source_gram_length):
                        temp_longest_source_gram_length = "0"
                        list_of_word_source.append(Word_Source(int_index, temp_longest_source_gram_length))
                    else:
                        list_of_word_source.append(Word_Source(int_index, list_longest_source_gram_length[int_index]))

                    #list_of_word_source[i].set_index(int_index)
                    #list_of_word_source[i].set_longest_gram_length(list_longest_source_gram_length[int_index])
                #end for

                #gan list_alignment_target_to_source da duoc tach (neu co) vao list_of_words_alignment_target_to_source
                #list_of_words_alignment_target_to_source[i].set_list_words_aligned_to_source(list_of_word_source)
                """
                if len(list_of_word_source) ==0:
                    print("Khong co gia tri nao duoc gan ?!?!?")
                else:
                    print("*list_of_word_source*")
                    for i_temp1 in list_of_word_source:
                        print(i_temp1.get_index())
                        print(i_temp1.get_longest_gram_length())
                    print("*list_of_word_source*")
                """

                #Dua danh sach cac tu nguon (index, longest gram length) vao tu dich tuong ung
                list_of_words_alignment_target_to_source = Word_Target_Language(list_of_word_source)

                """
                list_2 = list_of_words_alignment_target_to_source.get_list_of_words_aligned_to_source()

                print("*list_2*")
                for i_temp1 in list_2:
                    print(i_temp1.get_index())
                    print(i_temp1.get_longest_gram_length())
                print("*list_2*")

                print("*TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX*")
                print(list_of_words_alignment_target_to_source.get_max_longest_source_gram_length_aligned_target())
                #print(list_of_words_alignment_target_to_source.get_max_longest_source_gram_length_aligned_target(list_of_word_source))
                print("*TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX*")
                """

                #tuy tung loai type ma chung ta lay ket qua khac nhau
                #type_longest_gram_source_length
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL = 0
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX = 1
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN = 2
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG = 3
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST = 4

                current_config = load_configuration()

                #init
                int_max = 0
                int_min = 0
                int_avg = 0
                int_first = 0

                #max
                int_max = list_of_words_alignment_target_to_source.get_max_longest_source_gram_length_aligned_target()
                str_max = str(int_max)

                #min
                int_min = list_of_words_alignment_target_to_source.get_min_longest_source_gram_length_aligned_target()
                str_min = str(int_min)

                #avg
                int_avg = list_of_words_alignment_target_to_source.get_avg_longest_source_gram_length_aligned_target()
                str_avg = str(int_avg)

                #first
                int_first = list_of_words_alignment_target_to_source.get_first_longest_source_gram_length_aligned_target()
                str_first = str(int_first)

                #just for testing
                """
                if int_max != int_min:
                    print("index cua tu co min khac max la: %d trong cau thu %d. " % (i,number_of_sentence))
                    print("---> o dong thu %d " % (number_of_line + 1))
                """

                str_out = ""

                if type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL:
                    str_out = str_max + "\t" + str_min + "\t" + str_avg + "\t" + str_first
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX:
                    str_out = str_max
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN:
                    str_out = str_min
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG:
                    str_out = str_avg
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST:
                    str_out = str_first

                #ghi ra file output voi format la column
                file_writer.write(str_out)

                file_writer.write("\n") # new line
                number_of_line += 1

            #end if
        #end for

        #print("Da xu ly xong cau thu %d" %number_of_sentence)
        number_of_sentence = number_of_sentence + 1
        file_writer.write("\n") # new line for new sentence
        number_of_line += 1

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
    #end for

    #close files
    file_reader_output_from_moses.close()

    #for writing: file_output_path
    file_writer.close()

    print("Nb of words processed: %d" %number_of_word)

#**************************************************************************#
#HYPOTHESIS_ROW_CORPUS
def feature_longest_gram_source_length_threads(file_output_from_moses_included_alignment_word_to_word_path,  file_temp_longest_source_gram_length_not_aligned_target_row_path, type_longest_gram_source_length, file_output_path, current_config, config_end_user):
    """
    Create longest gram source length
    =============================================================
    2 : means that "Tu DICH tai index 0 canh le voi tu NGUON co longest gram length la 2 trong Language Model cua ngon ngu NGUON "
    3
    4
    2
    3

    :type file_output_from_moses_included_alignment_word_to_word_path: string
    :param file_output_from_moses_included_alignment_word_to_word_path: the ouput included alignment word to word from target to source (MOSES format)

    :type file_temp_longest_source_gram_length_not_aligned_target_row_path: string
    :param file_temp_longest_source_gram_length_not_aligned_target_row_path: file longest source gram length not aligned target path

    :type type_longest_gram_source_length: string
    :param type_longest_gram_source_length: the type of longest gram source length of each target word in the following types {MIN, MAX, AVG, FIRST} ~ TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX

    :type file_output_path: string
    :param file_output_path: longest gram source length of each target word

    :raise ValueError: if any path is not existed
    """

    # check existed paths
    """
    if not os.path.exists(file_output_from_moses_included_alignment_word_to_word_path):
        raise TypeError('Not Existed file MOSES format in output-moses included alignment word to word path')

    if not os.path.exists(file_temp_longest_source_gram_length_not_aligned_target_row_path):
        raise TypeError('Not Existed file Temp Longest SOURCE gram length not aligned TARGET path')
    """
    str_message_if_not_existed = "Not Existed file MOSES format in output-moses included alignment word to word path"
    is_existed_file(file_output_from_moses_included_alignment_word_to_word_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file Temp Longest SOURCE gram length not aligned TARGET path"
    is_existed_file(file_temp_longest_source_gram_length_not_aligned_target_row_path, str_message_if_not_existed)

    #for reading: file_output_from_moses_included_alignment_word_to_word_path
    file_reader_output_from_moses = open(file_output_from_moses_included_alignment_word_to_word_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    # Duyet tung cau dich --> xem xet co bao nhieu "tu" & gan danh sach cac tu nguon duoc aligned la RONG (empty) nghia la list_of_words_alignment_target_to_source = []
    number_of_sentence = 1
    number_of_line = 0
    number_of_word = 0

    for line_in_output_moses in file_reader_output_from_moses:
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
        #trim string
        line_in_output_moses = line_in_output_moses.strip()

        if len(line_in_output_moses) == 0:
            print("Xuat hien dong trong - Empty line ... You should check corpus...")
            print("Xem lai cau %d nha!!!???" %number_of_sentence)
            continue

        #Duyet Tung cau dich va cau moses va xet
        #0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m. camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
        #list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses(line_in_output_moses) #version 1 - Target - Source _ nhom cuoi cua MOSES output
        #config_end_user = load_config_end_user()
        list_alignment_target_to_source = []

        if config_end_user.VERSION_MOSES == 2009:
            list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE(line_in_output_moses)
        else:
            list_alignment_target_to_source = get_list_alignment_target_to_source_from_line_output_moses_SOURCE_To_TARGET(line_in_output_moses)

        #cong 1 co nghia la het 1 cau
        number_of_word += len(list_alignment_target_to_source) + 1
        """
        print("*list_alignment_target_to_source*")
        print(list_alignment_target_to_source)
        print("*list_alignment_target_to_source*")
        """

        #get temp_longest_source_gram_length_not_aligned_target_row
        line_longest_source_gram_length = get_line_given_number_of_sentence(file_temp_longest_source_gram_length_not_aligned_target_row_path, number_of_sentence)
        list_longest_source_gram_length = line_longest_source_gram_length.split() #Delimiter default = " "
        """
        print("*number_of_sentence*")
        print(number_of_sentence)
        print("*number_of_sentence*")

        print("*line_longest_source_gram_length*")
        print(line_longest_source_gram_length)
        print("*line_longest_source_gram_length*")

        print("*list_longest_source_gram_length*")
        print(list_longest_source_gram_length)
        print("*list_longest_source_gram_length*")
        """

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

        for i in range(len(list_alignment_target_to_source)):
            index_alignment_to_source = list_alignment_target_to_source[i]

            """
            print("*index_alignment_to_source**********************")
            print(index_alignment_to_source)
            print("*index_alignment_to_source**********************")
            """

            list_temp = [] # empty list

            #lay chuoi ra, neu chua dau phay ,
            if is_in_string(comma_char, index_alignment_to_source): #co tu 2 lien ket voi nguon tro len
                list_temp = index_alignment_to_source.split(comma_char)

            else: #neu chi la 1 so nguyen, khong chua dau phay , co nghia la: chi chua 1 phan tu
                list_temp.append(str(index_alignment_to_source))
            #end if

            #Duyet cac phan tu trong list_temp de lay longest gram length cua source tuong thich
            """
            print("*list_temp**********************")
            print(list_temp)
            print("*list_temp**********************")
            print(len(list_temp))
            print("*list_temp**********************")
            """

            if len(list_temp) == 0:
                #ghi ra file output voi format la column
                #file_writer.write('0')
                #vi lay 4 gia tri nen lam 4 so 0
                file_writer.write('0\t0\t0\t0')
                file_writer.write("\n") # new line
                number_of_line += 1
                """
                print("*Gia tri la: 0 *")
                print(0)
                print("*Gia tri la: 0 *")
                """
                continue
            else:
                #neu trong list_temp co tu 2 tu nguon duoc noi voi tu dich thi phu thuoc vao type chung ta co ket qua tuong ung
                #print("*Gia tri khac 0 *")

                if list_temp[0] == "": #khong co lien ket
                    #ghi ra file output voi format la column
                    #file_writer.write("0")
                    #vi lay 4 gia tri nen lam 4 so 0
                    file_writer.write('0\t0\t0\t0')
                    file_writer.write("\n") # new line
                    number_of_line += 1
                    continue

                #Tim longest gram length tuong ung voi cac index nguon
                #list_of_word_source = Word_Source[len(list_temp)]
                list_of_word_source = [] # empty list
                """
                print("*list_longest_source_gram_length*")
                print(list_longest_source_gram_length)
                print("*list_longest_source_gram_length*")
                """
                for i_temp in range(len(list_temp)):
                    int_index = int(list_temp[i_temp])
                    """
                    print("*i_temp*")
                    print(i_temp)
                    print(len(list_temp))
                    print(list_temp)
                    print("*i_temp*")

                    print("*int_index* lan thu %d" %i_temp)
                    print(int_index)
                    print(list_longest_source_gram_length)
                    print("*int_index* lan thu %d" %i_temp)
                    """
                    #kiem tra neu vuot qua index. co nghia la khong ket noi voi tu nao
                    if int_index >= len(list_longest_source_gram_length):
                        temp_longest_source_gram_length = "0"
                        list_of_word_source.append(Word_Source(int_index, temp_longest_source_gram_length))
                    else:
                        list_of_word_source.append(Word_Source(int_index, list_longest_source_gram_length[int_index]))

                    #list_of_word_source[i].set_index(int_index)
                    #list_of_word_source[i].set_longest_gram_length(list_longest_source_gram_length[int_index])
                #end for

                #gan list_alignment_target_to_source da duoc tach (neu co) vao list_of_words_alignment_target_to_source
                #list_of_words_alignment_target_to_source[i].set_list_words_aligned_to_source(list_of_word_source)
                """
                if len(list_of_word_source) ==0:
                    print("Khong co gia tri nao duoc gan ?!?!?")
                else:
                    print("*list_of_word_source*")
                    for i_temp1 in list_of_word_source:
                        print(i_temp1.get_index())
                        print(i_temp1.get_longest_gram_length())
                    print("*list_of_word_source*")
                """

                #Dua danh sach cac tu nguon (index, longest gram length) vao tu dich tuong ung
                list_of_words_alignment_target_to_source = Word_Target_Language(list_of_word_source)

                """
                list_2 = list_of_words_alignment_target_to_source.get_list_of_words_aligned_to_source()

                print("*list_2*")
                for i_temp1 in list_2:
                    print(i_temp1.get_index())
                    print(i_temp1.get_longest_gram_length())
                print("*list_2*")

                print("*TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX*")
                print(list_of_words_alignment_target_to_source.get_max_longest_source_gram_length_aligned_target())
                #print(list_of_words_alignment_target_to_source.get_max_longest_source_gram_length_aligned_target(list_of_word_source))
                print("*TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX*")
                """

                #tuy tung loai type ma chung ta lay ket qua khac nhau
                #type_longest_gram_source_length
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL = 0
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX = 1
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN = 2
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG = 3
                #TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST = 4

                #current_config = load_configuration()

                #init
                int_max = 0
                int_min = 0
                int_avg = 0
                int_first = 0

                #max
                int_max = list_of_words_alignment_target_to_source.get_max_longest_source_gram_length_aligned_target()
                str_max = str(int_max)

                #min
                int_min = list_of_words_alignment_target_to_source.get_min_longest_source_gram_length_aligned_target()
                str_min = str(int_min)

                #avg
                int_avg = list_of_words_alignment_target_to_source.get_avg_longest_source_gram_length_aligned_target()
                str_avg = str(int_avg)

                #first
                int_first = list_of_words_alignment_target_to_source.get_first_longest_source_gram_length_aligned_target()
                str_first = str(int_first)

                #just for testing
                """
                if int_max != int_min:
                    print("index cua tu co min khac max la: %d trong cau thu %d. " % (i,number_of_sentence))
                    print("---> o dong thu %d " % (number_of_line + 1))
                """

                str_out = ""

                if type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL:
                    str_out = str_max + "\t" + str_min + "\t" + str_avg + "\t" + str_first
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX:
                    str_out = str_max
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN:
                    str_out = str_min
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG:
                    str_out = str_avg
                elif type_longest_gram_source_length == current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST:
                    str_out = str_first

                #ghi ra file output voi format la column
                file_writer.write(str_out)

                file_writer.write("\n") # new line
                number_of_line += 1

            #end if
        #end for

        #print("Da xu ly xong cau thu %d" %number_of_sentence)
        number_of_sentence = number_of_sentence + 1
        file_writer.write("\n") # new line for new sentence
        number_of_line += 1

        #file_writer.close()
        #raise Exception("Just for testing ... :) Execute the first line....")
    #end for

    #close files
    file_reader_output_from_moses.close()

    #for writing: file_output_path
    file_writer.close()

    print("Nb of words processed: %d" %number_of_word)

#**************************************************************************#
#HYPOTHESIS_ROW_CORPUS


if __name__ == "__main__":

    current_config = load_configuration()

    #Buoc 1: File Source-ngram giong nhu cach lam Target-ngram
    get_temp_longest_source_gram_length_not_aligned_target( current_config.SRC_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_MODEL_SRC, current_config.N_GRAM, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET)

    #convert format column to format row
    convert_format_column_to_format_row( current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW)

    #feature_longest_gram_source_length(file_output_from_moses_included_alignment_word_to_word_path,  file_temp_longest_source_gram_length_not_aligned_target_row_path, type_longest_gram_source_length, file_output_path)
    feature_longest_gram_source_length( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW, current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL, current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

    print ('OK')