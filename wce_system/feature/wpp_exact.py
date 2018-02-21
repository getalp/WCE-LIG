# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 18:58:53 2014
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

#Purpose: Extracting the following features: WPP any, Nodes, Min, Max
import sys
import os

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
from common_module.cm_config import load_configuration#, load_config_end_user
from common_module.cm_file import is_existed_file, delete_all_files_temporary
#from common_module.cm_script import *
#from common_module.cm_tool import get_output_treetagger_format_row
#from common_module.cm_util import  is_in_string, print_time, print_result

#??? can dem cau bi lech cua wpp_exact va wpp_any
#??? viet bao cao & tom luot toan bo
#??? cai dat va bat dau lam viec voi KALDI

#**************************************************************************#
#Tao class Word_Position_Probability
class Word_Position_Probability(object):
    """
    This class contains the following information of words in nBestList. Note: The probability of each word has been accumulated the probabilities from other hypothesis sentences' probability when that word could appear in exact position in other hypothesis sentences.
    """
    word = ""
    position = 0
    probability = 0.0

    def __init__(self):
        self.word = ""
        self.position = 0
        self.probability = 0.0

    def __init__(self, word, position, probability):
        self.word = word
        self.position = position
        self.probability = probability

    def set_word(self, word=""):
        self.word = word

    def set_position(self, position=0):
        self.position = position

    def set_probability(self, probability=0.0):
        self.probability = probability

    def get_word(self):
        return self.word

    def get_position(self):
        return self.position

    def get_probability(self):
        return self.probability

    #operator overloading --> should accumulate
    def __add__(self, other):
        return self.probability + other.get_probability()

    #operator overding --> equal
    #neu 2 tu o cung vi tri va co noi dung giong nhau thi "bang nhau"
    #ref: https://docs.python.org/3.1/reference/datamodel.html
    # x==y calls x.__eq__(y)
    def __eq__(self, other):
        str1 = self.word.lower()
        pos1 = self.position

        str2 = other.get_word().lower()
        pos2 = other.get_position()

        if str1 == str2 and pos1==pos2:
            return True
        else:
            return False
#**************************************************************************#
def preprocessing_for_extracting():
    """
    + Deleting all files Phrase* in directory that contains code "nbestToLattice.sh"
    + Change mode execute for 2 files for fastnc & "nbestToLattice.sh"
    """
    #delete all file "Phrase*" --> moved to common_functions
    delete_all_files_temporary()

#**************************************************************************#
#* Buoc 1:
#+ Duyet tat ca cac dong trong n-best-list
#+ Dua thong tin cua cac cau gom: ... vao cac file co ID tuong ung
# xac suat cua cau|||Noi dung cau output cua n-best-list
def split_sentences_with_id(file_input_path, output_path):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type output_path: string
    :param output_path: contains path to script "nbestToLattice.sh"

    :rtype: the number of sentences in n-best-list. Default = 1000

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output from TreeTagger')

    #open files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    delimiter = "|||"
    number_of_sentences = 0

    """
0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15

0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , declared m camus .  ||| LexicalReordering0= -2.31489 0 0 -1.80126 0 0 Distortion0= 0 LM0= -147.721 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -6.58588 -6.62274 -4.26 -5.77525 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
    """
    current_index = -1 # gia su chua doc cau nao
    current_file_name = "PhraseN"
    int_number_of_sentences_in_PhraseN = 0
    max_number_of_sentences_in_PhraseN = 1000

    for line in file_reader:
        list_items = [] # set empty list

        line = line.strip() #trim line

        if len(line) == 0: #xuong dong hay het file
            break

        list_items = line.split(delimiter) # Split with delimiter "|||"

        if len(list_items) ==0:
            break

        #output: -1014.93|||the chirurgiens of los angeles ont said qu' ils étaient outrés , said m camus .
        #weighted overall score ~ index_3; hypothesis sentence
        str_index = list_items[0].strip() # trim string

        #weighted overall score
        str_weighted_overall_score = list_items[3].strip() # trim string

        #hypothesis sentence
        hyp_sentence = list_items[1].strip() # trim string

        #output string for PhraseN
        str_output = str_weighted_overall_score + delimiter + hyp_sentence

        #lay thu muc hien tai
        current_working_directory = os.getcwd()

        #chuyen den thu muc chua code script
        os.chdir(os.path.dirname(output_path))

        int_index = int(str_index)

        if int_index != current_index:
            #cau moi --> thay file de ghi vao
            current_index = int_index
            number_of_sentences += 1

            ##just for checking
            ##doi voi nhung PhraseN co du so luong N-best-list
            if int_number_of_sentences_in_PhraseN != max_number_of_sentences_in_PhraseN:
                print("%s co %d cau trong n-best-list." %(current_file_name, int_number_of_sentences_in_PhraseN))

            #update current_file_name = "PhraseN"
            #append information to file with new id
            current_file_name = "Phrase" + str_index
            int_number_of_sentences_in_PhraseN = 0
        #end if

        #for appending: file_output_path
        file_writer = open(current_file_name, mode = 'a', encoding = 'utf-8')
        int_number_of_sentences_in_PhraseN += 1

        file_writer.write(str_output)
        file_writer.write("\n")

        file_writer.close()

        #chuyen lai thu muc hien tai
        os.chdir(current_working_directory)

    #end for

    return number_of_sentences
