# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 13:10:12 2014
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

import os
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
#from config.configuration import *
from common_module.cm_util import split_string_to_list_delimeter_tab, is_in_list
from common_module.cm_file import is_existed_file
from common_module.cm_config import load_configuration
#**************************************************************************#
###Nen dung TreeTagger tren dong roi rut trich thong tin tu day
def feature_proper_name(file_input_path, target_language, file_output_path):
    """
    Counting each word (w) of each line (in file_input_path) and the frequency of each word in each line is written in file_output_path

    :type file_input_path: string
    :param file_input_path: contains corpus with format each word, pos, stemming in each line; there is a empty line among the sentences.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains the frequency of each word in each line.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #number_of_sentences = 0

    #get list of recognition unknown lemma
    list_of_unknown_lemma = ['<UNK>','<unknown>']

    #list of POS for recognizing Proper Name
    list_of_pos_proper_name = []

    list_of_pos_other_noun = []
    current_config = load_configuration()

    if target_language == current_config.LANGUAGE_SPANISH: #ref: http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/spanish-tagset.txt
        list_of_pos_proper_name = ["NP"]

    elif target_language == current_config.LANGUAGE_FRENCH:
        list_of_pos_proper_name = ["NAM"]
        list_of_pos_other_noun = ["NOM"]

    elif target_language == current_config.LANGUAGE_ENGLISH:
        list_of_pos_proper_name = ["NP","NPS","NP$","NPS$", "NNP"]
        list_of_pos_other_noun = ["NN", "NNS"]

    #read data in openned file
    for line in file_reader:
        is_proper_name = False

        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue

        #print("line = %s" %line)
        """Line 46755
        florence	NN	<unknown>
        <unk> <unk> <unk>
        believes	VVZ	believe
        """
        #Truong hop dac biet: khi du lieu chi chua UNK
        """
        str_UNK = "<UNK>"
        if line == str_UNK:
            file_writer.write('0\n')
            continue
        #end if
        """

        #format: word POS lemma
        #angeles	NNS	<unknown>
        values_cols = split_string_to_list_delimeter_tab(line)

        if len(list_of_pos_proper_name) == 0:
            raise Exception("You should add information of Target Language OR contact to developer Tien Ngoc LE and Tan Ngoc LE")

        pos_word = values_cols[1] #pos word, get value at index=1
        lemma_word = values_cols[2] # lemma of word

        #check existed value_col_stem in list of proper name
        if target_language == current_config.LANGUAGE_ENGLISH:
            if is_in_list(pos_word, list_of_pos_proper_name):
                is_proper_name = True
            if is_in_list(lemma_word, list_of_unknown_lemma) and is_in_list(pos_word, list_of_pos_other_noun):
                is_proper_name = True

        elif target_language == current_config.LANGUAGE_FRENCH:
            if is_in_list(pos_word, list_of_pos_proper_name):
                is_proper_name = True
            if is_in_list(lemma_word, list_of_unknown_lemma) and is_in_list(pos_word, list_of_pos_other_noun):
                is_proper_name = True
        elif target_language == current_config.LANGUAGE_SPANISH:
            if is_in_list(pos_word, list_of_pos_proper_name):
                is_proper_name = True

        if is_proper_name:
            file_writer.write('1\n')
        else:
            file_writer.write('0\n')
        #end if

        #number_of_sentences = number_of_sentences + 1

    #end for

    #print("Number of sentences is traversed: %d " % number_of_sentences)

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
def feature_proper_name_threads(file_input_path, target_language, file_output_path,current_config):
    """
    Counting each word (w) of each line (in file_input_path) and the frequency of each word in each line is written in file_output_path

    :type file_input_path: string
    :param file_input_path: contains corpus with format each word, pos, stemming in each line; there is a empty line among the sentences.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains the frequency of each word in each line.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #number_of_sentences = 0

    #get list of recognition unknown lemma
    list_of_unknown_lemma = ['<UNK>','<unknown>']

    #list of POS for recognizing Proper Name
    list_of_pos_proper_name = []

    list_of_pos_other_noun = []
    #current_config = load_configuration()

    if target_language == current_config.LANGUAGE_SPANISH: #ref: http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/spanish-tagset.txt
        list_of_pos_proper_name = ["NP"]

    elif target_language == current_config.LANGUAGE_FRENCH:
        list_of_pos_proper_name = ["NAM"]
        list_of_pos_other_noun = ["NOM"]

    elif target_language == current_config.LANGUAGE_ENGLISH:
        list_of_pos_proper_name = ["NP","NPS","NP$","NPS$", "NNP"]
        list_of_pos_other_noun = ["NN", "NNS"]

    #read data in openned file
    for line in file_reader:
        is_proper_name = False

        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue

        #print("line = %s" %line)
        """Line 46755
        florence	NN	<unknown>
        <unk> <unk> <unk>
        believes	VVZ	believe
        """
        #Truong hop dac biet: khi du lieu chi chua UNK
        """
        str_UNK = "<UNK>"
        if line == str_UNK:
            file_writer.write('0\n')
            continue
        #end if
        """

        #format: word POS lemma
        #angeles	NNS	<unknown>
        values_cols = split_string_to_list_delimeter_tab(line)

        if len(list_of_pos_proper_name) == 0:
            raise Exception("You should add information of Target Language OR contact to developer Tien Ngoc LE and Tan Ngoc LE")

        pos_word = values_cols[1] #pos word, get value at index=1
        lemma_word = values_cols[2] # lemma of word

        #check existed value_col_stem in list of proper name
        if target_language == current_config.LANGUAGE_ENGLISH:
            if is_in_list(pos_word, list_of_pos_proper_name):
                is_proper_name = True
            if is_in_list(lemma_word, list_of_unknown_lemma) and is_in_list(pos_word, list_of_pos_other_noun):
                is_proper_name = True

        elif target_language == current_config.LANGUAGE_FRENCH:
            if is_in_list(pos_word, list_of_pos_proper_name):
                is_proper_name = True
            if is_in_list(lemma_word, list_of_unknown_lemma) and is_in_list(pos_word, list_of_pos_other_noun):
                is_proper_name = True
        elif target_language == current_config.LANGUAGE_SPANISH:
            if is_in_list(pos_word, list_of_pos_proper_name):
                is_proper_name = True

        if is_proper_name:
            file_writer.write('1\n')
        else:
            file_writer.write('0\n')
        #end if

        #number_of_sentences = number_of_sentences + 1

    #end for

    #print("Number of sentences is traversed: %d " % number_of_sentences)

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()
    #You should update target language
    target_language = current_config.LANGUAGE_SPANISH # Spanish
    #target_language = current_config.LANGUAGE_ENGLISH # English
    #target_language = current_config.LANGUAGE_FRENCH # French

    print('TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL')
    print (current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL)

    print('output')
    print(current_config.PROPER_NAME)

    feature_proper_name( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, target_language, current_config.PROPER_NAME)


    print ('OK')