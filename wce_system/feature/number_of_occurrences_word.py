# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 14:44:33 2014
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
import collections
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
from common_module.cm_util import split_string_to_list_delimeter_tab, is_in_list
from common_module.cm_file import is_existed_file
from common_module.cm_config import load_configuration

#**************************************************************************#
def feature_number_of_occurrences_word(file_input_path, file_output_path):
    """
    Counting each word (w) of each line (in file_input_path) and the frequency of each word in each line is written in file_output_path

    :type file_input_path: string
    :param file_input_path: contains corpus with format each word, pos, stemming in each line; there is a empty line among the sentences.

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

    #get list of recognition Proper name
    #list_of_proper_name = ['<UNK>','<unknown>']

    #number of sentences
    number_of_sentences = 0

    #read data in openned file
    line = file_reader.readline()

    #trim line
    line = line.strip()

    while line:
        #BEGIN - Traverse each "sentence" --> list of words in sentence
        sentence = [] # word sequence ~ word list
        while len(line) > 0:#if empty line #line in ('\n', '\r\n')
            #get value at 3rd column (column stem) -> index=2
            #angeles	NNS	<unknown>
            values_cols = split_string_to_list_delimeter_tab(line)
            #print (values_cols)
            """
            stemmed_word = values_cols[2] #stemmed word, get value at index=2

            #if value in 3rd col = "<unknown>" then update stemmed_word = value in 1st column
            if is_in_list(stemmed_word, list_of_proper_name):#check existed value_col_stem in list of proper name --> True ~ <unknown> --> Get column with index = 0
                stemmed_word = values_cols[0]

            sentence.append(stemmed_word)
            """
            str_word = values_cols[0] #word, get value at index=0

            sentence.append(str_word)

            #read next line
            line = file_reader.readline()

            #trim line
            line = line.strip()

        #END - Traverse each "sentence" --> list of words in sentence

        #print(sentence)
        #break

        #Calculating frequency of word in the sentence
        frequencies=collections.Counter(sentence)

        #print(frequencies)
        #break

        for stem in sentence:
            #print(stem)
            #print(frequencies[stem])
            #break

            #write the frequency of stemming in the sentence
            file_writer.write(str(frequencies[stem]))

            #new line
            file_writer.write('\n')

        #new line
        file_writer.write('\n')

        number_of_sentences = number_of_sentences + 1

        #read next line
        line = file_reader.readline()

        #trim line
        line = line.strip()

    #print("Number of sentences is traversed: %d " % number_of_sentences)

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    #feature_number_of_occurrences_word(file_input_path, file_output_path)
    #feature_number_of_occurrences_word('../corpus/corpus.lc.en.column.pos.stem.txt','../extracted_features/corpus.lc.en.column.feature_number_of_occurrences_word.txt')

    current_config = load_configuration()

    print('TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL corpus')
    print (current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL)

    print('output')
    print(current_config.NUMBER_OF_OCCURRENCES_WORD)

    #feature_number_of_occurrences_word(current_config.POS_STEM_CORPUS, current_config.NUMBER_OF_OCCURRENCES_WORD)
    feature_number_of_occurrences_word( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL,  current_config.NUMBER_OF_OCCURRENCES_WORD)

    print ('OK')