#**************************************************************************#
# New version for the multithreaded option
def split_sentences_with_id_threads(file_input_path, output_path):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type output_path: string
    :param output_path: contains path to script "nbestToLattice.sh"

    :rtype: the number of sentences in n-best-list. Default = 1000

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output from TreeTagger')

    #open files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    delimiter = "|||"
    number_of_sentences = 0

    """
0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15

0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , declared m camus .  ||| LexicalReordering0= -2.31489 0 0 -1.80126 0 0 Distortion0= 0 LM0= -147.721 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -6.58588 -6.62274 -4.26 -5.77525 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
    """
    current_index = -1 # gia su chua doc cau nao
    current_file_name = "PhraseN"
    int_number_of_sentences_in_PhraseN = 0
    max_number_of_sentences_in_PhraseN = 1000
    first_index = -1

    for line in file_reader:
        list_items = [] # set empty list

        line = line.strip() #trim line

        if len(line) == 0: #xuong dong hay het file
            break

        list_items = line.split(delimiter) # Split with delimiter "|||"

        if len(list_items) ==0:
            break

        #output: -1014.93|||the chirurgiens of los angeles ont said qu' ils étaient outrés , said m camus .
        #weighted overall score ~ index_3; hypothesis sentence
        str_index = list_items[0].strip() # trim string
        if first_index == -1:
            first_index = int(str_index)


        #weighted overall score
        str_weighted_overall_score = list_items[3].strip() # trim string

        #hypothesis sentence
        hyp_sentence = list_items[1].strip() # trim string

        #output string for PhraseN
        str_output = str_weighted_overall_score + delimiter + hyp_sentence

        #lay thu muc hien tai
        current_working_directory = os.getcwd()

        #chuyen den thu muc chua code script
        #os.chdir(os.path.dirname(output_path))
        #os.chdir(output_path)

        int_index = int(str_index)

        if int_index != current_index:
            #cau moi --> thay file de ghi vao
            current_index = int_index
            number_of_sentences += 1

            ##just for checking
            ##doi voi nhung PhraseN co du so luong N-best-list
            if int_number_of_sentences_in_PhraseN != max_number_of_sentences_in_PhraseN:
                print("%s nbest size: %d " %(current_file_name, int_number_of_sentences_in_PhraseN))

            #update current_file_name = "PhraseN"
            #append information to file with new id
            current_file_name = output_path + "/" +"Phrase" + str_index
            int_number_of_sentences_in_PhraseN = 0
        #end if

        #for appending: file_output_path
        file_writer = open(current_file_name, mode = 'a', encoding = 'utf-8')
        int_number_of_sentences_in_PhraseN += 1

        file_writer.write(str_output)
        file_writer.write("\n")

        file_writer.close()

        #chuyen lai thu muc hien tai
        #os.chdir(current_working_directory)

    #end for

    return first_index, number_of_sentences
#**************************************************************************#
def get_list_Word_Position_Probability_from_string(string_input):
    """
    Getting List of Word_Position_Probability from String within format "#weighted overall score|||hypothesis sentence"

    :type file_input_path: string_input
    :param file_input_path: string within format "#weighted overall score|||hypothesis sentence"
    """
    delimiter = "|||"
    result = []

    list_items = string_input.split(delimiter) # Split with delimiter "|||"

    if len(list_items) ==0:
        return result #empty list

    #weighted overall score ~ index_0; hypothesis sentence
    str_weighted_overall_score = list_items[0].strip() # trim string
    probability = float(str_weighted_overall_score) #float datatype

    #hypothesis sentence
    hyp_sentence = list_items[1].strip().split() # trim string & split within Default delimiter ""

    if len(hyp_sentence) ==0:
        return result #empty list

    #Traverse hypothesis sentence for creating list "Word_Position_Probability(word, position, probability)"
    position = 0
    for item_word in hyp_sentence:
        word = item_word
        #print(word)
        #print(position)
        #print(probability)
        result.append(Word_Position_Probability(word, position, probability))

        position += 1
    #end for

    return result
#**************************************************************************#
#Doc tung file PhraseN
#    sum_all_probabilities = 0 #sum for PhraseK
#    list_for_first_sentence = []
#    is_first_line = False
#    Doc tung dong trong file
#        convert line to list_temp "list of objects"
#        sum_all_probabilities += list_temp[0].get_probability()
#        Neu not is_first_line thi:
#            luu lai 1 bien rieng list_for_first_sentence
#            is_first_line = True
#        Nguoc lai:
#            quet theo position cac item trong list_for_first_sentence:
#                lay tu tai vi tri position trong list_temp --> so sanh; neu = thi cong don vao tu do
#    sau cung la duyet list_for_first_sentence de tinh WPP_Exact va luu ra file_output_path
#**************************************************************************#
# Duyet cau dau tien de dua vao List cac object Word_Position_Probability
# Duyet theo POS cua cau thu 2 den het PhraseN de:
# + Neu tai vi tri POS co word giong word giong word o cau 1 thi cong don
# xac suat
def feature_wpp_exact(file_input_path, file_output_path):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type file_output_path: string
    :param file_output_path: contains corpus with format "WPP exact" in each line; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #Delete all files Phrase* if existed
    preprocessing_for_extracting()

    #generate Phrase* with format:
    #weighted overall score|||hypothesis sentence
    current_config = load_configuration()

    number_of_sentences = split_sentences_with_id(file_input_path, current_config.SCRIPT_TEMP)

    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing PhraseNs
    os.chdir(os.path.dirname(current_config.SCRIPT_TEMP))

    #xu ly du lieu dua vao PhraseN
    current_path = os.getcwd()
    strPhrase = "Phrase"
    current_number_of_phrase = 0
    while current_number_of_phrase < number_of_sentences:
        str_current_number_of_phrase = str(current_number_of_phrase)

        file_name = strPhrase + str_current_number_of_phrase
        file_name_path = current_path + "/" + file_name

        #print("file name & current_path: BEGIN")
        #print(file_name_path)
        #print("file name & current_path: END")

        #check existed paths
        if not os.path.exists(file_name_path):
            raise TypeError('Not Existed file corpus input %s' %file_name_path)

        #open file
        file_reader = open(file_name_path, mode = 'r', encoding = 'utf-8')

        sum_all_probabilities = 0 #sum of the probabilities for PhraseK
        list_for_first_sentence = []
        is_first_line = False

        for line in file_reader:
            list_temp = get_list_Word_Position_Probability_from_string(line)

            sum_all_probabilities += list_temp[0].get_probability()

            #print(line)
            #print(list_temp[0].get_probability())
            #print(sum_all_probabilities)

            if not is_first_line: #first line
                list_for_first_sentence = list_temp
                is_first_line = True
            else:
                pos_range = range(len(list_for_first_sentence))

                #just for testing
                #print(pos_range)
                #break

                length_of_list_temp = len(list_temp)

                for pos in pos_range:
                    if pos >= length_of_list_temp: #neu position nho hon length_of_list_temp thi xu ly tiep
                        break

                    current_Word_Position_Probability = list_for_first_sentence[pos]
                    Word_Position_Probability_in_list_temp_given_pos = list_temp[pos]

                    if current_Word_Position_Probability == Word_Position_Probability_in_list_temp_given_pos:
                        update_probability = current_Word_Position_Probability + Word_Position_Probability_in_list_temp_given_pos
                        list_for_first_sentence[pos].set_probability(update_probability)
                    #end if
                #end for
            #end if
        #end for

        #print(sum_all_probabilities)

        #sau khi duyet het cac dong trong file thi ap dung cong thuc tinh WPP Exact cho list_for_first_sentence va ghi ra file_output_path
        #mo file append
        file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

        for item in list_for_first_sentence:
            probability_each_word = item.get_probability()
            wpp_exact_each_word = probability_each_word / sum_all_probabilities

            file_writer.write(str(wpp_exact_each_word))
            file_writer.write("\n") # empty line
        #end for

        file_writer.write("\n") # empty line, purpose: seperate the sentences

        #close files
        file_reader.close()
        file_writer.close()

        current_number_of_phrase += 1
    #end while

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)

    #Delete Phrase files
    #preprocessing_for_extracting()
#**************************************************************************#
def feature_wpp_exact_threads(file_input_path, file_output_path, n_thread,current_config):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type file_output_path: string
    :param file_output_path: contains corpus with format "WPP exact" in each line; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #Delete all files Phrase* if existed
    #preprocessing_for_extracting()


    #generate Phrase* with format:
    #weighted overall score|||hypothesis sentence
    #current_config = load_configuration()

    tmp_dir = "/tmp/WCE_wpp_exact_feature"+ "_" + str(n_thread)
    try:
      os.stat(tmp_dir)
    except:
      os.mkdir(tmp_dir)
    #tmp_dir = current_config.SCRIPT_TEMP + "_" + str(n_thread)
    print (file_input_path)
    print (tmp_dir)

    first_sentence, number_of_sentences = split_sentences_with_id_threads(file_input_path, tmp_dir)

    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing PhraseNs
    os.chdir(os.path.dirname(tmp_dir))

    #xu ly du lieu dua vao PhraseN
    current_path = os.path.realpath(tmp_dir)
      #os.getcwd()
    strPhrase = "Phrase"
    current_number_of_phrase = first_sentence
    while current_number_of_phrase < (first_sentence+number_of_sentences):
        str_current_number_of_phrase = str(current_number_of_phrase)

        file_name = strPhrase + str_current_number_of_phrase
        file_name_path = current_path + "/" + file_name

        #print("file name & current_path: BEGIN")
        #print(file_name_path)
        #print("file name & current_path: END")

        #check existed paths
        if not os.path.exists(file_name_path):
            raise TypeError('Not Existed file corpus input %s' %file_name_path)

        #open file
        file_reader = open(file_name_path, mode = 'r', encoding = 'utf-8')

        sum_all_probabilities = 0 #sum of the probabilities for PhraseK
        list_for_first_sentence = []
        is_first_line = False

        for line in file_reader:
            list_temp = get_list_Word_Position_Probability_from_string(line)

            sum_all_probabilities += list_temp[0].get_probability()

            #print(line)
            #print(list_temp[0].get_probability())
            #print(sum_all_probabilities)

            if not is_first_line: #first line
                list_for_first_sentence = list_temp
                is_first_line = True
            else:
                pos_range = range(len(list_for_first_sentence))

                #just for testing
                #print(pos_range)
                #break

                length_of_list_temp = len(list_temp)

                for pos in pos_range:
                    if pos >= length_of_list_temp: #neu position nho hon length_of_list_temp thi xu ly tiep
                        break

                    current_Word_Position_Probability = list_for_first_sentence[pos]
                    Word_Position_Probability_in_list_temp_given_pos = list_temp[pos]

                    if current_Word_Position_Probability == Word_Position_Probability_in_list_temp_given_pos:
                        update_probability = current_Word_Position_Probability + Word_Position_Probability_in_list_temp_given_pos
                        list_for_first_sentence[pos].set_probability(update_probability)
                    #end if
                #end for
            #end if
        #end for

        #print(sum_all_probabilities)

        #sau khi duyet het cac dong trong file thi ap dung cong thuc tinh WPP Exact cho list_for_first_sentence va ghi ra file_output_path
        #mo file append
        file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')

        for item in list_for_first_sentence:
            probability_each_word = item.get_probability()
            wpp_exact_each_word = probability_each_word / sum_all_probabilities

            file_writer.write(str(wpp_exact_each_word))
            file_writer.write("\n") # empty line
        #end for

        file_writer.write("\n") # empty line, purpose: seperate the sentences

        #close files
        file_reader.close()
        file_writer.close()

        current_number_of_phrase += 1
    #end while

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)

    #Delete Phrase files - Tien tam disabled :) just for testing ...
    # for root, dirs, files in os.walk(tmp_dir):
    #   for f in files:
    #     os.unlink(os.path.join(root, f))
    #   for d in dirs:
    #     shutil.rmtree(os.path.join(root, d))
    #preprocessing_for_extracting()
#**************************************************************************#


if __name__=="__main__":
    #split sentences with ID from n-best-list
    current_config = load_configuration()

    #chu y: cac buoc nay chua chuan hoa
    #chuan hoa cac thong so ve he so 10 hay 100 --> update code de phu hop voi yeu cau bai toan

    feature_wpp_exact( current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT,  current_config.WPP_EXACT)

    print ('OK')

"""
Phrase455 co 449 cau trong n-best-list.
Phrase3474 co 1 cau trong n-best-list.
Phrase4178 co 224 cau trong n-best-list.
Phrase4526 co 982 cau trong n-best-list.
Phrase4660 co 12 cau trong n-best-list.
Phrase4661 co 12 cau trong n-best-list.
Phrase5755 co 224 cau trong n-best-list.
Phrase5783 co 800 cau trong n-best-list.
Phrase5944 co 464 cau trong n-best-list.
Phrase6305 co 20 cau trong n-best-list.
Phrase6989 co 478 cau trong n-best-list.
Phrase7483 co 236 cau trong n-best-list.
Phrase7651 co 555 cau trong n-best-list.
Phrase9075 co 42 cau trong n-best-list.
Phrase9213 co 477 cau trong n-best-list.
Phrase9269 co 477 cau trong n-best-list.
Phrase9559 co 662 cau trong n-best-list.
Phrase10273 co 40 cau trong n-best-list.
Phrase10342 co 40 cau trong n-best-list.
Phrase10648 co 1 cau trong n-best-list.
Phrase10671 co 800 cau trong n-best-list.
Phrase10685 co 40 cau trong n-best-list.
Phrase10744 co 20 cau trong n-best-list.

"""
